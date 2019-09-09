# -*- coding: utf-8 -*-
import os, gc, sys, time
reload(sys)
sys.setdefaultencoding('utf-8')
#from segmentation.src.utilslib.logger import  logger
from utilslib.webserverapi import get_one_job, post_job_status

localdebug = os.environ.get('DEBUG', 'True')

class cervical_seg():
    def __init__(self, jobid, jobdir):
        self.jobdir = jobdir
        self.jid = jobid
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
        post_job_status(self.jid, 8)
        print(text)
        return
    def failed(self, text):
        post_job_status(self.jid, 3)
        print(text)
        return

if __name__ == '__main__':
    while 1:
        if localdebug is not "True" and localdebug is not True:
            # datatype:  0未知1训练2预测
            jobid, status, dirname = get_one_job(4, 1)
        else:
            jobid = 95
            status = 4
            dirname = 'vwlN83JI'

        if status != 4 or dirname is None:
            time.sleep(5)
            continue

        cgan = cervical_seg(jobid, dirname)
        cgan.done('done!')

        del cgan
        gc.collect()
        time.sleep(5)

        if localdebug is "True" or localdebug is True:
            break
