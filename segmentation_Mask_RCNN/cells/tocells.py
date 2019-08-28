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

path = os.getcwd() + '/' + 'cells'
path_FOV = os.path.join(path, 'RIOS')
path_csv = os.path.join(path, 'RIOS')
path_cell = os.path.join(path, 'crop')
root_FOV = os.path.join(path_FOV, 'IMG032x018.JPG')
root_csv = os.path.join(path_csv, 'IMG032x018.JPG.csv.csv')

g_img = None

def saveToMysql(row):
    sides = [50]
    img = g_img
    limit_x = img.shape[1]
    limit_y = img.shape[0]
    for side in sides:
        x1 = row.X - side
        x2 = row.X + side
        y1 = row.Y - side
        y2 = row.Y + side
        x1 = min(limit_x, max(0, x1))
        x2 = max(x1+1, min(limit_x, x2))
        y1 = min(limit_y, max(0, y1))
        y2 = max(0, min(limit_y, y2))
        cropped = img[y1:y2,x1:x2,:]
        new_crop_parh = path_cell + '/' + str(row.Type) + '_' + str(row.X) + '_' + str(row.Y) + '_' +str(x2-x1) + '_' + str(y2-y1) + '_' + str(side) + '.png'
        scipy.misc.imsave(new_crop_parh , cropped)

if __name__ == '__main__':
        df = pd.read_csv(root_csv)
        print(df)
        print(type(df))
        df['img'] = root_FOV
        g_img = scipy.misc.imread(root_FOV)
        df.apply(saveToMysql, axis=1)

