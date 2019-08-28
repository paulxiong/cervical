# !/usr/bin/python
# -*- coding: UTF-8 -*-
import math
import pandas as pd
import numpy as np
import os
import time
import scipy.misc
from shutil import copyfile
from PIL import Image
import shutil
from pandas.core.frame import DataFrame
'''
path_ojb = os.getcwd()
path_org = os.path.join(path_ojb, 'orignal_img')
list_org = os.listdir(path_org)
path_orgimg = []
path_orgcsv = []
for n in list_org:
    print(n[-3:])
    if n[-3:] == 'JPG':
        path_orgimg.append(path_org + '/' + n)
    elif n[-3:] == 'csv'
        path_orgcsv.append(path_org + '/' + n)
    else:
        raise ErrorName(n)
path_segcsv = os.path.join(path_ojb, 'cells', 'RIOS')
list_segcsv = os.listdir(path_segcsv)
'''

path_func2 = os.path.join(path_ojb, 'cells')
path_orgcsv = os.path.join(path_func2, 'RIOS')
path_cell = os.path.join(path_func2, 'crop')
root_orgcsv = os.path.join(path_orgcsv, 'IMG032x018.csv')
root_segcsv = os.path.join(path_orgcsv, 'IMG032x018.JPG.csv')
root_savecsv = os.path.join(path_orgcsv, 'IMG032x018.JPG.csv.csv')
limit = 900
df_org = pd.read_csv(root_orgcsv, usecols = [0, 2, 3])
print(df_org)
df_seg = pd.read_csv(root_segcsv)
save_orgcsv = []
for index_org, row_org in df_org.iterrows():
    point_org_x = row_org['X']
    point_org_y = row_org['Y']
    L_temp_all = []
    for inde_seg, row_seg in df_seg.iterrows():
        x1 = row_seg['x1']
        x2 = row_seg['x2']
        y1 = row_seg['y1']
        y2 = row_seg['y2']
        point_seg_x = (x1 + x2)/2
        point_seg_y = (y1 + y2)/2
        print(">>>:",point_seg_x, point_seg_y)
        L_temp = np.sqrt((np.square(point_org_x - point_seg_x)) + np.square(point_org_y - point_seg_y))
        print("+++",L_temp)
        L_temp_all.append(L_temp)
    print(min(L_temp_all))
    if min(L_temp_all) < limit:
        print("ooo",row_org)
        save_orgcsv.append(row_org)
save_orgcsv = DataFrame(save_orgcsv)
save_orgcsv.to_csv(root_savecsv)

