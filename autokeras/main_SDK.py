import time, os, shutil, cv2, json
import pandas as pd
import numpy as np
from shutil import copyfile, rmtree
from SDK.worker import worker
from SDK.const.const import wt
from sklearn.model_selection import train_test_split
from autokeras.image.image_supervised import load_image_dataset, ImageClassifier
from autokeras.utils import pickle_from_file
from keras.preprocessing.image import load_img, img_to_array

#传入文件的路径，返回路径，文件名字，文件后缀
def get_filePath_fileName_fileExt(filename):
    (filepath, tempfilename) = os.path.split(filename)
    (shotname, extension) = os.path.splitext(tempfilename)
    return filepath, shotname, extension

class _cells_train(worker):
    def __init__(self, workertype):
        #初始化一个dataset的worker
        worker.__init__(self, workertype)
        self.log.info("初始化一个训练的worker")

    def get_all_cells_list(self):
        #获得需要训练的分类
        types = self.projectinfo['types']
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
        for i in range(len(X)):
            cellpath_src, celltype = X[i], y[i]
            cells_type_dir = os.path.join(outdir, str(celltype))
            if not os.path.exists(cells_type_dir):
                os.makedirs(cells_type_dir)
            if not os.path.exists(cellpath_src):
                continue
            _, shotname, extension = get_filePath_fileName_fileExt(cellpath_src)
            cellpath_dst = os.path.join(cells_type_dir, shotname + extension)
            shutil.copyfile(cellpath_src, cellpath_dst)
            newX.append(cellpath_dst)
            newy.append(str(celltype))
        return newX, newy

    def copy_train_cells(self, df, test_size=0.2):
        X, y = [], []
        #拷贝训练数据到训练目录
        for index, imginfo in df.iterrows():
            cellpath_src = imginfo['cellpath']
            X.append(cellpath_src)
            y.append(str(imginfo['celltype']))

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
        filelist = []
        for i in range(len(X)):
            cellpath, celltype = X[i], y[i]
            cellto_dir = os.path.join(outdir, celltype)
            if not os.path.exists(cellto_dir):
                os.makedirs(cellto_dir)
            img = cv2.imread(cellpath)
            if img.shape[0] != img.shape[1]:
                self.log.info("skip this image w != h: %s" % cellpath)
                continue
            img = cv2.resize(img, (RESIZE, RESIZE), interpolation=cv2.INTER_LINEAR)

            filepath, shotname, extension = get_filePath_fileName_fileExt(cellpath)
            cv2.imwrite(os.path.join(cellto_dir, shotname + extension), img)

            filelist.append([os.path.join(celltype, shotname + extension), celltype])

        if len(filelist) > 0:
            df = pd.DataFrame(filelist, columns=['File Name', 'Label'])
            df.to_csv(outcsvpath, quoting = 1, mode = 'w', index = False, header = True)
        return True

    def mkdatasets(self):
        size = self.projectinfo['parameter_resize']
        #获得所选数据集的细胞列表信息
        df = self.get_all_cells_list()
        if df is None or df.shape[0] < 1:
            return False
        #组织训练的目录结构
        if self.wtype == wt.PREDICT.value:
            X_predict, _, y_predict, _ = self.copy_train_cells(df)
            self.resize_img(X_predict, y_predict, self.project_resize_predict_dir, self.project_predict_labels_csv, RESIZE=size)
            return True
        elif self.wtype == wt.TRAIN.value:
            X_train, X_test, y_train, y_test = self.copy_train_cells(df)
            #resize
            self.resize_img(X_train, y_train, self.project_resize_train_dir, self.project_train_labels_csv, RESIZE=size)
            self.resize_img(X_test, y_test, self.project_resize_test_dir, self.project_test_labels_csv, RESIZE=size)
            return True

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

    def train_autokeras(self):
        time_limit = self.projectinfo['parameter_time']
        #Load images
        train_data, train_labels = load_image_dataset(csv_file_path=self.project_train_labels_csv,
                                                      images_path=self.project_resize_train_dir)
        test_data, test_labels = load_image_dataset(csv_file_path=self.project_test_labels_csv,
                                                    images_path=self.project_resize_test_dir)

        train_data = train_data.astype('float32') / 255
        test_data = test_data.astype('float32') / 255
        self.log.info("Train data shape: %d" % train_data.shape[0])

        clf = ImageClassifier(verbose=True, path=self.project_tmp_dir, resume=False)
        clf.fit(train_data, train_labels, time_limit=time_limit)
        clf.final_fit(train_data, train_labels, test_data, test_labels, retrain=True)

        evaluate_value = clf.evaluate(test_data, test_labels)
        self.log.info("Evaluate: %f" % evaluate_value)

        clf.export_autokeras_model(self.project_mod_path)

        #统计训练信息
        dic = {}
        ishape = clf.cnn.searcher.input_shape
        dic['n_train'] = train_data.shape[0]  #训练总共用了多少图
        dic['n_classes'] = clf.cnn.searcher.n_classes
        dic['input_shape'] = str(ishape[0]) + 'x' + str(ishape[1]) + 'x' + str(ishape[2])
        dic['history'] = clf.cnn.searcher.history
        dic['model_count'] = clf.cnn.searcher.model_count
        dic['best_model'] = clf.cnn.searcher.get_best_model_id()
        best_model = [item for item in dic['history'] if item['model_id'] == dic['best_model']]
        if len(best_model) > 0:
            dic['loss'] = best_model[0]['loss']
            dic['metric_value'] = best_model[0]['metric_value']
        dic['evaluate_value'] = evaluate_value
        return dic

    def train(self):
        ret = self.mkdatasets()
        if ret is False:
            return False
        self.woker_percent(10, 1800) #默认设置ETA为30分钟
        dic = self.train_autokeras()

        self.update_model_info_json(dic)

        return True

    def predict(self):
        ret = self.mkdatasets()
        if ret is False:
            return False
        model = pickle_from_file(self.projectinfo['modpath'])
        self.woker_percent(10, 1800) #默认设置ETA为30分钟

        result = []
        df_cells = pd.read_csv(self.project_predict_labels_csv)
        ts1 = int(time.time()*1000)
        for index, cellinfo in df_cells.iterrows():
            ts2 = int(time.time()*1000)
            needtime = (ts2 - ts1) * (df_cells.shape[0] - index)
            if index > 0:
                self.log.info("step %d / %d 预计还需要 %d秒" % (index, df_cells.shape[0] -1, needtime/1000))
            else:
                self.log.info("step %d / %d" % (index, df_cells.shape[0] -1))
            ts1 = ts2
            #向服务器报告任务进度,这里占90%
            self.woker_percent(int(90 * (index + 1) / (df_cells.shape[0] -1)), needtime/1000)

            celltype = str(cellinfo['Label'])
            cellpath = os.path.join(self.project_resize_predict_dir, cellinfo['File Name'])
            resize = self.projectinfo['parameter_resize']

            img = load_img(cellpath)
            x = img_to_array(img)
            x = x.astype('float32') / 255
            x = np.reshape(x, (1, resize, resize, 3))
            y = model.predict(x)
            correct = 1
            if celltype != str(y[0]):
                correct = 0
            result.append([cellpath, celltype, str(y[0]), correct])

        df_result = pd.DataFrame(result, columns=['cellpath', 'true_label', 'predict_label', 'correct'])
        return True

class cells_train(_cells_train):
    def __init__(self):
        _cells_train.__init__(self, wt.TRAIN.value)
        self.log.info("初始化一个训练的worker")

class cells_predict(_cells_train):
    def __init__(self):
        _cells_train.__init__(self, wt.PREDICT.value)
        self.log.info("初始化一个预测的worker")

def worker_load(w):
    w_str = "训练" if w.wtype == wt.TRAIN.value else "预测"

    wid, wdir = w.get_job()
    if wdir == None:
        return
    w.log.info("获得一个%s任务%d 工作目录%s" % (w_str, wid, wdir))

    ret = True
    try:
        w.prepare(wid, wdir, w.wtype)
        w.log.info("初始化%s文件目录完成" % w_str)

        w.projectinfo = w.load_info_json()
        w.log.info("读取%s信息完成" % w_str)

        w.log.info("开始%s" % w_str)
        w.woker_percent(4, 1800)
        if w.wtype == wt.TRAIN.value:
            ret = w.train()
        elif w.wtype == wt.PREDICT.value:
            ret = w.predict()
    except Exception as ex:
        w.log.info(str(ex))
        ret = False

    if ret == True:
        w.done()
        w.log.info("%s完成 %d 工作目录%s" % (w_str, wid, wdir))
    else:
        w.error()
        w.log.info("%s出错 %d 工作目录%s" % (w_str, wid, wdir))
    return

if __name__ == '__main__':
    tw = cells_train() #训练
    pw = cells_predict()

    while 1:
        #训练
        worker_load(tw)
        time.sleep(5)

        #预测
        worker_load(pw)
        time.sleep(5)


