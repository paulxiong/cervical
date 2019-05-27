from __future__ import division

import cv2
import numpy as np
import pandas as pd
#from sklearn.model_selection import KFold
#from sklearn import metrics
import keras
import glob
import ntpath
import os
#import shutil
#import sys


from keras.models import Model
#from keras.optimizers import Adam
from keras.applications.inception_v3 import InceptionV3
from keras.layers import Dense, Input, Flatten, Dropout, GlobalAveragePooling2D
from keras.layers.normalization import BatchNormalization
from keras import backend as K
import tensorflow as tf
#from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

from module.image_preprocessing import contrast_enhance

''' decorator for time cost analysis'''
import time
import re
# global var for time cost analysis
cp_list = []

def time_it(fun):
    def new_fun(*args,**kwargs):
        global cp_list
        start = time.time()
        result = fun(*args,**kwargs)
        end = time.time()
        duration = (end-start)*1000
        name = re.search(r' [a-zA-Z_\.]*',str(fun)).group()[1:]
        cp_list.append([name,duration])
        return result
    return new_fun
'''-----------end_decorator----------'''

def get_flops(model):
    run_meta = tf.RunMetadata()
    opts = tf.profiler.ProfileOptionBuilder.float_operation()

    # We use the Keras session graph in the call to the profiler.
    flops = tf.profiler.profile(graph=K.get_session().graph,
                                run_meta=run_meta, cmd='op', options=opts)

    return flops.total_float_ops  # Prints the "flops" of the model.


# # Define CNN Model Architecture
#def inceptionv3(img_dim):
#    input_tensor = Input(shape=img_dim)
#    base_model = InceptionV3(include_top=False,
#                   weights='imagenet',
#                   input_shape=img_dim)
#    bn = BatchNormalization()(input_tensor)
#    x = base_model(bn)
#    x = GlobalAveragePooling2D()(x)
#    x = Dropout(0.5)(x)
#    output = Dense(1, activation='sigmoid')(x)
#    model = Model(input_tensor, output)
#  return model
def inceptionv3(img_dim, clf_mode='binary', dropout=0.5, class_num=1):
    input_tensor = Input(shape=img_dim)
    base_model = InceptionV3(include_top=False,
                             weights='imagenet',
                             input_shape=img_dim)
    bn = BatchNormalization()(input_tensor)
    x = base_model(bn)
    x = GlobalAveragePooling2D()(x)
    #x = GlobalMaxPooling2D()(x)
    x = Dropout(dropout)(x)
    if clf_mode == 'Binary':
        #define last layer
        output = Dense(class_num, activation='sigmoid')(x)
        #define loss mode
        loss_mode = 'binary_crossentropy'
    elif clf_mode == 'MultiClass':
        assert class_num > 1, "Error, Multi class Number %d !> 1"%class_num
        #add a layer 
        #x = Dense(512, activation='elu')(x)
        #x = Dropout(dropout)(x)
        #last layer
        output = Dense(class_num, activation='softmax')(x)
        #loss mode
        loss_mode = 'categorical_crossentropy'
    
    model = Model(input_tensor, output)

    return model
    
    
#===============================
# image pre-process
#===============================
def padding(img, img_size, color):
    shape = img.shape[:-1]
    #print(img.shape,img_size)
    delta_height = img_size[0]-shape[0]
    delta_width = img_size[1]-shape[1]
    top = delta_height//2
    bottom = delta_height-top
    left = delta_width//2
    right = delta_width-left
    new_img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    return new_img

def double_size_and_padding(img, img_size, color):
    shape = img.shape[:-1]
    shape = tuple([edge*2 for edge in shape])
    img = cv2.resize(img, shape)
    #print(img.shape,img_size)
    assert (shape[0] < img_size[0])&(shape[1] < img_size[1]), \
                        "Input shape:{},Require shape:{}".format(shape, img_size)
    new_img = padding(img, img_size, color)
    return new_img
    
def oversize_crop(img, img_size, ratio):
    max_height = img_size[0] // ratio
    max_width = img_size[1] // ratio
    height = np.shape(img)[0]
    width = np.shape(img)[1]
    if width > max_width:
        left = (width - max_width) // 2
        right = width - max_width - left
        img = img[:, left:-right, :]
    if height > max_height:
        above = (height - max_height) // 2
        below = height - max_height - above
        img = img[above:-below, :, :]
    return img

class CervixClassifier(object):
    def __init__(self,
                 init_weights_path,
                 dataset_dir,
                 clf_mode='Binary',
                 color_mode='RGB',
                 class_num=1,
                 init_dim=[299,299,3], 
                 padding_methods='Double_ZoomOut_Padding',
                 init_batch_size=5
                 ):
        '''
            init_dim: a list of [image_height,image_width,image_channels]
            init_weights_path: initial weights path of inceptionv3 model 
            dataset_dir: the path to the segment datasets, with format dataset_dir/{}.png_output/
        '''
        #path parameters.For the input file name is generated by original path,
        #and the path of segment image for test is not as same as original path,
        #so here we store the pattern of test path, and use it to generate the paths
        #for different original images 
        self.TEST_FOLDER_PAT = dataset_dir + '/{}.png_output/crops/'
        self.PREVIEW_FOLDER_PAT = dataset_dir + '/{}.png_output/preview/'
        self.FINAL_RESULT_FILE_PAT = '{}/final_result.csv'
        self.INPUT_FILE_PATTERN = '*.png'
        
        #vars for path, use self.set_test_folder(img_name) to set all these vars
        self.TEST_FOLDER = None
        self.PREVIEW_FOLDER = None
        self.FINAL_RESULT_FILE = None
        
        #model parameters 
        self.IMG_DIM = init_dim
        self.BATCH_SIZE = init_batch_size
        
        ##model
        assert clf_mode in ['Binary', 'MultiClass'], "Bad classifier mode %s"%clf_mode
        self.CLF_MODE = clf_mode
        self.CLASS_NUM = class_num
        self.COLOR_MODE = color_mode
        self.MODEL = inceptionv3(self.IMG_DIM,
                                 clf_mode=self.CLF_MODE,
                                 class_num=self.CLASS_NUM)
        print(get_flops(self.MODEL))
        self.MODEL.summary()
        self.load_weights(init_weights_path)
        
        #preprocessing params
        self.PADDING_METHOD = padding_methods
        
        #Test prediction result
        self.TEST_RES = None
    
    def load_weights(self, weights_path):
        '''
            weights_path: weights path of inceptionv3 model
        '''
        self.MODEL.load_weights(filepath=weights_path)
    
    
    def set_test_folder(self, img_name):
        '''
            img_name: base name of the image file, str
        '''
        self.TEST_FOLDER = self.TEST_FOLDER_PAT.format(img_name)
        self.PREVIEW_FOLDER = self.PREVIEW_FOLDER_PAT.format(img_name)
        self.FINAL_RESULT_FILE = self.FINAL_RESULT_FILE_PAT.format(self.PREVIEW_FOLDER)
        
    # # Load Datasets
    # Since we will be using a generator we don't need to actually load in any files into memory 
    # all we need is the filepaths :)
    #@time_it
    def load_test(self, crops_path=None):
        '''
            crops_path: the directory path of the Segmented cell images(crops), default: self.TEST_FOLDER
        '''
        if crops_path is None:
            crops_path = self.TEST_FOLDER
        print(crops_path)
        
        test_files = list(np.sort(glob.glob(os.path.join(crops_path, self.INPUT_FILE_PATTERN))))
        names = [ntpath.basename(file_path) for file_path in test_files]
        positive = [0.5] * len(names)
        self.TEST_RES = pd.DataFrame(np.stack([names, positive], axis=1), columns= ['name','positive'])
        del names,positive
        
        #check the result
        print(len(test_files),self.TEST_RES.shape)
        #print(self.TEST_RES.head())
        return test_files

    
    @time_it
    def predict_test(self, test_files, batch_size=5, img_size=None):
        '''
            batch_size: batch size for predictions
            img_size: a tuple of (image_height, image_width)
            test_files: a list of the path to test files
        '''
        if img_size is None:
            img_size = tuple(self.IMG_DIM[:2])
        
        #add clahe to input crops=
        clahe = cv2.createCLAHE(clipLimit=5, tileGridSize=(2, 2))
        
        #test generator   
        def test_generator():
            while True:
                for start in range(0, len(test_files), batch_size):
                    x_batch = []
                    end = min(start + batch_size, len(test_files))
                    test_batch = test_files[start:end]
                    for filepath in test_batch:
                        #img = cv2.imread(filepath)
                        
                        r = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE).astype("uint8")
                        g = r
                        b = r
                        img = np.dstack((r, g, b))
                        
                        x_batch.append(img)
                    
                    contrast_enhance(x_batch, self.COLOR_MODE,  clahe)
                    
                    for i, img in enumerate(x_batch):
                        if self.PADDING_METHOD == 'Double_ZoomOut_Padding':
                            if (np.shape(img)[0] >= 150) or (np.shape(img)[1] >= 150):
                                img = oversize_crop(img, img_size, 2)
                            img = double_size_and_padding(img, img_size, (0, 0, 0))
                        elif self.PADDING_METHOD == 'Padding':
                            img = padding(img, img_size, (0, 0, 0))
                        elif self.PADDING_METHOD == 'Warp':
                            img = cv2.resize(img, img_size)
                        else:
                            print("Not supported Padding method.")
                            exit(-1)
                            
                        x_batch[i] = img
                
                    for i, img in enumerate(x_batch):
                        assert img.shape[:-1] == img_size, "img size error: No.{}, Size {}".format(i, img.shape)
                        
                    x_batch = np.array(x_batch, np.float32) / 255.
                    yield x_batch
                
        test_steps = np.ceil(len(test_files) / batch_size)
        
        preds_test = self.MODEL.predict_generator(generator=test_generator(),
                                              steps=test_steps, verbose=1)
                                              
        if self.CLF_MODE == 'Binary':
            preds_test = preds_test[:, -1]
        
       # print(len(test_files),test_steps,len(test_files)/batch_size, preds_test.shape)
        
        return preds_test
    
    #@time_it
    def gen_final_csv(self,preds_test):
        if len(preds_test) != 0:
            if self.CLF_MODE == 'Binary':
                self.TEST_RES['positive'] = preds_test
            elif self.CLF_MODE == 'MultiClass':
                try:
                    self.TEST_RES['positive'] = np.argmax(preds_test, axis=1)
                except:
                    print("No predict results found.")
                    print(np.shape(preds_test)) 
                    print(preds_test)
                    pass
                for clazz in range(np.shape(preds_test)[1]):
                    self.TEST_RES['preds_' + str(clazz)] = preds_test[:, clazz]
            self.TEST_RES.to_csv(self.FINAL_RESULT_FILE, index=None)
        
    def count_positive(self,preds_test,threshold=None):
        if len(preds_test) != 0:
            if self.CLF_MODE == 'Binary':
                assert type(threshold) == float
                num = np.sum(preds_test > threshold)
                print("Count of positive is {} with threshold {}." .format(num, threshold))
            elif self.CLF_MODE == 'MultiClass':
                assert threshold is None
                preds_cat = np.argmax(preds_test, axis=1)
                for clazz in np.unique(preds_cat):
                    num = np.sum(preds_cat == clazz)
                    print("Count of Class-{} is {}.".format(clazz, num))
        else:
            print("No Predict results found")
    
    @time_it   
    def run_test_predict(self, img_name, threshold):
        '''
            img_name: base name of the image file, str
        '''
        self.set_test_folder(img_name)
        test_files = self.load_test()
        preds_test = self.predict_test(test_files)
        self.gen_final_csv(preds_test)
        self.count_positive(preds_test, threshold)



# Test_cases:

if __name__=='__main__':
    os.environ["CUDA_VISIBLE_DEVICES"] = '7'
    weights_path = 'inception.fold_1.hdf5'
    util = CervixClassifier(weights_path, 
                            'datasets/classify', 
                            clf_mode='MultiClass',
                            class_num=5)
    
    util.TEST_FOLDER_PAT = '../../../' + util.TEST_FOLDER_PAT
    util.PREVIEW_FOLDER_PAT = '../../../' + util.PREVIEW_FOLDER_PAT
    
    file_list = ['HSIL_IMG001x006','HSIL_IMG001x009',\
    'LSIL_HPV_IMG001x018','LSIL_HPV_IMG001x020',\
    'LSIL_HPV_IMG002x006','LSIL_HPV_IMG002x008',\
    'LSIL_IMG005x017', 'LSIL_IMG006x004',\
    'NILM_HS_IMG005x019']
    for file in file_list:
        print(file)
        #util.run_test_predict(file,0.9)
        util.run_test_predict(file,None)
    #util.run_test_predict('IMG001x013',0.9)
    
    for name,duration in cp_list:
        print('Function {} time costs: {} ms'.format(name,duration))
    
    fd = open('./check_point_inception.txt','w')
    fd.write(str(cp_list))
    fd.close()
