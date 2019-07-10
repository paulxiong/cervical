import os,sys,time,gc
from step0v2 import step0v2
from step1v2 import step1v2
sys.path.append(os.path.abspath('step2v2'))
sys.path.append(os.path.abspath('step2v2/modules/'))
from step2v2.schwaebische_nuclei_predict_v2 import step2v2
from step3v2 import step3v2
from src.utilslib.webserverapi import get_one_job, post_job_status
from src.utilslib.logger import  logger

class cell_crop():
    def __init__(self, jobId, jobdir):
        self.jid = jobId
        #path
        self.scratchdir = './scratch'
        self.jobdir = self.scratchdir + '/' + jobdir                            # path of every job
        self.filelist = self.jobdir + '/filelist.csv'
        self.input_datasets = self.jobdir + '/input_datasets'                  # input FOV images and csv
        self.input_datasets_denoising = self.jobdir + '/input_datasets_denoising' # denoised images
        self.middle_mask = self.jobdir + '/middle_mask'                           # images mask
        self.output_datasets = self.jobdir + '/output_datasets'                   # croped cells
        self.output_datasets_npy = self.jobdir + '/output_datasets/npy'                   # croped cells
        #const path
        self.modpath = './src/SEGMENT/kaggle-dsb2018/src/all_output'
        self.datasets_train_path = 'datasets/segment/stage1_train'
        self.csvroot = '/ai/lambdatest/csv'
        self.imgroot= '/ai/lambdatest/img'
        #config
        self.action = 'predict_test'
        self.cuda_device = '1'
        self.filepattern = '*.JPG'
        self.crop_method = 'Mask'
        self.area_thresh = 100
        self.square_edge = 50
        self.perimeter_vs_area = 18
        self.makedir()
        #log
        self.logger = logger(str(self.jid), self.jobdir)
        return
    def makedir(self):
        if os.path.exists(self.scratchdir) is False:
            os.makedirs(self.scratchdir)
        if os.path.exists(self.jobdir) is False:
            os.makedirs(self.jobdir)
        if os.path.exists(self.input_datasets) is False:
            os.makedirs(self.input_datasets)
        if os.path.exists(self.input_datasets_denoising) is False:
            os.makedirs(self.input_datasets_denoising)
        if os.path.exists(self.middle_mask) is False:
            os.makedirs(self.middle_mask)
        if os.path.exists(self.output_datasets) is False:
            os.makedirs(self.output_datasets)
        if os.path.exists(self.output_datasets_npy) is False:
            os.makedirs(self.output_datasets_npy)
        return
    def done(self, text):
        #0初始化1用户要求开始处理2开始处理3处理出错4处理完成5目录不存在
        post_job_status(self.jid, 4)
        self.logger.info(text)
        return
    def failed(self, text):
        post_job_status(self.jid, 3)
        self.logger.info(text)
        return

if __name__ == '__main__':
    while 1:
        jobid, status, dirname = get_one_job()
        if status != 1 or dirname is None:
            time.sleep(5)
            continue

        j = cell_crop(jobid, dirname)
        j.makedir()

        j.logger.info("begain step0...")
        try:
            ret = step0v2(j.filelist, j.imgroot, j.csvroot, j.scratchdir, j.logger)
        except Exception as ex:
            j.failed(ex)
            continue
        else:
            if ret is False:
                j.failed("step0 failed")
                continue
        j.logger.info("end step0...")

        j.logger.info("begain step1...")
        try:
            step1v2(j.input_datasets, j.input_datasets_denoising, j.filepattern)
        except Exception as ex:
            j.failed(ex)
            continue
        j.logger.info("end step1...")

        j.logger.info("begain step2...")
        try:
            step2v2(j.action, j.modpath, j.cuda_device, j.datasets_train_path, j.input_datasets_denoising, j.middle_mask)
        except Exception as ex:
            j.failed(ex)
            continue
        j.logger.info("end step2...")

        j.logger.info("begain step3...")
        try:
            step3v2(j.input_datasets, j.filepattern, j.output_datasets, j.input_datasets_denoising, j.middle_mask, j.crop_method, j.area_thresh, j.square_edge, j.perimeter_vs_area)
        except Exception as ex:
            j.failed(ex)
            continue
        j.logger.info("end step3...")


        j.done('done!')

        #python3 step4_annot.py --origin_dir '/ai/lambdatest/*/' --pattern '*.JPG' --seg_dir datasets/classify --output_dir datasets/classify/annot_out
        print("step4")

        #python3 step5_gendata.py --annot_path datasets/classify/annot_out/annotation_default.txt --seg_dir datasets/classify
        #                         --output_dir datasets/classify/train_datasets --train_test_split
        print("step5")

        #python3 step6_copy2nugan.py --origin_dir '/ai/lambdatest/*/' --csv_dir datasets/classify/annot_out/fov_type.csv
        #                            --npy_dir datasets/classify/npy/ --output_dir datasets/classify/data --pattern '*.JPG'
        print("step6")

        del j
        gc.collect()
        time.sleep(5)
