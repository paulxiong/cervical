import os
import time
from utils.experiment import image_classificationv2, image_classification_trainv2
import numpy as np

class cervical_gan():
    def __init__(self, jobdir):
        self.jobdir = jobdir
        #for image classification and nuclei segmentation
        self.experiment_root      = "scratch/" + self.jobdir + "/"
        self.positive_images_root = self.experiment_root + "data/original/positive_images/"
        self.negative_images_root = self.experiment_root + "data/original/negative_images/"
        self.positive_npy_root    = self.experiment_root + "data/segmented/positive_npy/"
        self.negative_npy_root    = self.experiment_root + "data/segmented/negative_npy/"

        #cell_level_data
        self.X_train_path = self.experiment_root + 'data/cell_level_label/X_train.npy'
        self.X_test_path  = self.experiment_root + 'data/cell_level_label/X_test.npy'
        self.y_train_path = self.experiment_root + 'data/cell_level_label/y_train.npy'
        self.y_test_path  = self.experiment_root + 'data/cell_level_label/y_test.npy'

        self.n_epoch = 2
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

if __name__ == '__main__':
    cgan = cervical_gan('1234567')
    #cgan.train_gan()
    cgan.train2()
