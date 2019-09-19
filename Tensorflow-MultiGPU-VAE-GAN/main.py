import numpy as np
import os
from shutil import copyfile, rmtree
import matplotlib as mpl
mpl.use('Agg')

class vae_auto():
    def __init__(self, name):
        self.ROOTPATH = './'
        self.DSTPATH = os.path.join(self.ROOTPATH, name)
        self.FAKECOPY = os.path.join(self.ROOTPATH, 'fake_' + name)
        self.MODELSCOPY = os.path.join(self.ROOTPATH, 'models_' + name)
        self.MODELS = os.path.join(self.ROOTPATH, 'models')
        self.DATAORG = os.path.join(self.ROOTPATH, 'data_org')
        self.DATASETS = os.path.join(self.ROOTPATH, 'datasets')
        self.DATARESIZE = os.path.join(self.ROOTPATH, 'data_resize')
        self.IMGS = os.path.join(self.ROOTPATH, 'imgs')
        self.FAKE = os.path.join(self.ROOTPATH, 'fake')

    def clean_folds(self):
        dirs = [self.DATAORG, self.DATASETS, self.DATARESIZE, self.IMGS, self.FAKE, self.FAKECOPY, self.MODELSCOPY,self.MODELS]
        for n in dirs:
            if os.path.exists(n):
                rmtree(n)
            os.makedirs(n)
        print('>>>',self.DSTPATH)
        list_name = os.listdir(self.DSTPATH)
        for m in list_name:
            print(m)
            copyfile(self.DSTPATH + '/' + m, self.DATAORG + '/' + m)

    def datasets(self):
        activate_this = 'celeba_make_dataset.py'
        execfile(activate_this, dict(__file__=activate_this))

    def train(self):
        activate_this = 'VAE-GAN-multi-gpu-celebA.py'
        execfile(activate_this, dict(__file__=activate_this))

    def save_data(self):
        activate_this = 'fake.py'
        execfile(activate_this, dict(__file__=activate_this))
        list_name = os.listdir(self.FAKE)
        for n in list_name:
            copyfile(self.FAKE+'/'+n, self.FAKECOPY+'/'+n)
        list_name_2 = os.listdir(self.MODELS)
        for m in list_name_2:
            copyfile(self.MODELS+'/'+m, self.MODELSCOPY+'/'+m)

if __name__ == "__main__":
    vae = vae_auto('red_7')
    vae.clean_folds()
    vae.datasets()
    vae.train()
    vae.save_data()