# !/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import pandas as pd
import glob
import shutil
import re

dst_path = './picks'
if not os.path.exists(dst_path):
    os.makedirs(dst_path)

csv_files = glob.glob('./*.csv')
csv_files = [ csv for csv in csv_files if re.search(r'.*\(.*\).*', os.path.basename(csv)) is None ]
print(csv_files)

#pat = re.search('/([0-9]{7}', os.getcwd())
#if pat is None:
#    print("匹配不到Slide编号，随机生成中...")
#    slide_name = str(np.random.randint(5000)).zfill(7)
#    print("随机编号： %s" % slid_name)
#else:
#    slide_name = pat.group(1)
#    print("匹配到Slide编号：%s" % slide_name)


CSV_NILM_TYPE = [1, 5, 12, 13, 14]

for csv in csv_files:
    name = os.path.splitext(os.path.basename(csv))[0]
    jpg_file = name + '.JPG'
    df = pd.read_csv(csv)
    df['Type'] = df['Type'].apply(lambda x: x if x not in CSV_NILM_TYPE else 0)
    fov_type = df['Type'].max()
    if fov_type != 0:
        print("找到一个异常FOV, %s" % name)
#        dst_name = slide_name + '_' + jpg_file
        src = os.path.join('./Images', jpg_file)
#        dst = os.path.join(dst_path, dst_name)
        shutil.copy(src, dst_path)
        shutil.copy(csv, dst_path)
