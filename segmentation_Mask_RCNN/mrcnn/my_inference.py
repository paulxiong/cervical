seed=123
import numpy as np
np.random.seed(seed)
import tensorflow as tf
tf.set_random_seed(seed)
import random
random.seed(seed)
from skimage import img_as_ubyte
import model as modellib
import pandas as pd
import os, sys
import my_functions as f
import time
import cv2
from config import Config
import scipy
import visualize
import time

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
    def __init__(self, model_path, original_img_path, cells_path, cells_mask_path):
        self.model_path = model_path
        self.original_img_path = original_img_path
        self.cells_mask_path = cells_mask_path
        self.cells_path = cells_path
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
                    print(">>> unexpected folder Error: %s, must be image." % path1)
                continue
            ext = os.path.splitext(path1)[1]
            ext = ext.lower()
            if not ext in ['.jpg', '.png', '.jpeg', '.bmp']:
                if self.debug and (not ext in ['.csv']):
                    print(">>> unexpected file: %s, must be jpg/png/bmp" % path1)
            else:
                image_list.append(i)
        if self.debug is True and allfiles_num > len(image_list):
            print(">>> %d files/folder ignored !!" % (allfiles_num - len(image_list)))
        return image_list

    def calculate_wh(self, x, y, img, side):
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

    def compare_rois(self, x_, y_, seg_center): # x_, y_为原始csv中细胞中心坐标, seg_center为切割细胞中心坐标矩阵
        index, x1, y1, x2, y2 = None, None, None, None, None
        limit = 20
        min_distance = 1000000
        for n in range(len(seg_center)):
            x1, y1, x2, y2 = seg_center[n, 1], seg_center[n, 0], seg_center[n, 3], seg_center[n, 2]
            x = int((x1 + x2)/2)
            y = int((y1 + y2)/2)
            L_temp = np.sqrt((np.square(x_ - x)) + np.square(y_ - y))
            if L_temp < min_distance:
                min_distance = L_temp
                index, x1_, y1_, x2_, y2_ = n, x1, y1, x2, y2
        if min_distance < limit:
            return True, index, x1_, y1_, x2_, y2_
        return False, index, x1_, y1_, x2_, y2_

    def get_FOV_type(self, org_csv_path): # 获取FOV类型
        sign_N = ['1','5','12','13','14','15']
        if not os.path.exists(original_img_path):
            return '-1' # 表示预测类型
        df1 = pd.read_csv(org_csv_path)
        for index, row in df1.iterrows(): # 遍历原始csv
            _type = row['Type']
            if _type in sign_N:
                return 'N'
            else:
                return 'P'

    def crop_fov(self, img, cell_point, npy, cells_path, cells_mask_path, filename, fov_type, cell_type): # img为读取到的原图， cell_point为目标细胞切割坐标， npy为目标对应的掩码， cells_path为存放细胞外层文件夹， filename为原图名称， fov_type为原图标签， cell_type为细胞类型
        x1, y1, x2, y2 = cell_point[1], cell_point[0], cell_point[3], cell_point[2]
        cropped = img[y1:y2,x1:x2,:]
        cells_crop_file_path = os.path.join(cells_path, '{}_{}_{}_{}_{}_{}_{}.png'.format(filename, fov_type, str(cell_type), x1, y1, x2, y2))
        cv2.imwrite(cells_crop_file_path, cropped)
        segmentate = np.tile(np.expand_dims(npy, axis=2),(1,1,3))
        img_masked = cropped*segmentate
        size_x, size_y = img_masked.shape[0], img_masked.shape[1]
        for n in range(size_x):
            for m in range(size_y):
                if img_masked[n,m,1] == 0:
                    img_masked[n,m,0] = 255
                    img_masked[n,m,1] = 255
                    img_masked[n,m,2] = 255
        cells_masked_crop_file_path = os.path.join(cells_mask_path, 'crop_masked', '{}_{}_{}_{}_{}_{}_{}masked.png'.format(filename, fov_type, cell_type, x1, y1, x2, y2))
        cv2.imwrite(cells_masked_crop_file_path, img_masked)
        return

    def detect_image(self, gray=False, print2=None, sign = '1'): # sign == 1为训练， sign == 2为预测
        pathList = self.get_image_lists()
        if print2 is None:
            print2 = print

        step, total_steps = 0, len(pathList)
        if total_steps < 1:
            return False
        for filename in pathList:
            step = step + 1
            image_path = os.path.join(self.original_img_path, filename)
            print2("step %d/%d  %s" %(step, total_steps, image_path))
            original_image = cv2.imread(image_path)
            predict_img = original_image

            if gray is True:
                grayImage = cv2.cvtColor(original_image, cv2.COLOR_RGB2GRAY)
                if len(grayImage.shape)<3:
                    grayImage = img_as_ubyte(grayImage)
                    grayImage = np.expand_dims(grayImage, 2)
                    grayImage = grayImage[:,:,[0,0,0]] # flip r and b
                grayImage = grayImage[:,:,:3]
                predict_img = grayImage
            else:
                if len(original_image.shape)<3:
                    original_image = img_as_ubyte(original_image)
                    original_image = np.expand_dims(original_image,2)
                    original_image = original_image[:,:,[0,0,0]] # flip r and b
                original_image = original_image[:,:,:3]
                predict_img = original_image

            ## Make prediction for that image
            results = self.model.detect([predict_img], verbose=0)
            r = results[0]
            scores_masks = r['scores']      #判别物得分
            final_rois = r["rois"]         #交并比得到的回归框坐标
            pred_masks = r['masks']

            _rois = []
            mask_cell_npy = []
            threshold = float(0.90)
            for i in range(0, len(scores_masks)):
                score = scores_masks[i]
                classid = r['class_ids'][i]
                roi = final_rois[i]
                if int(threshold*100) > int(score*100):
                    print2("%s drop roi, score=%f" % (filename, score))
                    continue

                mask_npy = pred_masks[:,:,i]
                y1, x1, y2, x2 = roi[0], roi[1], roi[2], roi[3]
                mask_x, mask_y = int((x2 + x1) / 2), int((y2 + y1) / 2)
                x1, y1, x2, y2 = self.calculate_wh(mask_x, mask_y, mask_npy, 50)
                _mask_npy = mask_npy[y1:y2, x1:x2]

                mask_cell_npy.append(_mask_npy)
                _rois.append([y1, x1, y2, x2])

            #mask_cell = np.array(mask_cell_npy)
            mask_npy = np.array(mask_cell_npy)
            cell_points = np.array(_rois)
            if sign == '1': # 训练
                org_csv_path = image_path[:-4] + '.csv' # 拼原始csv路径
                if os.path.exists(org_csv_path) == False:
                    print( filename + ' no csv')
                    continue
                df1 = pd.read_csv(org_csv_path)
                for index, row in df1.iterrows(): # 遍历原始csv
                    x_center = int(row['X'])
                    y_center = int(row['Y'])
                    cell_type = str(row['Type'])
                    cell_type = cell_type[:-2]
                    ret, index_, x1, y1, x2, y2 = self.compare_rois(x_center, y_center, cell_points) # seg_center为切割y1, x1, y2, x2
                    if ret == True:
                        fov_type = self.get_FOV_type(org_csv_path)
                        cell_point = [y1, x1, y2, x2]
                        self.crop_fov(original_image, cell_points[index_, :], mask_npy[index_,], cells_path, 
                                      cells_mask_path, filename, fov_type, cell_type)

            elif sign == '2': # 预测
                for n in range(len(cell_points)):
                    cell_point = cell_points[n,:]
                    cell_type = str(100)
                    fov_type = str(100)
                    self.crop_fov(original_image, cell_point, mask_cell_npy[n], cells_path, cells_mask_path, filename, fov_type, cell_type)

            if self.debug:
                visualize.display_instances(original_image, filename, r['rois'], r['masks'], r['class_ids'], r['scores'])
                output_image_path = os.path.join(self.output_image_path, filename + '1_.png')
                for i in range(len(final_rois)):
                    score = scores_masks[i]
                    rois = final_rois[i,:]
                    x1, x2, y1, y2 = rois[0], rois[2], rois[1], rois[3]
                    draw_color = (0, 0, 255)
#                     if (score >= 0.98):
#                         draw_color = (0, 0, 255)
#                     elif (0.94 < score < 0.98) :
#                         draw_color = (0, 255, 0)
#                     elif score <= 0.94 :
#                         draw_color = (255, 0, 0)
                    cv2.rectangle(original_image, (y1, x1), (y2, x2), draw_color, 1)
                cv2.imwrite(output_image_path, original_image)

        return True

if __name__ == "__main__":
    time_start=time.time()
    model_path = "./model/deepretina_final.h5"
    original_img_path = './origin_imgs'
    cells_path = './cells/crop'
    cells_mask_path = 'cells/crop_mask'
    d = detector(model_path, original_img_path, cells_path, cells_mask_path)
    d.detect_image(gray = True )
    time_end=time.time()
    print('totally cost:',time_end-time_start)
