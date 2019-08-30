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

def crop_fov(img, cells_crop_file_path, x, y, side, sign):
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
    if sign == 1:
        cropped = img[y1:y2,x1:x2,:]
        scipy.misc.imsave(cells_crop_file_path, cropped)
    color = []
    if side == 50:
        color = [0,255,0]
    elif side == 55:
        color = [255,0,0]
    else:
        color = [0,0,255]
    cv2.rectangle(img, (x1, y1), (x2, y2), color,2)
    return

def crop_fovs(original_img_path, cells_rois_path, cells_crop_path):
    imgs = get_image_lists(original_img_path)
    print(imgs)
    for i in imgs:
        imgpath = os.path.join(original_img_path, i)
        (filepath, filename) = os.path.split(imgpath)

        csv_path = os.path.join(cells_rois_path, (filename + '_.csv_and.csv')) # 交集
        print(csv_path)
        csv_org_path = imgpath[:-3] + 'csv' # 医生csv
        csv_seg_path = csv_path[:-8]
        if not os.path.exists(csv_path):
            print("not found %s" % csv_path)
            continue
        img = scipy.misc.imread(imgpath)
        df1 = pd.read_csv(csv_path) # 交集csv
        for index, row in df1.iterrows():
            x, y = row['x'], row['y']
            cell_path = os.path.join(cells_crop_path, (filename + '_n_' + \
                            str(row['type']) + '_' + str(int(x)) + '_' + str(int(y)) + '_w_h.png'))
            crop_fov(img, cell_path, int(x), int(y), side = 50, sign = 1)
        df_org = pd.read_csv(csv_org_path) # 原始csv
        for index_org, row_org in df_org.iterrows():
            x, y = row_org['X'], row_org['Y']
            crop_fov(img, cell_path, int(x), int(y), side = 55, sign = 0)
        df_seg = pd.read_csv(csv_seg_path) # 裁减csv
        for index_seg, row_seg in df_seg.iterrows():
            x1,x2, y1,y2 = row_seg['x1'], row_seg['x2'],row_seg['y1'],row_seg['y2']
            y = int((x1+x2)/2)
            x = int((y1+y2)/2)
            crop_fov(img, cell_path, int(x), int(y), side = 60, sign = 0)
        cv2.imwrite(imgpath + '_abc.png', img)
    return

if __name__ == '__main__':
    crop_fovs('origin_imgs/', 'cells/rois/', 'cells/crop/')
