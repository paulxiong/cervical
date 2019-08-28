seed=123
from keras import backend as K
import matplotlib as plt
import numpy as np
np.random.seed(seed)
import tensorflow as tf

tf.set_random_seed(seed)

import random
random.seed(seed)
from skimage import io 
from skimage import img_as_ubyte

import model as modellib
import pandas as pd
import os
import cv2
import my_functions as f
import visualize
import sys
import time

#######################################################################################
## SET UP CONFIGURATION
from config import Config

class BowlConfig(Config):
    """Configuration for training on the toy shapes dataset.
    Derives from the base Config class and overrides values specific
    to the toy shapes dataset.
    """
    # Give the configuration a recognizable name
    NAME = "Inference"

    IMAGE_RESIZE_MODE = "pad64" ## tried to modfied but I am using other git clone
    ## No augmentation
    ZOOM = False
    ASPECT_RATIO = 1
    MIN_ENLARGE = 1
    IMAGE_MIN_SCALE = False ## Not using this

    IMAGE_MIN_DIM = 512 # We scale small images up so that smallest side is 512
    IMAGE_MAX_DIM = False

    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

    DETECTION_MAX_INSTANCES = 512
    DETECTION_NMS_THRESHOLD =  0.2
    DETECTION_MIN_CONFIDENCE = 0.9

    LEARNING_RATE = 0.001
    
    # Number of classes (including background)
    NUM_CLASSES = 1 + 1 # background + nuclei

    # Use smaller anchors because our image and objects are small
    RPN_ANCHOR_SCALES = (8 , 16, 32, 64, 128)  # anchor side in pixels

    # Reduce training ROIs per image because the images are small and have
    # few objects. Aim to allow ROI sampling to pick 33% positive ROIs.
    TRAIN_ROIS_PER_IMAGE = 600

    USE_MINI_MASK = True

def main():
    inference_config = BowlConfig()
    inference_config.display()

    ROOT_DIR = os.getcwd()
    MODEL_DIR = os.path.join(ROOT_DIR, "logs")

    ## Change this with the path to the last epoch of train
    model_path = "./model/deepretina_final.h5"
    #sample_submission_path = sys.argv[1]
    print("Loading weights from ", model_path)
    test_path = './data1/0826_test2'
    # Recreate the model in inference mode
    model = modellib.MaskRCNN(mode="inference", 
                          config=inference_config,
                          model_dir=MODEL_DIR)
    model.load_weights(model_path, by_name=True)
    detect_image(test_path, model)
    

def __init__(self,test_path,model_path,save_path):
        self.test_path = test_path
        self.model_path = model_path
        self.save_path = save_path
#检测细胞
#返回细胞的坐标值
def detect_image(test_path, model):
    if not os.path.exists(test_path) or not os.path.isdir(test_path):
        raise RuntimeError('not found folder: %s' % test_path)
        
    pathList = os.listdir(test_path)
   
    for image_id in pathList:
       image_path = os.path.join(test_path,image_id)  
       if not pathList in ['JPG','.jpg', '.png', '.jpeg', '.bmp']:
            print(">>> unexpected file: %s, must be jpg/png/bmp" % image_path)
       original_image = io.imread(image_path) 
        
       if len(original_image.shape)<3:
           original_image = img_as_ubyte(original_image)
           original_image = np.expand_dims(original_image,2)
           original_image = original_image[:,:,[0,0,0]] # flip r and b
    ####################################################################
       original_image = original_image[:,:,:3] 
    ## Make prediction for that image 
       results = model.detect([original_image], verbose=0)   
       r = results[0]
       visualize.display_instances(original_image, image_id, r['rois'], r['masks'], r['class_ids'], 
                             r['scores'])
   
    ## Proccess prediction into rle
       pred_masks = results[0]['masks']       #每张图像的大小和对应的mask点
       scores_masks = results[0]['scores']    #判别物得分
       class_ids = results[0]['class_ids']
       final_rois =results[0]["rois"]         #交并比得到的回归框坐标
       print("cell_len:",len(class_ids))
       pd_data = pd.DataFrame(final_rois,columns=['x1', 'y1', 'x2', 'y2'])
     #print(pd_data)
       save_file = pd_data.to_csv("./cells/" + image_id + '.csv')

    
if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    ellapsed_time = (end_time-start_time)/3600
    print('Time required to train ', ellapsed_time, 'hours')

