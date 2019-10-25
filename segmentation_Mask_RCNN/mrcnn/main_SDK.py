import os, time, cv2
import pandas as pd
from SDK.worker import worker

#xy坐标转x1, y1, x2, y2
def xy_x1y1x2y2(x, y, w):
    slide = int(w/2)
    x1, y1, x2, y2 = (x-slide), (y-slide), (x+slide), (y+slide)
    x1 = x1 if x1>0 else 0
    y1 = y1 if y1>0 else 0
    x2 = x2 if x2>0 else 0
    y2 = y2 if y2>0 else 0
    return x1, y1, x2, y2

def make_square(x1, y1, x2, y2, maxx, maxy):
    _x1, _y1, _x2, _y2 = x1, y1, x2, y2
    if (_x2 - _x1) == (_y2 - _y1):
        return _x1, _y1, _x2, _y2
    #先生成正方形坐标
    delta = (_x2 - _x1) - (_y2 - _y1)
    if delta > 0:
        _y2 = _y2 + delta
    elif delta < 0:
        _x2 = _x2 - delta
    #判断越界
    if _x2 > maxx:
        delta = _x2 - maxx
        _x1, _x2 = _x1 - delta, _x2 -delta
    if _y2 > maxy:
        delta = _y2 - maxy
        _y1, _y2 = _y1 - delta, _y2 - delta
    return _x1, _y1, _x2, _y2

class cells_detect_crop(worker):
    def __init__(self, wtype):
        worker.__init__(self, wtype)
        self.log.info("初始化一个数据预处理的worker")

    def cell_name(self, imginfo, x1, y1, x2, y2, celltype):
        batchid, medicalid, imgname = str(imginfo['batchid']), str(imginfo['medicalid']), str(imginfo['imgname'])
        cellname = "{}.{}.{}_{}_{}_{}_{}_{}_{}_{}_{}_{}.png".format(
            batchid, medicalid, imgname,
            str(self.datasetinfo["parameter_gray"]),
            str(self.datasetinfo["parameter_size"]),
            str(self.datasetinfo["parameter_type"]),
            str(self.datasetinfo["parameter_mid"]),
            x1, y1, x2, y2, celltype)
        return cellname

    def get_cells_info(self, imginfo, cellsinfo):
        """
        细胞信息, 存成csv，方便后面抠图和统计细胞信息
        """
        columns = ['batchid', 'medicalid', 'imgname', 'p1n0', 'parameter_gray',
                   'parameter_size', 'parameter_type', 'parameter_mid', 'parameter_cache',
                   'cellpath', 'x1', 'y1', 'x2', 'y2', 'celltype', 'cached']
        cellsinfo2 = []
        for c in cellsinfo:
            x1, y1, x2, y2, celltype = int(c[0]), int(c[1]), int(c[2]), int(c[3]), int(c[4])
            x1, y1, x2, y2 = make_square(x1, y1, x2, y2, int(imginfo['w']), int(imginfo['h']))

            _cell_name = self.cell_name(imginfo, x1, y1, x2, y2, celltype)
            cellpath = os.path.join(self.scratch_dir, str(imginfo['batchid']), str(imginfo['medicalid']), 'cells', _cell_name)
            if (x2 - x1) != (y2 - y1):
                self.log.info("not square!")

            _cellsinfo2 = []
            _cellsinfo2.append(str(imginfo['batchid']))
            _cellsinfo2.append(str(imginfo['medicalid']))
            _cellsinfo2.append(str(imginfo['imgname']))
            _cellsinfo2.append(str(imginfo['p1n0']))
            _cellsinfo2.append(int(self.datasetinfo['parameter_gray']))
            _cellsinfo2.append(int(self.datasetinfo['parameter_size']))
            _cellsinfo2.append(int(self.datasetinfo['parameter_type']))
            _cellsinfo2.append(int(self.datasetinfo['parameter_mid']))
            _cellsinfo2.append(int(self.datasetinfo['parameter_cache']))
            _cellsinfo2.append(cellpath)
            _cellsinfo2.append(int(x1))
            _cellsinfo2.append(int(y1))
            _cellsinfo2.append(int(x2))
            _cellsinfo2.append(int(y2))
            _cellsinfo2.append(int(celltype))

            #判断当前细胞图是不是已经在缓存目录里面
            cached = 0
            if os.path.exists(cellpath):
                cached = 1
            _cellsinfo2.append(cached)

            cellsinfo2.append(_cellsinfo2)
        df = pd.DataFrame(cellsinfo2, columns=columns)
        return df

    def get_cells_posation(self, imginfo):
        cellsinfo = []
        if self.datasetinfo['parameter_type'] == 1:
            csvpath = os.path.join(w.csv_dir, str(imginfo['csvpath']))
            if not os.path.exists(csvpath):
                self.log.info("not found csv: %s" % csvpath)
                return cellsinfo, False
            df_cells = pd.read_csv(csvpath)
            for index2, labelinfo in df_cells.iterrows():
                #单个细胞的标注
                size = 100
                if self.datasetinfo['parameter_size'] > 0:
                    size = self.datasetinfo['parameter_size']
                x1, y1, x2, y2 = xy_x1y1x2y2(int(labelinfo['X']), int(labelinfo['Y']), size)
                cellsinfo.append([x1, y1, x2, y2, int(labelinfo['Type'])])
            return cellsinfo, True
        return True

    def load_image(self, image_path):
        image, w, h, channels = None, 0, 0, 0
        if not os.path.exists(image_path):
            self.log.error("not found %s" % image_path)
            return image, w, h, channels
        image = cv2.imread(image_path)
        if image is None:
            return image, w, h, channels
        w, h, channels = image.shape[0], image.shape[1], image.shape[2]
        return image, w, h, channels

    def crop_images(self):
        """
        裁剪方式：
            0 图片直接检测并切割出细胞
            1 按照标注csv切割细胞
        步骤：
            loop 取出单个图片 {
                定位
                细胞信息生成
                抠图
            }
        """
        df_allcells = None
        df_imgs = pd.read_csv(self.dataset_lists)
        for index, imginfo in df_imgs.iterrows():
            self.log.info("step %d / %d" % (index, df_imgs.shape[0] -1))

            #向服务器报告任务进度,这里占95%
            self.woker_percent(int(95 * (index + 1) / (df_imgs.shape[0] -1)))

            #创建缓存切割细胞的目录
            cache_dir = os.path.join(self.scratch_dir, str(imginfo['batchid']), str(imginfo['medicalid']), 'cells')
            if not os.path.exists(cache_dir):
                os.makedirs(cache_dir)

            #读取原图
            image_path = os.path.join(self.img_dir, imginfo['imgpath'])
            image, imginfo['w'], imginfo['h'], imginfo['channels'] = self.load_image(image_path)

            #获得一张图片里面所有细胞坐标，如果有医生标注直接从csv读取，没有的用maskrcnn定位
            cellsinfo, ret = self.get_cells_posation(imginfo)

            #把细胞的所有详细信息记录到csv, 坐标超出图片的要做处理
            df_cells = self.get_cells_info(imginfo, cellsinfo)
            if df_allcells is None:
                df_allcells = df_cells
            else:
                df_allcells = df_allcells.append(df_cells)

            #细胞信息裁剪出细胞图
            for index2, cellinfo in df_cells.iterrows():
                x1, y1, x2, y2, cellpath = int(cellinfo['x1']), int(cellinfo['y1']), int(cellinfo['x2']), \
                                           int(cellinfo['y2']), str(cellinfo['cellpath'])
                #如果使用缓存，并且缓存存在，跳过裁剪
                if os.path.exists(cellpath) and self.datasetinfo['parameter_cache'] == 1:
                    self.log.info("use cache of %s" % cellpath)
                    continue
                cell_img = image[y1:y2, x1:x2]
                cv2.imwrite(cellpath, cell_img)

        #保存所有细胞的信息到文件
        if df_allcells is not None:
            df_allcells.to_csv(self.dataset_cellslists, quoting = 1, mode = 'w', index = False, header = True)

        return True

if __name__ == '__main__':
    w = cells_detect_crop(1)
    while 1:
        wid, wdir = w.get_job()
        if wdir == None:
            exit()
            time.sleep(5)
            continue
        w.log.info("获得一个数据集预处理任务%d 工作目录%s" % (wid, wdir))

        w.prepare(wid, wdir, 1)
        w.log.info("初始化文件目录完成")

        w.datasetinfo = w.load_info_json()
        w.log.info("读取数据集信息完成")

        w.log.info("开始数据预处理")
        w.woker_percent(4)
        ret = w.crop_images()

        if ret == True:
            w.done()
            w.log.info("数据集预处理完成 %d 工作目录%s" % (wid, wdir))
        else:
            w.error()
            w.log.info("数据集预处理出错 %d 工作目录%s" % (wid, wdir))
        exit()
