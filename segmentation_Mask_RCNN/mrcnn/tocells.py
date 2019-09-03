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

def getFOVlabel(type):
    label_N = [1, 5, 12, 13, 14, 15]
    FOVlabel = []
    if type in label_N:
        FOVlabel = 'N'
    else:
        FOVlabel = 'P'
    FOVlabel = '_' + FOVlabel + '_'
    return FOVlabel

class cropper():
    def __init__(self, rootpath):
        self.original_img_path = os.path.join(rootpath, 'origin_imgs/')
        self.cells_rois_path = os.path.join(rootpath, 'cells/rois/')
        self.cells_crop_path = os.path.join(rootpath, 'cells/crop/')
        self.cells_npy_path = os.path.join(rootpath, 'cells/mask_npy/')
        self.cells_crop_masked = os.path.join(rootpath, 'cells/crop_masked/')

    def crop_fov(img, cells_crop_file_path, x, y, side, sign):
        limit_x = img.shape[1]
        limit_y = img.shape[0]
        x1, x2, y1, y2 = (x - side), (x + side), (y - side), (y + side)
        x2 = int(max(0, min(limit_x, x2)))
        x1 = int(max(0, min(x2-1, x1)))
        y2 = int(max(0, min(limit_y, y2)))
        y1 = int(max(0, min(y2-1, y1)))
        if sign == 1: # 是否存成细胞图
            cropped = img[y1:y2,x1:x2,:]
            scipy.misc.imsave(cells_crop_file_path, cropped)
        color = []
        if side == 50: # 选择标记细胞边框颜色
            color = [0,255,0]
        elif side == 55:
            color = [255,0,0]
        else:
            color = [0,0,255]
        cv2.rectangle(img, (x1, y1), (x2, y2), color,2)
        return

    def crop_fov2(self, img, cells_crop_file_path, x1, y1, x2, y2, sign):
        if sign == 1: # 是否存成细胞图
            cropped = img[y1:y2,x1:x2,:]
            cv2.imwrite(cells_crop_file_path, cropped)
        return cropped

    # 细胞原图加mask生成细胞核
    def processing_img(self, img, npy_path, masked_path, expand_side):
        #mask+原图 ==》img1
        mask = np.load(npy_path)
        #细胞边缘扩展(图像膨胀方法，模板尺寸：3*3)
        if expand_side == 1:
            mask_w = mask.shape[0]
            mask_h = mask.shape[1]
            temp_mask = np.zeros((mask_w+2, mask_h+2)) # 用0扩展mask图一圈
            temp_mask[1:mask_w+1, 1:mask_h+1] = mask
            temp_mask_w = temp_mask.shape[0]
            temp_mask_h = temp_mask.shape[1]
            for i_temp_mask_w in range(1, temp_mask_w-2):
                for i_temp_mask_h in range(1, temp_mask_h-2):
                    filter_3_3 = np.zeros((3,3))
                    filter_3_3[0,0] = temp_mask[i_temp_mask_w-1, i_temp_mask_h-1]
                    filter_3_3[0,1] = temp_mask[i_temp_mask_w-1, i_temp_mask_h]
                    filter_3_3[0,2] = temp_mask[i_temp_mask_w-1, i_temp_mask_h+1]
                    filter_3_3[1,0] = temp_mask[i_temp_mask_w, i_temp_mask_h-1]
                    filter_3_3[1,1] = temp_mask[i_temp_mask_w, i_temp_mask_h] # 中心
                    filter_3_3[1,2] = temp_mask[i_temp_mask_w, i_temp_mask_h+1]
                    filter_3_3[2,0] = temp_mask[i_temp_mask_w+1, i_temp_mask_h-1]
                    filter_3_3[2,1] = temp_mask[i_temp_mask_w+1, i_temp_mask_h]
                    filter_3_3[2,2] = temp_mask[i_temp_mask_w+1, i_temp_mask_h+1]
                    if np.mean(np.mean(filter_3_3)) != 0.0:
                        mask[i_temp_mask_w,i_temp_mask_h] = 1
                        
        segmentate = np.tile(np.expand_dims(mask,axis=2),(1,1,3))
        img1 = img*segmentate

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
        for i in imgs:
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
                    cell_path = os.path.join(self.cells_crop_path, (filename + getFOVlabel(row['type']) + \
                                    str(row['type']) + '_' + str(int(x1)) + '_' + str(int(y1)) + '_w_h.png'))
                    crop_img = self.crop_fov2(img, cell_path, x1, y1, x2, y2, sign = 1)
                    roi = [x1, y1, x2, y2]
                    cell_type, fov_type = str(row['type']), get_fov_type(str(row['type']))
                    npy_path = os.path.join(self.cells_npy_path, '{}_{}_{}_{}_{}.npy'.format(filename, x1, y1, x2, y2))
                    masked_path = os.path.join(self.cells_crop_masked, '{}_{}_{}_{}_{}_{}_{}.png'.format(filename, fov_type, cell_type, x1, y1, x2, y2))
                    self.processing_img(crop_img, npy_path, masked_path, expand_side = 1)
            if '2' in degug:
                df_org = pd.read_csv(csv_org_path) # 原始csv
                for index_org, row_org in df_org.iterrows():
                    x, y = row_org['X'], row_org['Y']
                    cell_path = os.path.join(self.cells_crop_path, (filename + getFOVlabel(row_org['Type']) + \
                                    str(row_org['Type']) + '_' + str(int(x)) + '_' + str(int(y)) + '_w_h.png'))
                    crop_fov(img, cell_path, int(x), int(y), side = 55, sign = 1)
            if '3' in degug:
                df_seg = pd.read_csv(csv_seg_path) # 裁减csv
                for index_seg, row_seg in df_seg.iterrows():
                    x1,x2, y1,y2 = row_seg['x1'], row_seg['x2'],row_seg['y1'],row_seg['y2']
                    y = int((x1+x2)/2)
                    x = int((y1+y2)/2)
                    cell_path = os.path.join(self.cells_crop_path, (filename + getFOVlabel(row['type']) + \
                                    str(int(x)) + '_' + str(int(y)) + '_w_h.png'))
                    crop_fov(img, cell_path, int(x), int(y), side = 60, sign = 1)
            #cv2.imwrite(imgpath + '_abc.png', img)
        return

if __name__ == '__main__':
    c = cropper('./')
    c.crop_fovs()