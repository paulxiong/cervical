import time, os, shutil
import pandas as pd
from SDK.worker import worker
from SDK.const.const import wt
from sklearn.model_selection import train_test_split

#传入文件的路径，返回路径，文件名字，文件后缀
def get_filePath_fileName_fileExt(filename):
    (filepath, tempfilename) = os.path.split(filename)
    (shotname, extension) = os.path.splitext(tempfilename)
    return filepath, shotname, extension

class cells_train(worker):
    def __init__(self):
        #初始化一个dataset的worker
        worker.__init__(self, wt.TRAIN.value)
        self.log.info("初始化一个训练的worker")

    def get_train_cells_list(self):
        #获得需要训练的分类
        types = self.projectinfo['types']
        if len(types) < 2 and self.wtype == wt.TRAIN.value:
            self.log.error("less then 2 labels to train")
            return None
        #获得所有用作训练的细胞的信息
        df_traincells = None
        df_cells = pd.read_csv(self.cellslist_csv)
        for celltype in types:
            df2 = df_cells[df_cells['celltype'] == celltype]
            if df_traincells is None:
                df_traincells = df2
            else:
                df_traincells = df_traincells.append(df2)
        return df_traincells

    def _copy_train_cells(self, X, y, dirname):
        for i in range(len(X)):
            cellpath_src, celltype = X[i], y[i]
            cells_type_dir = os.path.join(self.project_dir, dirname, str(celltype))
            if not os.path.exists(cells_type_dir):
                os.makedirs(cells_type_dir)
            if not os.path.exists(cellpath_src):
                continue
            _, shotname, extension = get_filePath_fileName_fileExt(cellpath_src)
            cellpath_dst = os.path.join(cells_type_dir, shotname + extension)
            shutil.copyfile(cellpath_src, cellpath_dst)
        return

    def copy_train_cells(self, df, test_size=0.2):
        X, y = [], []
        #拷贝训练数据到训练目录
        for index, imginfo in df.iterrows():
            cellpath_src = imginfo['cellpath']
            X.append(cellpath_src)
            y.append(str(imginfo['celltype']))

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        self._copy_train_cells(X_train, y_train, 'train')
        self._copy_train_cells(X_test, y_test, 'test')

        print(len(X_train), len(X_test))
        return True

    def mkdatasets(self):
        """
        步骤：
            获得所选数据集的细胞列表信息
            组织训练的目录结构
            resize
        """
        df = self.get_train_cells_list()
        self.copy_train_cells(df)

        print(self.project_train_dir)
        return

    def train(self):
        self.mkdatasets()

        for i in range(100):
            #向服务器端报告任务进度
            self.woker_percent(int(95 * i / 100), (100 - i) * 4)

            #do something
            time.sleep(1)
            return False
        return True

if __name__ == '__main__':
    w = cells_train()
    while 1:
        wid, wdir = w.get_job()
        if wdir == None:
            exit()
            time.sleep(5)
            continue
        w.log.info("获得一个训练任务%d 工作目录%s" % (wid, wdir))

        w.prepare(wid, wdir, wt.TRAIN.value)
        w.log.info("初始化文件目录完成")

        w.projectinfo = w.load_info_json()
        w.log.info("读取训练信息完成")

        w.log.info("开始训练")
        w.woker_percent(4, 0)
        ret = w.train()

        if ret == True:
            w.done()
            w.log.info("训练完成 %d 工作目录%s" % (wid, wdir))
        else:
            w.error()
            w.log.info("训练出错 %d 工作目录%s" % (wid, wdir))
        exit()
