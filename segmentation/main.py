import os,sys,time,gc
from step0v2 import step0v2
from step1v2 import step1v2
sys.path.append(os.path.abspath('step2v2'))
sys.path.append(os.path.abspath('step2v2/modules/'))
from step2v2.schwaebische_nuclei_predict_v2 import step2v2
from step3v2 import step3v2
from src.utilslib.webserverapi import get_one_job, post_job_status
from src.utilslib.logger import  logger
from step7v2 import step7v2
from step4_annotv2 import step4_annotv2
from step5_gendatav2 import step5_gendatav2
from step6_copy2nuganv2 import step6_copy2nuganv2
from step6_generate_npy_v2 import step6_generate_npy_v2

localdebug = os.environ.get('GEBUG', 'True')

class cell_crop():
    def __init__(self, jobId, jobdir):
        self.jid = jobId
        #path
        self.scratchdir = os.environ.get('SCRATCHDIR', './scratch')
        self.jobdir = self.scratchdir + '/' + jobdir                            # path of every job
        self.filelist = self.jobdir + '/filelist.csv'
        self.infojson = self.jobdir + '/info.json'
        self.input_datasets = self.jobdir + '/input_datasets'                  # input FOV images and csv
        self.input_datasets_denoising = self.jobdir + '/input_datasets_denoising' # denoised images
        self.middle_mask = self.jobdir + '/middle_mask'                           # images mask
        self.output_datasets = self.jobdir + '/output_datasets'                   # croped cells
        self.output_datasets_npy = self.jobdir + '/output_datasets/npy'                   # croped cells
        self.output_datasets_slide_npy = self.jobdir + '/output_datasets/slide_npy'
        self.output_datasets_data = self.jobdir + '/output_datasets/data'
        self.output_annot_out = self.jobdir + '/output_datasets/annot_out'
        self.output_annot_out_txt = self.jobdir + '/output_datasets/annot_out/annotation_default.txt'
        self.output_annot_out_csv = self.jobdir + '/output_datasets/annot_out/fov_type.csv'
        self.output_train_datasets = self.jobdir + '/output_datasets/train_datasets'
        self.input_train_pridict = self.jobdir + '/train_predict_datasets/'
        #const path
        self.modpath = os.environ.get('MODDIR', './src/SEGMENT/kaggle-dsb2018/src/all_output')
        self.datasets_train_path = os.environ.get('TRAINDATASETS', 'datasets/segment/stage1_train')
        self.csvroot = os.environ.get('CSVDIR', './csv')
        self.imgroot= os.environ.get('IMGDIR', './img')
        #config
        self.action = 'predict_test'
        self.cuda_device = '0'
        self.filepattern = '*.JPG'
        self.crop_method = 'Mask'
        self.area_thresh = 100
        self.square_edge = 50
        self.perimeter_vs_area = 18
        self.train0_predict1 = 0
        #debug
        self.localdebug = localdebug
        #log
        self.logger = logger(str(self.jid), self.jobdir)

        self.makedir()
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
        if os.path.exists(self.output_annot_out) is False:
            os.makedirs(self.output_annot_out)
        if os.path.exists(self.output_train_datasets) is False:
            os.makedirs(self.output_train_datasets)
        if os.path.exists(self.output_datasets_data) is False:
            os.makedirs(self.output_datasets_data)
        if os.path.exists(self.input_train_pridict) is False:
            os.makedirs(self.input_train_pridict)
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
        if localdebug is not "True" and localdebug is not True:
            jobid, status, dirname = get_one_job()
        else:
            jobid = 95
            status = 1
            dirname = 'vwlN83JI'

        if status != 1 or dirname is None:
            time.sleep(5)
            continue

        j = cell_crop(jobid, dirname)
        j.makedir()

        #j.logger.info("begain step0...")
        #try:
        #    ret = step0v2(j.filelist, j.imgroot, j.csvroot, j.scratchdir, j.logger)
        #except Exception as ex:
        #    j.failed(ex)
        #    continue
        #else:
        #    if ret is False:
        #        j.failed("step0 failed")
        #        continue
        #j.logger.info("end step0...")

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


        step4_annotv2(j.input_datasets, j.output_datasets, j.filepattern, j.output_annot_out)
        print("step4")

        #python3 step5_gendata.py --annot_path datasets/classify/annot_out/annotation_default.txt --seg_dir datasets/classify
        #                         --output_dir datasets/classify/train_datasets --train_test_split
        step5_gendatav2(j.output_annot_out_txt, j.output_datasets, j.output_train_datasets, True)
        print("step5")

        #python3 step6_copy2nugan.py --origin_dir '/ai/lambdatest/*/' --csv_dir datasets/classify/annot_out/fov_type.csv
        #                            --npy_dir datasets/classify/npy/ --output_dir datasets/classify/data --pattern '*.JPG'
        step6_copy2nuganv2(j.input_datasets, j.output_annot_out_csv, j.output_datasets_npy, j.input_train_pridict, j.filepattern, True)
        #print("step6")

        step6_generate_npy_v2(j.output_train_datasets, j.input_train_pridict)

        j.logger.info("begain step7...")
        try:
            ret = step7v2(j)
        except Exception as ex:
            j.failed(ex)
            continue
        else:
            if ret is False:
                j.failed("step7 failed")
                continue

        break
        j.done('done!')

        del j
        gc.collect()
        time.sleep(5)
