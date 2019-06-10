# !/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import pandas as pd
import glob
import shutil

dst_path = './picks'
if not os.path.exists(dst_path):
    os.makedirs(dst_path)

csv_files = glob.glob('./*.csv')


CSV_NILM_TYPE = [1, 5, 12, 13, 14]

for csv in csv_files:
    name = os.path.splitext(os.path.basename(csv))[0]
    jpg_file = name + '.JPG'
    df = pd.read_csv(csv)
    df['Type'] = df['Type'].apply(lambda x: x if x not in CSV_NILM_TYPE else 0)
    fov_type = df['Type'].max()
    if fov_type != 0:
        print("找到一个异常FOV, %s" % name)
        src = os.path.join('./', jpg_file)
        shutil.copy(src, dst_path)
        shutil.copy(csv, dst_path)
