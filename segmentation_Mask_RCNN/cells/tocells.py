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

def crop_fov(img, cells_crop_file_path, x, y):
    sides = [50]
    limit_x = img.shape[1]
    limit_y = img.shape[0]
    print(limit_x, limit_y)
    for side in sides:
        x1 = x - side
        x2 = x + side
        y1 = y - side
        y2 = y + side
        x1 = int(min(limit_x, max(0, x1)))
        x2 = int(max(x1+1, min(limit_x, x2)))
        y1 = int(min(limit_y, max(0, y1)))
        y2 = int(max(0, min(limit_y, y2)))
        print(y1,y2,x1,x2)
        #FIXME: 这里算的不对
        cropped = img[y1:y2,x1:x2,:]
        scipy.misc.imsave(cells_crop_file_path, cropped)
        print(cells_crop_file_path)
    return

def crop_fovs(original_img_path, cells_rois_path, cells_crop_path):
    imgs = get_image_lists(original_img_path)
    print(imgs)
    for i in imgs:
        imgpath = os.path.join(original_img_path, i)
        (filepath, filename) = os.path.split(imgpath)

        csv_path = os.path.join(cells_rois_path, (filename + '_.csv_and.csv'))
        if not os.path.exists(csv_path):
            print("not found %s" % csv_path)
            continue
        img = scipy.misc.imread(imgpath)
        df1 = pd.read_csv(csv_path)
        for index, row in df1.iterrows():
            x, y = row['x'], row['y']
            cell_path = os.path.join(cells_crop_path, (filename + '_n_' + \
                            str(row['type']) + '_' + str(int(x)) + '_' + str(int(y)) + '_w_h.pg'))
            crop_fov(img, cell_path, int(x), int(y))
    return

if __name__ == '__main__':
    crop_fovs('origin_imgs/', 'cells/rois/', 'cells/crop/')
