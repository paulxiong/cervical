# !/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd
import numpy as np
import os
import time
import scipy.misc
from shutil import copyfile
from PIL import Image
import shutil
import cv2
from pandas.core.frame import DataFrame
from utilslib.fileinfo import get_original_imgname_by_filename, get_fov_type

def get_image_lists(original_img_path):
    if not os.path.exists(original_img_path) or \
       not os.path.isdir(original_img_path):
        raise RuntimeError('not found folder: %s' % original_img_path)
    image_list = []
    allfiles = os.listdir(original_img_path)
    allfiles_num = len(allfiles)
    for i in allfiles:
        path1 = os.path.join(original_img_path, i)
        if os.path.isdir(path1):
            print(">>> unexpected folder: %s, must be image." % path1)
            continue
        ext = os.path.splitext(path1)[1]
        ext = ext.lower()
        if not ext in ['.jpg', '.png', '.jpeg', '.bmp']:
            print(">>> unexpected file: %s, must be jpg/png/bmp" % path1)
        else:
            image_list.append(i)
    if allfiles_num > len(image_list):
        print(">>> %d files/folder ignored !!" % (allfiles_num - len(image_list)))
    return image_list

class cropper():
    def __init__(self, rootpath):
        self.original_img_path = os.path.join(rootpath, 'origin_imgs/')
        self.cells_rois_path = os.path.join(rootpath, 'cells/rois/')
        self.cells_crop_path = os.path.join(rootpath, 'cells/crop/')
        self.cells_npy_path = os.path.join(rootpath, 'cells/mask_npy/')
        self.cells_crop_masked = os.path.join(rootpath, 'cells/crop_masked/')

    def crop_fov(self, img, cells_crop_file_path, x1, y1, x2, y2, side, sign):
        if sign == 1: # 是否存成细胞图
            cropped = img[y1:y2,x1:x2,:]
            cv2.imwrite(cells_crop_file_path, cropped)
        color = []
        if sign != 1:
            if side == 50: # 选择标记细胞边框颜色
                color = [0,255,0]
            elif side == 55:
                color = [255,0,0]
            else:
                color = [0,0,255]
            cv2.rectangle(img, (x1, y1), (x2, y2), color,2)
        return cropped

    # 细胞原图加mask生成细胞核
    def processing_img(self, img, npy_path, masked_path, expand_side):
        #mask+原图 ==》img1
        mask = np.load(npy_path)
        #细胞边缘扩展(图像膨胀方法)
        if expand_side == 2:
            mask_w = mask.shape[0]
            mask_h = mask.shape[1]
            temp_mask = np.zeros((mask_w+6, mask_h+6)) # 用0扩展mask图一圈
            temp_mask[3:mask_w+3, 3:mask_h+3] = mask
            temp_mask_w = temp_mask.shape[0]
            temp_mask_h = temp_mask.shape[1]
            for i_temp_mask_w in range(3, temp_mask_w-7):
                for i_temp_mask_h in range(3, temp_mask_h-7):
                    filter_5_5 = np.zeros((5,5)) # 模板尺寸：5*5
                    filter_5_5 = temp_mask[i_temp_mask_w-2:i_temp_mask_w+2, i_temp_mask_h-2:i_temp_mask_h+2]
                    if np.mean(np.mean(filter_5_5)) != 0.0:
                        mask[i_temp_mask_w-1-3:i_temp_mask_w+1-3, i_temp_mask_h-1-3:i_temp_mask_h+1-3] = 1

        if expand_side == 1:
            mask_w = mask.shape[0]
            mask_h = mask.shape[1]
            temp_mask = np.zeros((mask_w+2, mask_h+2)) # 用0扩展mask图两圈
            temp_mask[1:mask_w+1, 1:mask_h+1] = mask
            temp_mask_w = temp_mask.shape[0]
            temp_mask_h = temp_mask.shape[1]
            for i_temp_mask_w in range(1, temp_mask_w-2):
                for i_temp_mask_h in range(1, temp_mask_h-2):
                    filter_3_3 = np.zeros((3,3)) # 模板尺寸：3*3
                    filter_3_3 = temp_mask[i_temp_mask_w-1:i_temp_mask_w+1, i_temp_mask_h-1:i_temp_mask_h+1]
                    if np.mean(np.mean(filter_3_3)) != 0.0:
                        mask[i_temp_mask_w-1,i_temp_mask_h-1] = 1
        segmentate = np.tile(np.expand_dims(mask,axis=2),(1,1,3))
        img1 = img*segmentate

        #细胞尺寸补齐，尺寸统一为：100*100
        limit_size = 100
        if img1.shape[0]==limit_size and img1.shape[1]==limit_size:
            pass
        else:
            temp_w = img1.shape[0]
            temp_h = img1.shape[1]
            temp_img1 = np.zeros((limit_size, limit_size, 3))
            num_str_w = int((limit_size - temp_w)/2)
            num_str_h = int((limit_size - temp_h)/2)
            temp_img1[num_str_w:num_str_w+temp_w, num_str_h:num_str_h+temp_h,:] = img1
            img1 = temp_img1

        #背景换成白色
        color_mean = img1.mean(axis=2)
        for p in range(0, color_mean.shape[0]):
            for q in range(0, color_mean.shape[1]):
                if color_mean[p, q] == 0.0:
                    img1[p, q, :] = 255
        cv2.imwrite(masked_path, img1)
        return

    def crop_fovs(self):
        imgs = get_image_lists(self.original_img_path)
        total_steps = len(imgs)
        step = 0
        for i in imgs:
            print("step %s/%d" % (step, total_steps))
            step = step + 1
            imgpath = os.path.join(self.original_img_path, i)
            (filepath, filename) = os.path.split(imgpath)

            csv_path = os.path.join(self.cells_rois_path, (filename + '_.csv_and.csv')) # 交集
            if not os.path.exists(csv_path):
                continue
            csv_org_path = imgpath[:-3] + 'csv' # 医生csv
            csv_seg_path = csv_path[:-8]
            if not os.path.exists(csv_path):
                print("not found %s" % csv_path)
                continue
            img = cv2.imread(imgpath) 
            degug = ['1'] # '1', '2', '3'分别代表交集csv，医生csv，裁减csv
            if '1' in degug:
                df1 = pd.read_csv(csv_path) # 交集csv
                for index, row in df1.iterrows():
                    x1, y1, x2, y2 = int(row['x1']), int(row['y1']), int(row['x2']), int(row['y2'])
                    cell_type, fov_type = str(int(row['type'])), get_fov_type(str(int(row['type'])))
                    cell_path = os.path.join(self.cells_crop_path, '{}_{}_{}_{}_{}_{}_{}.png'.format(filename,
                                             fov_type, cell_type, x1, y1, x2, y2))
                    x = int((x1 + x2)/2)
                    y = int((y1 + y2)/2)
                    crop_img = self.crop_fov(img, cell_path, x1, y1, x2, y2, side = 50, sign = 1)
                    roi = [x1, y1, x2, y2]
                    npy_path = os.path.join(self.cells_npy_path, '{}_{}_{}_{}_{}.npy'.format(filename, x1, y1, x2, y2))
                    masked_path = os.path.join(self.cells_crop_masked, '{}_{}_{}_{}_{}_{}_{}_maksed.png'.format(filename,
                                               fov_type, cell_type, x1, y1, x2, y2))
                    self.processing_img(crop_img, npy_path, masked_path, expand_side = 1)
                    # 下面的注释代码方便调试医生csv，裁剪csv，交集csv细胞在FOV上标记，以调试交集csv产生方法和性能提升，需保留
#                     x = int(row['x'])
#                     y = int(row['y'])
#                     self.crop_fov(img, cell_path, int(x), int(y), side = 50, sign = 1) 
            if '2' in degug:
                df_org = pd.read_csv(csv_org_path) # 原始csv
                for index_org, row_org in df_org.iterrows():
                    x, y = row_org['X'], row_org['Y']
                    cell_path = os.path.join(self.cells_crop_path, (filename + getFOVlabel(row_org['Type']) + \
                                    str(row_org['Type']) + '_' + str(int(x)) + '_' + str(int(y)) + '_w_h.png'))
                    self.crop_fov(img, cell_path, int(x), int(y), side = 55, sign = 1)
            if '3' in degug:
                df_seg = pd.read_csv(csv_seg_path) # 裁减csv
                for index_seg, row_seg in df_seg.iterrows():
                    x1,x2, y1,y2 = row_seg['x1'], row_seg['x2'],row_seg['y1'],row_seg['y2']
                    y = int((x1+x2)/2)
                    x = int((y1+y2)/2)
                    cell_path = os.path.join(self.cells_crop_path, (filename + getFOVlabel(row['type']) + \
                                    str(int(x)) + '_' + str(int(y)) + '_w_h.png'))
                    self.crop_fov(img, cell_path, int(x), int(y), side = 60, sign = 1)
            cv2.imwrite(imgpath + '_abc.png', img)
        return

if __name__ == '__main__':
    c = cropper('./')
    c.crop_fovs()
