#!/usr/bin/env python
# coding: utf-8
import time, os, shutil, cv2, json
import pandas as pd
import numpy as np
from keras.models import load_model
import tensorflow as tf
import keras.backend.tensorflow_backend as KTF
from keras.preprocessing.image import ImageDataGenerator
from SDK.worker import worker
from SDK.const.const import wt, mt
from SDK.utilslib.fileops import parse_imgid_xy_from_cellname, get_file_lists

# 自适应分配计算资源
config = tf.ConfigProto()
config.gpu_options.allow_growth=True
session = tf.Session(config=config)
KTF.set_session(session)

#传入文件的路径，返回路径，文件名字，文件后缀
def get_filePath_fileName_fileExt(filename):
    (filepath, tempfilename) = os.path.split(filename)
    (shotname, extension) = os.path.splitext(tempfilename)
    return filepath, shotname, extension

class mala_predict(worker):
    def __init__(self, workertype):
        #初始化一个dataset的worker
        worker.__init__(self, workertype)
        self.log.info("初始化一个预测的worker")
        self.mtype = mt.MALA.value
        self.modpath = ""
        self.filtermod = ""
        self.filtermodyolo = ""
        self.filtermod90 = ""
        self.filtermodyolo2 = ""

        self.BS = 128
        self.totalTest_cross_domain = 1
        self.log.info("totalTest_cross_domain=" + str(self.totalTest_cross_domain))

    def get_all_cells_list(self):
        #获得需要训练的分类
        types = self.projectinfo['types']
        #添加默认的type
        needtypes = [100, 200, 201]
        for _needtypes in needtypes:
            if _needtypes not in types:
                types.append(_needtypes)

        self.totalTest_cross_domain = len(types)
        if len(types) < 2 and self.wtype == wt.TRAIN.value:
            self.log.error("less then 2 labels to train")
            return None
        #获得所有用作训练的细胞的信息
        df_allcells = None
        df_cells = pd.read_csv(self.cellslist_csv)
        for celltype in types:
            df2 = df_cells[df_cells['celltype'] == celltype]
            if df_allcells is None:
                df_allcells = df2
            else:
                df_allcells = df_allcells.append(df2)
        return df_allcells

    def mkdatasets(self):
        return True, []

    def update_model_info_json(self, modinfo):
        if os.path.exists(self.info_json) is False:
            return False
        job_info = self.load_info_json()
        mod = modinfo

        mod['id'] = 0
        mod['type'] = 5
        mod['types'] = job_info['types']
        mod['pid'] = job_info['id']
        mod['path'] = self.project_mod_path
        mod['desc'] = '未保存的模型'
        mod['recall'] = -1
        mod['precision'] = mod['metric_value']

        with open(self.project_mod_json, 'w', encoding='utf-8') as file:
            file.write(json.dumps(mod, indent=2, ensure_ascii=False))
        return True

    #统计预测结果
    def result_predict(self, df):
        predict_info = self.load_info_json()
        num = df.shape[0]
        result = {"result": [], "crop_cells": []}

        if predict_info['parameter_type'] == 0:
            self.log.info("统计:图片直接检测并切割出细胞")
        elif predict_info['parameter_type'] == 1:
            self.log.info("统计:按照标注csv切割细胞")

        if num > 0:
            #计算每个类别的recall/precision/f1，输出到前端log
            true_label = np.array(df["true_label"])
            predict_label = np.array(df["predict_label"])
            key = np.unique(true_label)
            self.log.info("统计:recall/precision/f1")

            if predict_info['parameter_type'] == 1:
                #统计每个分类的信息
                for true_label, df1 in df.groupby(['true_label']):
                    df_correct = df1[df1["correct"] == 1]
                    result["result"].append({"type": true_label, "total": df1.shape[0], "correct": df_correct.shape[0]})

                #统计crop_cells
                for index, row in df.iterrows():
                    cellpath = row["cellpath"][len(self.rootdir):]
                    one = {"predict": row["predict_label"], "type": row["true_label"], "url": cellpath, "score":row["score"],
                            "x1": row["x1"], "y1": row["y1"], "x2": row["x2"], "y2": row["y2"], "imgid": row["imgid"]}
                    result["crop_cells"].append(one)
            elif predict_info['parameter_type'] == 0:
                #统计每个分类的信息
                for predict_label, df1 in df.groupby(['predict_label']):
                    result["result"].append({"type": predict_label, "total": df1.shape[0], "correct": df1.shape[0]})
                #统计crop_cells
                for index, row in df.iterrows():
                    cellpath = row["cellpath"][len(self.rootdir):]
                    one = {"predict": row["predict_label"], "type": row["predict_label"], "url": cellpath, "score":row["score"],
                            "x1": row["x1"], "y1": row["y1"], "x2": row["x2"], "y2": row["y2"], "imgid": row["imgid"]}
                    result["crop_cells"].append(one)

        #写入文件
        predict_info['crop_cells'] = result['crop_cells']
        predict_info['result'] = result['result']
        self.save_info_json(predict_info, self.predict2_json)

        #记录一份到predict.json，加速后端统计预测结果
        predict_info['crop_cells'] = []
        self.save_info_json(predict_info, self.predict_json)
        return True

    def _filter(self, result201):
        result = []
        result.extend(result201)
        filter_mod='filter_model.h5'
        self.projectinfo['parameter_resize'] = 64 #模型只支持64x64

        df = self.get_all_cells_list()
        # initialize the testing generator for cross domain
        valAug = ImageDataGenerator(rescale=1 / 255.0)
        testGen_cross_domain = valAug.flow_from_dataframe(
            df, directory=None,
            x_col='cellpath', y_col=['celltype'],
           	classes=None, class_mode='raw',
        	target_size=(64, 64),
        	color_mode="rgb",
        	shuffle=False,
        	batch_size=self.BS)

        if self.filtermod != filter_mod  or self.filter_model is None:
            self.filtermod = filter_mod
            self.filter_model = load_model(self.filtermod)

        # reset the testGen_cross_domain generator and then use our trained model to
        # make predictions on the data
        testGen_cross_domain.reset()
        predIdxs = self.filter_model.predict_generator(testGen_cross_domain,
            steps=(self.totalTest_cross_domain // self.BS+1),verbose=1)

        classes = list(np.argmax(predIdxs, axis=1))
        classes_scores = []
        for i in range(len(predIdxs)):
            classes_scores.append(float('%.2f'%(max(predIdxs[i]))))
        filenames = testGen_cross_domain.filenames
        for f in zip(filenames, classes, classes_scores):
            cellpath = os.path.join(self.project_resize_predict_dir, f[0])
            predict_label = 100 #100未知细胞类型 200不是细胞
            #只记录过滤掉的，有效细胞在预测时候记录
            if int(f[1]) == 1:
                predict_label = 200
                os.remove(cellpath)
                cellpath = os.path.join(self.project_predict_dir, f[0])
            else:
                continue

            #已经按尺寸滤掉了,201
            arr = os.path.split(f[0])
            if arr[0] == "201":
                predict_label = 201

            _, shotname, extension = get_filePath_fileName_fileExt(cellpath)
            imgid, x1, y1, x2, y2 = parse_imgid_xy_from_cellname(shotname)

            result.append([cellpath, predict_label, predict_label, f[2], 1, x1, y1, x2, y2, imgid])
        #df_result = pd.DataFrame(result, columns=['cellpath', 'true_label', 'predict_label', 'score', 'correct', 'x1', 'y1', 'x2', 'y2', 'imgid'])
        return True, result

    def _predict(self, result201_200, remove_cnt_201, remove_cnt_200):
        self.projectinfo['parameter_resize'] = 64 #模型只支持64x64
        #设置预测个数
        self.BS = 128

        df = self.get_all_cells_list()
        # initialize the testing generator for cross domain
        valAug = ImageDataGenerator(rescale=1 / 255.0)
        testGen_cross_domain = valAug.flow_from_dataframe(
            df, directory=None,
            x_col='cellpath', y_col=['celltype'],
           	classes=None, class_mode='raw',
        	target_size=(64, 64),
        	color_mode="rgb",
        	shuffle=False,
        	batch_size=self.BS)
        self.totalTest_cross_domain = len(testGen_cross_domain.filenames)
        if (self.totalTest_cross_domain < 1):
            _df_result = pd.DataFrame([], columns=['cellpath', 'true_label', 'predict_label', 'score', 'correct', 'x1', 'y1', 'x2', 'y2', 'imgid'])
            return True, _df_result

        if self.modpath != self.projectinfo['modpath'] or self.model is None:
            self.modpath = self.projectinfo['modpath']
            self.model = load_model(self.projectinfo['modpath'])

        # reset the testGen_cross_domain generator and then use our trained model to
        # make predictions on the data
        print("[INFO] evaluating network ...(testGen_cross_domain)")
        testGen_cross_domain.reset()
        predIdxs = self.model.predict_generator(testGen_cross_domain,
        	steps=(self.totalTest_cross_domain // self.BS+1),verbose=1)

        classes = list(np.argmax(predIdxs, axis=1))
        classes_scores = []
        for i in range(len(predIdxs)):
            classes_scores.append(float('%.2f'%(max(predIdxs[i]))))
        filenames = testGen_cross_domain.filenames
        result = []
        result.extend(result201_200)
        for f in zip(filenames, classes, classes_scores):
            cellpath = os.path.join(self.project_resize_predict_dir, f[0])
            #FIXME: mala这个模型暂时按照预测阴性/阳性来显示结果
            predict_label = 51 #阳性
            if int(f[1]) == 1:
                predict_label = 50
            _, shotname, extension = get_filePath_fileName_fileExt(cellpath)
            imgid, x1, y1, x2, y2 = parse_imgid_xy_from_cellname(shotname)

            result.append([cellpath, predict_label, predict_label, f[2], 1, x1, y1, x2, y2, imgid])
        _df_result = pd.DataFrame(result, columns=['cellpath', 'true_label', 'predict_label', 'score', 'correct', 'x1', 'y1', 'x2', 'y2', 'imgid'])
        return True, _df_result

    def predict(self):
        remove_cnt_201, remove_cnt_200 = 0, 0

        #拷贝细胞图，并且返回不是细胞的list
        ret, result201 = self.mkdatasets()
        if ret is False:
            return False
        remove_cnt_201 = len(result201)
        self.log.info("根据像素尺寸删除不是细胞的图片总数%d" % len(result201))

        #删除不是细胞的图片
        ret, result201_200 = self._filter(result201)
        if ret is False:
            return False

        remove_cnt_200 = len(result201_200) - remove_cnt_201
        self.log.info("删除(%s) 的个数　%d" % ( "200", remove_cnt_200 ))

        #预测
        ret, df = self._predict(result201_200, remove_cnt_201, remove_cnt_200)
        if ret is False:
            return False
        self.log.info("预测结束开始统计预测结果")

        #预测结果统计
        ret = self.result_predict(df)
        if ret is False:
            return False

        return True

def worker_load(w):
    w_str = "训练" if w.wtype == wt.TRAIN.value else "预测"

    wid, wdir = w.get_job()
    if wdir == None:
        return
    w.log.info("获得一个%s任务%d 工作目录%s" % (w_str, wid, wdir))

    ret = True
    try:
        w.prepare(wid, wdir, w.wtype, w.mtype)
        w.log.info("初始化%s文件目录完成" % w_str)

        w.projectinfo = w.load_info_json()
        w.log.info("读取%s信息完成" % w_str)

        w.log.info("开始%s" % w_str)
        w.woker_percent(4, 60)
        if w.wtype == wt.TRAIN.value:
            ret = w.train()
        elif w.wtype == wt.PREDICT.value:
            ret = w.predict()
    except Exception as ex:
        w.log.error(str(ex))
        ret = False
    if ret == True:
        w.done()
        w.log.info("%s完成 %d 工作目录%s" % (w_str, wid, wdir))
    else:
        w.error()
        w.log.warning("%s出错 %d 工作目录%s" % (w_str, wid, wdir))
    return

if __name__ == '__main__':
    w = mala_predict(wt.PREDICT.value)
    while 1:
        worker_load(w)
        time.sleep(10)
