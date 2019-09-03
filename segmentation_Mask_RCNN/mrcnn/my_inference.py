seed=123
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
import my_functions as f
import time
import cv2
from config import Config
import scipy

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

class detector():
    def __init__(self, model_path, original_img_path, cells_rois_path, cells_mask_npy_path):
        self.model_path = model_path
        self.original_img_path = original_img_path
        self.cells_rois_path = cells_rois_path
        self.cells_mask_npy_path = cells_mask_npy_path
        self.debug = False
        self.inference_config = None
        self.logs_dir = './logs'
        self.output_image_path = './output_image'
        if not os.path.exists(self.model_path):
            raise RuntimeError("not found: %s" % model_path)
        if not os.path.exists(self.original_img_path):
            raise RuntimeError("not found: %s" % original_img_path)

        self.model = self.detector_init()

    def detector_init(self):
        self.inference_config = BowlConfig()
        if self.debug is True:
            self.inference_config.display()

        print("Loading weights from ", self.model_path)
        model = modellib.MaskRCNN(mode = "inference",
                    config = self.inference_config, model_dir = self.logs_dir)
        model.load_weights(self.model_path, by_name = True)
        return model

    # 找出目录里面所有的图片, 只查找self.original_img_path这级目录
    # 返回图片名称的一个数组
    def get_image_lists(self):
        if not os.path.exists(self.original_img_path) or \
           not os.path.isdir(self.original_img_path):
            raise RuntimeError('not found folder: %s' % self.original_img_path)
        image_list = []
        allfiles = os.listdir(self.original_img_path)
        allfiles_num = len(allfiles)
        for i in allfiles:
            path1 = os.path.join(self.original_img_path, i)
            if os.path.isdir(path1):
                if self.debug:
                    print(">>> unexpected folder: %s, must be image." % path1)
                continue
            ext = os.path.splitext(path1)[1]
            ext = ext.lower()
            if not ext in ['.jpg', '.png', '.jpeg', '.bmp']:
                if self.debug:
                    print(">>> unexpected file: %s, must be jpg/png/bmp" % path1)
            else:
                image_list.append(i)
        if self.debug is True and allfiles_num > len(image_list):
            print(">>> %d files/folder ignored !!" % (allfiles_num - len(image_list)))
        return image_list
    def calculate_wh(slef, x, y, img, side):
        limit_x = img.shape[1]
        limit_y = img.shape[0]
        x1 = x - side
        x2 = x + side
        y1 = y - side
        y2 = y + side
        x2 = int(max(0, min(limit_x, x2)))
        x1 = int(max(0, min(x2-1, x1)))
        y2 = int(max(0, min(limit_y, y2)))
        y1 = int(max(0, min(y2-1, y1)))
        return x1, y1, x2, y2

    def detect_image(self):
        pathList = self.get_image_lists()

        step, total_steps = 0, len(pathList)
        for filename in pathList:
            step = step + 1
            image_path = os.path.join(self.original_img_path, filename)
            print("step %d/%d  %s" %(step, total_steps, image_path))
            original_image = io.imread(image_path)

            if len(original_image.shape)<3:
                original_image = img_as_ubyte(original_image)
                original_image = np.expand_dims(original_image,2)
                original_image = original_image[:,:,[0,0,0]] # flip r and b
            original_image = original_image[:,:,:3]

            ## Make prediction for that image
            results = self.model.detect([original_image], verbose=0)
            r = results[0]

            scores_masks = r['scores']      #判别物得分
            final_rois = r["rois"]         #交并比得到的回归框坐标
            pred_masks = r['masks']

            _rois = []
            threshold = float(0.90)
            for i in range(0, len(scores_masks)):
                score = scores_masks[i]
                roi = final_rois[i]
                if int(threshold*100) > int(score*100):
                    print("%s drop roi, score=%f" % (filename, score))
                    continue

                mask_npy = pred_masks[:,:,i]
                y1, x1, y2, x2 = roi[0], roi[1], roi[2], roi[3]
                mask_x, mask_y = int((x2 + x1) / 2), int((y2 + y1) / 2)
                x1, y1, x2, y2 = self.calculate_wh(mask_x, mask_y, mask_npy, 32)

                _mask_npy = mask_npy[y1:y2, x1:x2]
                np.save(self.cells_mask_npy_path + '/' + filename + '_{}_{}_{}_{}.npy'.format(x1, y1, x2, y2), _mask_npy)
                _rois.append([y1, x1, y2, x2, float(int(score * 100) / 100)])

            csv_path = os.path.join(self.cells_rois_path, filename + '_.csv')
            pd_data = pd.DataFrame(_rois, columns=['y1', 'x1', 'y2', 'x2', 'score'])
            save_file = pd_data.to_csv(csv_path, quoting = 1, mode = 'w',
                        index = False, header = True)

            if self.debug:
                output_image_path = os.path.join(self.output_image_path, filename + '_.png')
                for i in range(len(final_rois)):
                    score = scores_masks[i]
                    rois = final_rois[i,:]
                    x1, x2, y1, y2 = rois[0], rois[2], rois[1], rois[3]
                    draw_color = (0, 0, 255)
                    if (score >= 0.98):
                        draw_color = (0, 0, 255)
                    elif (0.94 < score < 0.98) :
                        draw_color = (0, 255, 0)
                    elif score <= 0.94 :
                        draw_color = (255, 0, 0)
                    cv2.rectangle(original_image, (y1, x1), (y2, x2), draw_color, 4)
                io.imsave(output_image_path, original_image)

if __name__ == "__main__":
    model_path = "./model/deepretina_final.h5"
    original_img_path = './origin_imgs'
    cells_rois_path = 'cells/rois'
    cells_mask_npy_path = 'cells/mask_npy'
    d = detector(model_path, original_img_path, cells_rois_path, cells_mask_npy_path)
    d.detect_image()
