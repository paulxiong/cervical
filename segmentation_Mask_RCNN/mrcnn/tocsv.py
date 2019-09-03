# !/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd
import numpy as np
import os
import time
def get_csv_lists(original_img_path):
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
        if not ext in ['.csv']:
            print(">>> unexpected file: %s, must be csv" % path1)
        else:
            image_list.append(i)
    if allfiles_num > len(image_list):
        print(">>> %d files/folder ignored !!" % (allfiles_num - len(image_list)))
    return image_list

def get_fileName_fileExt(filename):
    (shotname,extension) = os.path.splitext(filename)
    return shotname, extension

def get_cells_rois_csv(cells_rois_path, original_csv_name):
    filename, _ = get_fileName_fileExt(original_csv_name)
    csvfilename = filename + '.JPG_.csv'
    cells_rois_csv = os.path.join(cells_rois_path, csvfilename)
    if not os.path.exists(cells_rois_csv):
        print("not found %s" % cells_rois_csv)
        return None
    return cells_rois_csv

def compare_roi(x, y, Type, csv_path):
    org_x, org_y, _type, x1, x2, y1, y2 = None, None, None, None, None, None, None
    df2 = pd.read_csv(csv_path)
    org_num = df2.shape[0]
    limit = 300
    min_distance = 1000000
    for index, row in df2.iterrows():
        x_center = int((row['x2'] + row['x1']) / 2)
        y_center = int((row['y2'] + row['y1']) / 2)
        L_temp = np.sqrt((np.square(x_center - x)) + np.square(y_center - y))
        if L_temp < min_distance:
            min_distance = L_temp
            org_x, org_y, _type, x1, x2, y1, y2 = x, y, int(Type), int(row['x1']), int(row['x2']), int(row['y1']), int(row['y2'])
    if min_distance < limit:
        return True, org_x, org_y, _type, x1, x2, y1, y2
    return False, org_x, org_y, _type, x1, x2, y1, y2

def save_rois_as_csv(cells_rois_file_path, rois):
    csv_path = cells_rois_file_path + '_and.csv'
    pd_data = pd.DataFrame(rois, columns=['x', 'y', 'type', 'x1', 'x2', 'y1', 'y2'])
    save_file = pd_data.to_csv(csv_path, quoting = 1, mode = 'w',
                index = False, header = True)
    return

def get_trusted_labels(original_csv_path, cells_rois_path):
    #第一步查找预测的csv和医生的csv
    original_csv_names = get_csv_lists(original_csv_path)

    step, total_steps = 0, len(original_csv_names)
    #比较求交集
    for i in original_csv_names:
        print("step %s/%d" % (step, total_steps))
        step = step + 1
        org_csv_path = os.path.join(original_csv_path, i) # 原始csv
        csv_path = get_cells_rois_csv(cells_rois_path, i) # 切割csv

        if csv_path is None or not os.path.exists(csv_path):
            print('not found %s ' % csv_path)
            continue
        rois = []
        df1 = pd.read_csv(org_csv_path)
        rois_label_num = df1.shape[0]
        org_num = 0
        cnt = 0
        for index, row in df1.iterrows(): # 遍历切割csv
            ret, org_x, org_y, _type, x1, x2, y1, y2 = compare_roi(row['X'], row['Y'], row['Type'], csv_path)
            if ret is True:
                rois.append([org_x, org_y, _type, x1, x2, y1, y2])
        if len(rois) > 0:
            print("org_label_num=%d  len(rois)=%d org_num=%d" % (rois_label_num, len(rois), org_num))
            save_rois_as_csv(csv_path, rois)

if __name__ == "__main__":
    t1 = time.time()
    get_trusted_labels('origin_imgs/', 'cells/rois/')
    print(time.time() - t1)
