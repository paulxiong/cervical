# -*- coding: utf-8 -*-
import os, gc, sys, time, shutil
from enum import Enum
from utilslib.webserverapi import get_one_job, post_job_status
from utilslib.logger import logger
from utilslib.fileinfo import copy_origin_imgs
from utilslib.jsonfile import update_info_json
from my_inference import detector
from tocsv import get_trusted_labels
from tocells import cropper

localdebug = os.environ.get('DEBUG', 'False')

# datasets status
class ds(Enum):
    INIT            = 0 #0初始化
    READ4PROCESS    = 1 #1用户要求开始处理
    PROCESSING      = 2 #2开始处理
    PROCESSING_ERR  = 3 #3处理出错
    PROCESSING_DONE = 4 #4处理完成
    PATH_ERR        = 5 #5目录不存在
    TRAINNING       = 6 #6开始训练
    TRAINNING_ERR   = 7 #7训练出错
    TRAINNING_DONE  = 8 #8训练完成

# datasets type
class dt(Enum):
    UNKNOWN  = 0 #0未知
    TRAIN    = 1 #1训练
    PREDICT  = 2 #2预测

class cervical_seg():
    def __init__(self, jobid, jobdir):
        self.jobdir = jobdir
        self.jid = jobid
        self.percent = 0
        self.scratchdir  = os.environ.get('SCRATCHDIR', 'scratch/')
        self.rootdir     = os.path.join(self.scratchdir, self.jobdir) #每个任务的根目录
        #裁剪
        self.csvroot = os.environ.get('CSVDIR', './csv')
        self.imgroot = os.environ.get('IMGDIR', './img')
        self.model1_path = "./model/deepretina_final.h5" #mask-rcnn使用的模型
        self.gray        = True #检测细胞用黑白图（无论True还是False，最终扣出的细胞是彩色的）
        self.filelist    = os.path.join(self.rootdir, 'filelist.csv') #页面上选中的图片的列表
        self.infojson    = os.path.join(self.rootdir, 'info.json') #存任务的所有信息
        self.origin_imgs = os.path.join(self.rootdir, 'origin_imgs') #存放原图和原图对应的csv文件的目录
        self.cells       = os.path.join(self.rootdir, 'cells') #存放细胞相关的，比如检测出来原图细胞的坐标csv文件，细胞的mask，裁剪出来的细胞
        self.mask_npy    = os.path.join(self.cells, 'mask_npy') #ndarray 存成的npy文件，里面是每个细胞的mask
        self.rois        = os.path.join(self.cells, 'rois') #存放细胞在原图里的坐标
        self.crop        = os.path.join(self.cells, 'crop') #存放扣出来的细胞图，目前特指医生标注过的
        self.crop_masked = os.path.join(self.cells, 'crop_masked') #存放扣出来的细胞图去掉了背景，目前特指医生标注过的
        #初始化
        self.prepare_fs()
        self.d = detector(self.model1_path, self.origin_imgs, self.rois, self.mask_npy) # 准备裁剪
        self.c = cropper(self.rootdir)
        #log
        self.logger = logger(str(self.jid), self.rootdir)

    def segmentation(self):
        try:
            #把原图和对应的CSV拷贝到任务目录下面
            ret = copy_origin_imgs(self.filelist, self.imgroot, self.csvroot, self.origin_imgs, self.logger)
            if ret == False:
                self.logger.info('copy origin images failed')
                return False
            self.processing(5)
            #开始从图片里面定位细胞
            ret = self.d.detect_image(gray=self.gray, print2=self.logger.info)
            if ret == False:
                self.logger.info('detect cells failed')
                return False
            self.processing(45)
            #挑出医生标注过的坐标和检测出来的细胞的交集
            ret = get_trusted_labels(self.origin_imgs, self.rois)
            if ret == False:
                self.logger.info('get_trusted_labels failed')
                return False
            self.processing(75)
            #上面挑出来的细胞扣成细胞图
            ret = self.c.crop_fovs()
            if ret == False:
                self.logger.info('crop_fovs failed')
                return False
            self.processing(95)
        except Exception as ex:
            self.logger.info(ex)
            return False
        return True

    #初始化必要的文件夹
    def prepare_fs(self):
        dirs1 = [self.scratchdir, self.rootdir, self.origin_imgs, self.cells,
                 self.mask_npy, self.rois, self.crop, self.crop_masked]
        for folder in dirs1:
            if not os.path.exists(folder):
                os.makedirs(folder)

    def done(self, text):
        #0初始化1用户要求开始处理2开始处理3处理出错4处理完成5目录不存在6开始训练7训练出错8训练完成
        self.percent = 100
        post_job_status(self.jid, 4, self.percent)
        print(text)
        return
    def processing(self, percent):
        self.percent = percent
        post_job_status(self.jid, 2, self.percent)
        return
    def failed(self, text):
        post_job_status(self.jid, 3, self.percent)
        print(text)
        return

if __name__ == '__main__':
    while 1:
        #向服务器请求任务，任务的状态必须是 READ4PROCESS
        if localdebug is not True and localdebug != "True":
            # datatype:  0未知1训练2预测
            jobid, status, dirname, jobtype = get_one_job(ds.READ4PROCESS.value, dt.TRAIN.value)
        else:
            jobid = 31
            status = ds.READ4PROCESS.value
            dirname = 'BVv1p1U6'

        #检查得到的任务是不是想要的
        if status != ds.READ4PROCESS.value or dirname is None:
            time.sleep(5)
            continue

        #新建任务
        cseg = cervical_seg(jobid, dirname)
        #处理完之前更新任务信息到info.json，方便web展示原图
        update_info_json(cseg, ds.PROCESSING.value)
        #开始处理任务
        ret = cseg.segmentation()
        #处理结果判断
        if ret == True:
            #处理完之后更新任务信息到info.json
            update_info_json(cseg, ds.PROCESSING_DONE.value)
            cseg.done('done!')
        else:
            #处理完之后更新任务信息到info.json
            update_info_json(cseg, ds.PROCESSING_ERR.value)
            cseg.failed("failed segmentation: %d %s" % (cseg.jid, cseg.jobdir))

        del cseg
        gc.collect()
        time.sleep(5)

        if localdebug is "True" or localdebug is True:
            break
