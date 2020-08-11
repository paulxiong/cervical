# coding: utf-8
import os, time, cv2, math
import pandas as pd
from SDK.worker import worker
from SDK.const.const import wt, mt
from SDK.utilslib.fileops import getcellname
from kernelpredict import detect, get_images, get_filePath_fileName_fileExt

# 裁剪原图为细胞图，主要函数是crop_images，其他函数是被这个函数调用
class cells_detect_crop(worker):
    def __init__(self):
        #初始化一个dataset的worker
        worker.__init__(self, wt.DATA.value)

        self.model_path = ""
        self.detector =  None
        self.log.info("初始化一个数据预处理的worker")
        self.mtype = mt.YOLOV4.value

        self.configPath = ""
        self.weightPath = ""
        self.metaPath = "names-data/obj.data"
        self.batch_size = 20

    def crop_images(self):
        #细胞定位时候才需要，如果按照标注裁剪不需要
        if self.datasetinfo['parameter_type'] == 0:
            self.log.info("方式：图片直接送检测并切割出细胞")
            model_path = self.datasetinfo['modpath'] #目前存的是绝对路径
            print(model_path)
            if self.model_path != model_path or self.detector is None:
                self.model_path = model_path
                self.weightPath = model_path
                self.configPath = model_path.replace('.weights', '.cfg')
                self.detector =  detect(self.configPath, self.weightPath, self.metaPath, self.batch_size)
        elif self.datasetinfo['parameter_type'] == 1:
            self.log.info("方式：按照标注切割出细胞")

        df_allcells = None
        df_imgs = pd.read_csv(self.dataset_lists)
        ts1 = int(time.time()*1000)
        for index, imginfo in df_imgs.iterrows():
            imgpath = os.path.join(self.rootdir, imginfo['imgpath'])
            img = cv2.imread(imgpath)
            slices = self.detector.img_slice(img, size=608, padx=148, pady=128) # FOV 切成多个608x608图片， 默认认为输入尺寸是2448x2048
            slicesresults = self.detector.batchDetect(slices, img) # 多个切图里面预测细胞核
            results = self.detector.resultsConcat(slices, slicesresults) # 把预测结果还原到原FOV图
            results = self.detector.removeSmall(results) # 删除细胞核太小，以及得分不高的
            if len(results) > 0:
                print(results)
                # filepath, shotname, extension = get_filePath_fileName_fileExt(imgpath)
                # savepath = os.path.join(outdir, shotname + extension)
                # d.drawRectangle(results, img, savepath)
        return True
