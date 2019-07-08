import os,sys,time,gc
from step1v2 import step1v2
sys.path.append(os.path.abspath('step2v2'))
sys.path.append(os.path.abspath('step2v2/modules/'))
from src.utilslib.webserverapi import get_one_job
from src.utilslib.logger import  logger

class cell_crop():
    def __init__(self, jobId):
        self.jid = jobId
        #path
        self.scratchdir = './scratch'
        self.jobdir = self.scratchdir + '/' + self.jid                            # path of every job
        self.input_datasets = self.jobdir + '/input_datasets'                  # input FOV images and csv
        self.input_datasets_denoising = self.jobdir + '/input_datasets_denoising' # denoised images
        self.middle_mask = self.jobdir + '/middle_mask'                           # images mask
        self.output_datasets = self.jobdir + '/output_datasets'                   # croped cells
        #const path
        self.modpath = './src/SEGMENT/kaggle-dsb2018/src/all_output'
        self.datasets_train_path = 'datasets/segment/stage1_train'
        #config
        self.action = 'predict_test'
        self.cuda_device = '1'
        self.filepattern = '*.JPG'
        self.crop_method = 'Mask'
        self.area_thresh = 100
        self.square_edge = 50
        self.perimeter_vs_area = 18
        #log
        self.logger = logger(self.jid, self.jobdir)
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
        return

if __name__ == '__main__':
    while 1:
        _, job, study, hyperparameters = get_one_job()
        print(job)
        if job is None or job['type'] is not 'predict':
            time.sleep(5)
            continue
        ID = str(int(time.time()*1000)) + '00000001'
        ID = '156256766279800000001'
        j = cell_crop(ID)
        j.makedir()

        j.logger.info("begain step1...")
        step1v2(j.input_datasets, j.input_datasets_denoising, j.filepattern)
        j.logger.info("end step1...")

        j.logger.info("begain step2...")
        from step2v2.schwaebische_nuclei_predict_v2 import step2v2
        step2v2(j.action, j.modpath, j.cuda_device, j.datasets_train_path, j.input_datasets_denoising, j.middle_mask)
        j.logger.info("end step2...")

        j.logger.info("begain step3...")
        from step3v2 import step3v2
        step3v2(j.input_datasets, j.filepattern, j.output_datasets, j.input_datasets_denoising, j.middle_mask, j.crop_method, j.area_thresh, j.square_edge, j.perimeter_vs_area)
        j.logger.info("end step3...")

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
