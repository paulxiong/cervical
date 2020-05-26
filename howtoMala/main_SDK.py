#!/usr/bin/env python
# coding: utf-8
import time, os, shutil, cv2, json
import pandas as pd
import numpy as np
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
from sklearn.metrics import classification_report
#from keras.utils.vis_utils import plot_model
from SDK.worker import worker
from SDK.const.const import wt, mt
from SDK.utilslib.fileops import parse_imgid_xy_from_cellname, get_file_lists
import keras.backend.tensorflow_backend as KTF
from filter_end.filter_end import main_filter_end
from filter_end.predict import yolo_init
import filter_end.test_cell_seg2 as mala2

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
        #totalTest_cross_domain = len(list(paths.list_images(config.TEST_PATH_CROSS_DOMAIN)))
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

    def _copy_train_cells(self, X, y, outdir):
        newX, newy = [], []
        total = len(X)
        for i in range(total):
            if i % 10000 == 0:
                self.log.info("%d/%d 拷贝要用来预测的文件" % (i, total))
            cellpath_src, celltype = X[i], int(y[i])
            cells_type_dir = os.path.join(outdir, str(celltype))
            if not os.path.exists(cells_type_dir):
                os.makedirs(cells_type_dir)
            if not os.path.exists(cellpath_src):
                self.log.info("拷贝文件时文件缺失：%s" % cellpath_src)
                continue
            _, shotname, extension = get_filePath_fileName_fileExt(cellpath_src)
            cellpath_dst = os.path.join(cells_type_dir, shotname + extension)
            ret = shutil.copyfile(cellpath_src, cellpath_dst)
            if ret == "" or not os.path.exists(ret):
                self.log.info("拷贝文件失败：%s" % cellpath_src)

            newX.append(cellpath_dst)
            newy.append(int(celltype))
        return newX, newy

    def copy_train_cells(self, df, test_size=0.2):
        X, y = [], []
        #拷贝训练数据到训练目录
        for index, imginfo in df.iterrows():
            cellpath_src = imginfo['cellpath']
            X.append(cellpath_src)
            y.append(int(imginfo['celltype']))

        if self.wtype == wt.PREDICT.value:
            newX, newy = self._copy_train_cells(X, y, self.project_predict_dir)
            return newX, None, newy, None
        elif self.wtype == wt.TRAIN.value:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
            newX_train, newy_train = self._copy_train_cells(X_train, y_train, self.project_train_dir)
            newX_test, newy_test = self._copy_train_cells(X_test, y_test, self.project_test_dir)
            return newX_train, newX_test, newy_train, newy_test
        return None, None, None, None

    def resize_img(self, X, y, outdir, outcsvpath, RESIZE=100):
        result201 = []
        filelist = []
        for i in range(len(X)):
            cellpath, celltype = X[i], int(y[i])
            #201表示细胞尺寸太小已经排除删除了
            if celltype == 201:
                _, shotname, extension = get_filePath_fileName_fileExt(cellpath)
                imgid, x1, y1, x2, y2 = parse_imgid_xy_from_cellname(shotname)
                result201.append([cellpath, celltype, celltype, 1.0, 1, x1, y1, x2, y2, imgid])
                continue

            cellto_dir = os.path.join(outdir, str(celltype))
            if not os.path.exists(cellto_dir):
                os.makedirs(cellto_dir)
            if not os.path.exists(cellpath):
                self.log.info("image not found %s" % cellpath)
                continue
            img = cv2.imread(cellpath)
            if img is None:
                self.log.info("invalid image file %s" % cellpath)
                continue
            if img.shape[0] != img.shape[1]:
                self.log.info("skip this image w != h: %s" % cellpath)
                continue
            if img.shape[0] != RESIZE:
                img = cv2.resize(img, (RESIZE, RESIZE), interpolation=cv2.INTER_LINEAR)

            filepath, shotname, extension = get_filePath_fileName_fileExt(cellpath)
            cv2.imwrite(os.path.join(cellto_dir, shotname + extension), img)

            filelist.append([os.path.join(str(celltype), shotname + extension), celltype])

        if len(filelist) > 0:
            df = pd.DataFrame(filelist, columns=['File Name', 'Label'])
            df.to_csv(outcsvpath, quoting = 1, mode = 'w', index = False, header = True)
        return True, result201

    def mkdatasets(self):
        size = self.projectinfo['parameter_resize']
        #获得所选数据集的细胞列表信息
        df = self.get_all_cells_list()

        #获取预测数据信息，输出到前端log
        temp_np = np.array(df['celltype'])
        key = np.unique(temp_np)
        result = {}
        for k in key:
            mask = (temp_np == k)
            temp_np_new = temp_np[mask]
            v = temp_np_new.size
            result[k] = v
        self.log.info("预测数据信息：%s"%result)

        if df is None or df.shape[0] < 1:
            return False, []

        #组织预测的目录结构
        if self.wtype == wt.PREDICT.value:
            #设置预测个数
            self.BS = 128
            self.totalTest_cross_domain = df.shape[0]

            X_predict, _, y_predict, _ = self.copy_train_cells(df)
            _, result201 = self.resize_img(X_predict, y_predict, self.project_resize_predict_dir, self.project_predict_labels_csv, RESIZE=size)
            return True, result201
        elif self.wtype == wt.TRAIN.value:
            X_train, X_test, y_train, y_test = self.copy_train_cells(df)
            #resize
            self.resize_img(X_train, y_train, self.project_resize_train_dir, self.project_train_labels_csv, RESIZE=size)
            self.resize_img(X_test, y_test, self.project_resize_test_dir, self.project_test_labels_csv, RESIZE=size)
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

        if predict_info['parameter_type'] == 0:
            self.log.info("统计:图片直接检测并切割出细胞")
        elif predict_info['parameter_type'] == 1:
            self.log.info("统计:按照标注csv切割细胞")

        #计算每个类别的recall/precision/f1，输出到前端log
        true_label = np.array(df["true_label"])
        predict_label = np.array(df["predict_label"])
        key = np.unique(true_label)
        self.log.info("统计:recall/precision/f1")
        self.log.info('\n%s'%classification_report(true_label, predict_label, key))

        result = {"result": [], "crop_cells": []}

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

        # initialize the testing generator for cross domain
        valAug = ImageDataGenerator(rescale=1 / 255.0)
        testGen_cross_domain = valAug.flow_from_directory(
            self.project_resize_predict_dir,
            class_mode="categorical",
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

    def _filter_yolo(self, result201):
        cfg, metadata = "yolov3/yolov3-voc-predict.cfg", "yolov3/voc.data"
        weights = "yolov3/yolov3-voc.backup"

        if self.filtermodyolo != weights or self.yolo_net is None:
            self.filtermodyolo = weights
            self.yolo_net, self.yolo_meta = yolo_init(cfg, weights, metadata)

        result = []
        result.extend(result201)
        files = get_file_lists(self.project_resize_predict_dir)
        for f in files:
            cellpath = f
            predict_label = 100 #100未知细胞类型 200不是细胞
            r = detect(self.yolo_net, self.yolo_meta, f.encode('utf-8'), thresh=0.5, hier_thresh=0.5, nms=0.45)
            dic = {"boxes": []}
            for i in range(len(r)):
                classname = str(r[i][0])
                x1, y1 = int(r[i][2][0]-r[i][2][2]/2), int(r[i][2][1]-r[i][2][3]/2)
                x2, y2 = int(r[i][2][0]+r[i][2][2]/2), int(r[i][2][1]+r[i][2][3]/2)
                w, h, score, classname = x2 - x1, y2 - y1, round(r[i][1], 2), str(r[i][0], encoding = "utf-8")
                dic["boxes"].append({"class": classname, "score": score, "w": w, "h": h, "x1": x1, "y1": y1, "x2": x2, "y2": y2})
            dic["boxes"] = _filter3(dic["boxes"])
            invalid = _filter2(dic["boxes"])
            arr = cellpath.split('/', -1)
            if invalid is True:
                predict_label = 200
                os.remove(cellpath)
                cellpath = os.path.join(self.project_predict_dir, arr[len(arr) - 2], arr[len(arr) - 1])

            #已经按尺寸滤掉了,201
            if arr[len(arr) - 2] == "201":
                predict_label = 201
            _, shotname, extension = get_filePath_fileName_fileExt(cellpath)
            imgid, x1, y1, x2, y2 = parse_imgid_xy_from_cellname(shotname)

            result.append([cellpath, predict_label, predict_label, 1, 1, x1, y1, x2, y2, imgid])

        df_result = pd.DataFrame(result, columns=['cellpath', 'true_label', 'predict_label', 'score', 'correct', 'x1', 'y1', 'x2', 'y2', 'imgid'])
        return True, df_result

    def _predict(self, result201_200, remove_cnt_201, remove_cnt_200):
        self.projectinfo['parameter_resize'] = 64 #模型只支持64x64
        #设置预测个数
        self.BS = 128

        # initialize the testing generator for cross domain
        valAug = ImageDataGenerator(rescale=1 / 255.0)
        testGen_cross_domain = valAug.flow_from_directory(
                self.project_resize_predict_dir,
        	class_mode="categorical",
        	target_size=(64, 64),
        	color_mode="rgb",
        	shuffle=False,
        	batch_size=self.BS)
        self.totalTest_cross_domain = len(testGen_cross_domain.filenames)

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

        # 加入yolo过滤及最终mala模型过滤
        cfg2, metadata2 = "filter_end/names-data/yolov3-voc-predict.cfg", "filter_end/names-data/voc.data"
        weights2 = "filter_end/yolov3-voc_40100.weights.0501.concat"

        if self.filtermodyolo2 != weights2 or self.yolo_net2 is None:
            self.filtermodyolo2 = weights2
            self.yolo_net2, self.yolo_meta2 = yolo_init(cfg2, weights2, metadata2)

        #filter_mod90_file='filter_end/Mala_H_fillter_0501_2.h5'
        filter_mod90_file='filter_end/Mala_H_fillter_0520.h5'
        if self.filtermod90 != filter_mod90_file  or self.filter_model90 is None:
            self.filtermod90 = filter_mod90_file
            print(os.path.exists(self.filtermod90))
            self.filter_model90 = load_model(self.filtermod90)
            print(self.filter_model90)

        df_result = main_filter_end(_df_result, self.filter_model90, self.yolo_net2, self.yolo_meta2)
        return True, df_result

    def predict(self):
        remove_cnt_201, remove_cnt_200 = 0, 0

        #拷贝细胞图，并且返回不是细胞的list
        ret, result201 = self.mkdatasets()
        if ret is False:
            return False
        remove_cnt_201 = len(result201)
        self.log.info("根据像素尺寸删除不是细胞的图片总数%d" % len(result201))

        #删除不是细胞的图片
        #ret, df = self._filter_yolo(result201)
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
