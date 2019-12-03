import os, time, cv2
import pandas as pd
from SDK.worker import worker
from SDK.const.const import wt, mt
from SDK.utilslib.fileops import getcellname
from config import Config
import model as modellib

#Mask-Rcnn的配置, 从源码拷贝过来的
class BowlConfig(Config):
    """Configuration for training on the toy shapes dataset.
    Derives from the base Config class and overrides values specific
    to the toy shapes dataset.
    """
    # Give the configuration a recognizable name
    NAME = "Inference"

    IMAGE_RESIZE_MODE = "pad64" ## tried to modfied but I am using other git clone
    ## No augmentation
    ZOOM = False
    ASPECT_RATIO = 1
    MIN_ENLARGE = 1
    IMAGE_MIN_SCALE = False ## Not using this

    IMAGE_MIN_DIM = 512 # We scale small images up so that smallest side is 512
    IMAGE_MAX_DIM = False

    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

    DETECTION_MAX_INSTANCES = 512
    DETECTION_NMS_THRESHOLD =  0.2
    DETECTION_MIN_CONFIDENCE = 0.9

    LEARNING_RATE = 0.001

    # Number of classes (including background)
    NUM_CLASSES = 1 + 1 # background + nuclei

    # Use smaller anchors because our image and objects are small
    RPN_ANCHOR_SCALES = (8 , 16, 32, 64, 128)  # anchor side in pixels

    # Reduce training ROIs per image because the images are small and have
    # few objects. Aim to allow ROI sampling to pick 33% positive ROIs.
    TRAIN_ROIS_PER_IMAGE = 600

    USE_MINI_MASK = True

class cells_detector():
    def __init__(self, model_path, wdir, debug=False):
        self.model_path = model_path
        self.wdir = wdir
        self.debug = debug
        self.inference_config = None
        if not os.path.exists(self.model_path):
            raise RuntimeError("not found: %s" % model_path)
        self.model = self.detector_init()

    def detector_init(self):
        logs_dir = os.path.join(self.wdir, 'logs')
        self.inference_config = BowlConfig()
        if self.debug is True:
            self.inference_config.display()

        print("Loading weights from ", self.model_path)
        model = modellib.MaskRCNN(mode = "inference",
                    config = self.inference_config, model_dir = logs_dir)
        model.load_weights(self.model_path, by_name = True)
        return model

    # 从一张原图定位出细胞的坐标
    def detect_image(self, image, gray=True, size=100):
        celltype = 100 #100表示类型未知
        predict_img = image
        if gray is True:
            grayImage = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            predict_img = grayImage

        if len(predict_img.shape)<3:
            predict_img = img_as_ubyte(predict_img)
            predict_img = np.expand_dims(predict_img, 2)
            predict_img = predict_img[:, :, [0, 0, 0]] # flip r and b
        predict_img = predict_img[:, :, :3]

        ## Make prediction for that image
        results = self.model.detect([predict_img], verbose=0)
        r = results[0]
        scores_masks = r['scores']      #判别物得分
        final_rois = r["rois"]         #交并比得到的回归框坐标
        pred_masks = r['masks']

        _rois = []
        threshold = float(0.90)
        for i in range(0, len(scores_masks)):
            score = scores_masks[i]
            classid = r['class_ids'][i]
            roi = final_rois[i]
            if int(threshold*100) > int(score*100):
                print("%s drop roi, score=%f" % (filename, score))
                continue
            y1, x1, y2, x2 = int(roi[0]), int(roi[1]), int(roi[2]), int(roi[3])
            #FIXME:细胞尺寸过滤
            if (x2 - x1) <= 17 or  (y2 - y1) <= 17:
                celltype = 201 #201表示不是细胞(尺寸太小)

            x1, y1, x2, y2 = xy_x1y1x2y2((x2 + x1) / 2, (y2 + y1) / 2, size)
            _rois.append([x1, y1, x2, y2, celltype])
        return _rois

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
    if (_x2 - _x1) == (_y2 - _y1) and _x2 < maxx and _y2 < maxy:
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

# 裁剪原图为细胞图，主要函数是crop_images，其他函数是被这个函数调用
class cells_detect_crop(worker):
    def __init__(self):
        #初始化一个dataset的worker
        worker.__init__(self, wt.DATA.value)

        self.model_path = ""
        self.detector =  None
        self.log.info("初始化一个数据预处理的worker")
        self.mtype = mt.MASKRCNN.value

    def cell_name(self, imginfo, x1, y1, x2, y2, celltype):
        batchid, medicalid, imgname, imgid = str(imginfo['batchid']), str(imginfo['medicalid']), str(imginfo['imgname']), int(imginfo['imgid'])
        cellname = getcellname(
            batchid, medicalid, imgid, imgname,
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
        columns = ['batchid', 'medicalid', 'imgid', 'imgname', 'imgpath', 'p1n0', 'parameter_gray',
                   'parameter_size', 'parameter_type', 'parameter_mid', 'parameter_cache',
                   'cellpath', 'x1', 'y1', 'x2', 'y2', 'celltype']
        cellsinfo2 = []
        for c in cellsinfo:
            x1, y1, x2, y2, celltype = int(c[0]), int(c[1]), int(c[2]), int(c[3]), int(c[4])
            x1, y1, x2, y2 = make_square(x1, y1, x2, y2, int(imginfo['w']), int(imginfo['h']))

            _cell_name = self.cell_name(imginfo, x1, y1, x2, y2, celltype)
            cellpath = os.path.join(self.scratch_dir, str(imginfo['batchid']), str(imginfo['medicalid']), 'cells', _cell_name)
            if (x2 - x1) != (y2 - y1):
                self.log.info("not square!")

            image_path = os.path.join(self.rootdir, imginfo['imgpath'])

            _cellsinfo2 = []
            _cellsinfo2.append(str(imginfo['batchid']))
            _cellsinfo2.append(str(imginfo['medicalid']))
            _cellsinfo2.append(str(imginfo['imgname']))
            _cellsinfo2.append(imginfo['imgid'])
            _cellsinfo2.append(image_path)
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

            cellsinfo2.append(_cellsinfo2)
        df = pd.DataFrame(cellsinfo2, columns=columns)
        return df

    def get_cells_posation(self, imginfo, image):
        cellsinfo = []
        size = 100
        if self.datasetinfo['parameter_size'] > 0:
            size = self.datasetinfo['parameter_size']

        if self.datasetinfo['parameter_type'] == 0:
            gray = 1 if self.datasetinfo['parameter_gray'] ==0 else 0
            cellsinfo = self.detector.detect_image(image, gray=gray, size=size)
        elif self.datasetinfo['parameter_type'] == 1:
            csvpath = os.path.join(self.rootdir, str(imginfo['csvpath']))
            if not os.path.exists(csvpath):
                self.log.info("not found csv: %s" % csvpath)
                return cellsinfo, False
            df_cells = pd.read_csv(csvpath)
            for index2, labelinfo in df_cells.iterrows():
                #单个细胞的标注
                x1, y1, x2, y2 = xy_x1y1x2y2(int(labelinfo['X']), int(labelinfo['Y']), size)
                cellsinfo.append([x1, y1, x2, y2, int(labelinfo['Type'])])
            return cellsinfo, True
        return cellsinfo, True

    def load_image(self, image_path):
        image, w, h, channels = None, 0, 0, 0
        if not os.path.exists(image_path):
            self.log.error("not found %s" % image_path)
            return image, w, h, channels
        image = cv2.imread(image_path)
        if image is None:
            return image, w, h, channels
        h, w, channels = image.shape[0], image.shape[1], image.shape[2]
        return image, w, h, channels

    #从细胞列表csv文件取出原图/细胞图的集合，是相对路径
    def get_image_list_from_csv(self, df, columename, rootdir):
        imgs = []
        for imgpath, df1 in df.groupby([columename]):
            imgpath2 = imgpath[len(rootdir):]
            imgs.append(imgpath2)
        return imgs

    #裁剪完之后统计信息
    def update_info_json(self, df):
        job_info = self.load_info_json()
        job_info['origin_imgs']       = self.get_image_list_from_csv(df, 'imgpath', self.rootdir)
        job_info['cells_crop']        = self.get_image_list_from_csv(df, 'cellpath', self.rootdir)
        job_info['status'] = self.status

        #统计医生标注的信息
        df = pd.read_csv(self.dataset_cellslists)
        job_info['batchcnt']   = df.groupby(['batchid']).size().shape[0] #总的批次数
        job_info['medicalcnt'] = df.groupby(['medicalid']).size().shape[0] #总的病例数
        job_info['fovcnt']     = df.groupby(['imgpath']).size().shape[0] #总的图片数
        job_info['fovncnt']    = df[df.p1n0.isin(['0'])].groupby(['imgpath']).size().shape[0] #FOVN的个数
        job_info['fovpcnt']    = df[df.p1n0.isin(['1'])].groupby(['imgpath']).size().shape[0] #FOVP的个数
        #job_info['labelncnt']  = df[df.cellpn.isin(['N'])].shape[0] #n的标注次数
        #job_info['labelpcnt']  = df[df.cellpn.isin(['P'])].shape[0] #p的标注次数
        job_info['labelcnt']   = df.shape[0] #总的标注次数
        types = [] #各个type标注次数
        for celltype, df1 in df.groupby(['celltype']):
            onetype = {'celltype': celltype, 'labelcnt': df1.shape[0]}
            types.append(onetype)
        job_info['types'] = types

        self.save_info_json(job_info, self.info2_json)

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
            统计信息
        """
        #细胞定位时候才需要，如果按照标注裁剪不需要
        if self.datasetinfo['parameter_type'] == 0:
            self.log.info("方式：图片直接送检测并切割出细胞")
            model_path = os.path.join(self.modules_dir, self.datasetinfo['modpath'])
            if self.model_path != model_path or self.detector is None:
                self.model_path = model_path
                self.detector =  cells_detector(model_path, self.wdir, self.debug)
        elif self.datasetinfo['parameter_type'] == 1:
            self.log.info("方式：按照标注切割出细胞")

        df_allcells = None
        df_imgs = pd.read_csv(self.dataset_lists)
        ts1 = int(time.time()*1000)
        for index, imginfo in df_imgs.iterrows():
            ts2 = int(time.time()*1000)
            needtime = df_imgs.shape[0] #假设每张图片1秒
            if index > 0:
                needtime = (ts2 - ts1) * (df_imgs.shape[0] - index)
                self.log.info("step %d / %d 预计还需要 %d秒" % (index, df_imgs.shape[0] -1, needtime/1000))
            else:
                self.log.info("step %d / %d" % (index, df_imgs.shape[0] -1))
            ts1 = ts2

            #向服务器报告任务进度,这里占95%
            if df_imgs.shape[0] > 1:
                self.woker_percent(int(95 * (index + 1) / (df_imgs.shape[0] -1)), needtime/1000)

            #创建缓存切割细胞的目录
            cache_dir = os.path.join(self.scratch_dir, str(imginfo['batchid']), str(imginfo['medicalid']), 'cells')
            if not os.path.exists(cache_dir):
                os.makedirs(cache_dir)

            #读取原图
            image_path = os.path.join(self.rootdir, imginfo['imgpath'])
            image, imginfo['w'], imginfo['h'], imginfo['channels'] = self.load_image(image_path)

            #获得一张图片里面所有细胞坐标，如果有医生标注直接从csv读取，没有的用maskrcnn定位
            cellsinfo, ret = self.get_cells_posation(imginfo, image)

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
                    if self.debug:
                        self.log.info("use cache of %s" % cellpath)
                    continue
                cell_img = image[y1:y2, x1:x2]
                cv2.imwrite(cellpath, cell_img)
                if cell_img.shape[0] != cell_img.shape[1]:
                    self.log.info("not square ! %d %d %s" % (cell_img.shape[0], cell_img.shape[1], cellpath))

        #保存所有细胞的信息到文件
        if df_allcells is not None:
            df_allcells.to_csv(self.dataset_cellslists, quoting = 1, mode = 'w', index = False, header = True)


        self.update_info_json(df_allcells)

        return True
