# -*- coding: utf-8 -*-
import os
import time
from utils.experiment import image_classificationv2, image_classification_trainv2, image_classification_predictv2
import numpy as np
from segmentation.src.utilslib.webserverapi import get_one_job, post_job_status

localdebug = os.environ.get('GEBUG', 'True')

class cervical_gan():
    def __init__(self, jobid, jobdir):
        self.jobdir = jobdir
        self.jobid = jobid
        #for image classification and nuclei segmentation
        self.experiment_root      = "segmentation/scratch/" + self.jobdir + "/"
        self.positive_images_root = self.experiment_root + "train_predict_datasets/original/positive_images/"
        self.negative_images_root = self.experiment_root + "train_predict_datasets/original/negative_images/"
        self.positive_npy_root    = self.experiment_root + "train_predict_datasets/segmented/positive_npy/"
        self.negative_npy_root    = self.experiment_root + "train_predict_datasets/segmented/negative_npy/"

        #cell_level_data
        self.X_train_path = self.experiment_root + 'train_predict_datasets/cell_level_label/X_train.npy'
        self.X_test_path  = self.experiment_root + 'train_predict_datasets/cell_level_label/X_test.npy'
        self.y_train_path = self.experiment_root + 'train_predict_datasets/cell_level_label/y_train.npy'
        self.y_test_path  = self.experiment_root + 'train_predict_datasets/cell_level_label/y_test.npy'

        self.positive_test_images_root = self.experiment_root + "train_predict_datasets/original/positive_test_images/"
        self.negative_test_images_root = self.experiment_root + "train_predict_datasets/original/negative_test_images/"
        self.positive_test_npy_root    = self.experiment_root + "train_predict_datasets/segmented/positive_test_npy/"
        self.negative_test_npy_root    = self.experiment_root + "train_predict_datasets/segmented/negative_test_npy/"
        self.ref_path = ""

        self.n_epoch = 550
        self.batchsize = 36
        self.rand = 32
        self.dis = 1
        self.dis_category = len(np.unique(np.load(self.y_train_path)))
        self.ld = 1e-4
        self.lg = 1e-4
        self.lq = 1e-4
        self.random_seed = 42
        self.save_model_steps = 100
        self.intensity = 160 #segmentation intensity
        self.fold = 4
        self.choosing_fold = 1 #cross-validation for classification

        if not os.path.exists(self.experiment_root):
            os.makedirs(self.experiment_root)
        if not os.path.exists(self.experiment_root + '/picture'):
            os.makedirs(self.experiment_root + '/picture')
        if not os.path.exists(self.experiment_root + '/model'):
            os.makedirs(self.experiment_root + '/model')

        self.netD_path   = self.experiment_root + "model/netD_0.37644110275689224_1.6596411766945283_0.pth"
        self.netD_Q_path = self.experiment_root + "model/netD_Q_0.37644110275689224_1.6596411766945283_0.pth"
        self.clf_model   = self.experiment_root + "clf_model/svm_1564542659.model"

    def train_gan(self):
        image_classificationv2(self.positive_images_root, self.negative_images_root,
            self.positive_npy_root, self.negative_npy_root, self.intensity,
            self.X_train_path, self.X_test_path, self.y_train_path, self.y_test_path,
            self.experiment_root, self.fold, self.random_seed, self.choosing_fold,
            self.n_epoch, self.batchsize, self.rand, self.dis, self.dis_category,
            self.ld, self.lg, self.lq, self.save_model_steps)

    def train2(self):
        image_classification_trainv2(self.positive_images_root, self.negative_images_root,
            self.positive_npy_root, self.negative_npy_root, self.intensity,
            self.X_train_path, self.X_test_path, self.y_train_path, self.y_test_path,
            self.netD_path, self.netD_Q_path, self.experiment_root, self.fold, self.random_seed, self.choosing_fold,
            self.batchsize, self.rand, self.dis_category)

    def train3(self):
        image_classification_predictv2(self.positive_test_images_root, self.negative_test_images_root,
            self.positive_test_npy_root, self.negative_test_npy_root,
            self.intensity, self.experiment_root, self.netD_path, self.netD_Q_path,
            self.clf_model, dis_category=self.dis_category)

    def done(self, text):
        #0初始化1用户要求开始处理2开始处理3处理出错4处理完成5目录不存在6开始训练7训练出错8训练完成
        post_job_status(self.jid, 8)
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
            status = 4
            dirname = 'vwlN83JI'

        if status != 4 or dirname is None:
            time.sleep(5)
            continue

        cgan = cervical_gan(jobid, dirname)
        cgan.train_gan()
        #cgan.train2()
        #cgan.train3()
        cgan.done('done!')

        del cgan
        gc.collect()
        time.sleep(5)
