# -*- coding: utf-8 -*-
import os, gc, sys, time
from enum import Enum
reload(sys)
sys.setdefaultencoding('utf-8')
#from segmentation.src.utilslib.logger import  logger
from utilslib.webserverapi import get_one_job, post_job_status

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
        self.scratchdir = os.environ.get('SCRATCHDIR', 'scratch/')
        #for image classification and nuclei segmentation
        self.experiment_root      = self.scratchdir + self.jobdir + "/"

        if not os.path.exists(self.experiment_root):
            os.makedirs(self.experiment_root)
        if not os.path.exists(self.experiment_root + '/picture'):
            os.makedirs(self.experiment_root + '/picture')
        if not os.path.exists(self.experiment_root + '/model'):
            os.makedirs(self.experiment_root + '/model')

        #log
        #self.logger = logger(str(self.jobid), self.jobdir)
    def done(self, text):
        #0初始化1用户要求开始处理2开始处理3处理出错4处理完成5目录不存在6开始训练7训练出错8训练完成
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
        if localdebug is not "True" and localdebug is not True:
            # datatype:  0未知1训练2预测
            jobid, status, dirname, jobtype = get_one_job(ds.READ4PROCESS.value, dt.TRAIN.value)
        else:
            jobid = 95
            status = 4
            dirname = 'vwlN83JI'

        print(status, dirname)
        if status != 1 or dirname is None:
            time.sleep(5)
            continue

        cgan = cervical_seg(jobid, dirname)
        for i in range(0, 100):
            time.sleep(1)
            cgan.processing(i)

        cgan.done('done!')

        del cgan
        gc.collect()
        time.sleep(5)

        if localdebug is "True" or localdebug is True:
            break
