# -*- coding: utf-8 -*-
import shutil
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from scipy.misc import imread, imresize

CLASS_MAP = {
    0: 'Norm',
    1: 'LSIL',
    2: 'HSIL',
    3: 'HPV',
    4: 'NILM',
    5: 'SCC',
    6: 'ASCUS',
    7: 'ASCH',
    8: 'AGC',
    9: 'AIS',
    10:'ADC',
    11:'T',
    12:'M',
    13:'HSV'
}
NILM_TYPE = [0, 4, 11, 12, 13]
CROP_DIR = 'crops'
COLUMNS = ['folder','point','type']



def show_statics(df,classes):
    #print(df.head())
    folders = df['folder'].unique()
    print("Total images: "+ str(len(folders))+'\n')
    print("Total cells :" + str(len(df)))
    for i in CLASS_MAP.keys():
        print("Number of {} cells:{}".format(CLASS_MAP[i],np.sum(df['type']==i)))
        if i == len(CLASS_MAP.keys())-1:
            print('===================')
    print('========================')
    for i in CLASS_MAP.keys():
        fov = df.loc[df['FOV_type']==i, 'folder'].unique()
        print("Number of {} FOVs:{}".format(CLASS_MAP[i],len(fov)))
    print('\n')

def get_rest_segs(folder, data_root, fov_type, picked_segs):
    seg_path = os.path.join(data_root, folder, CROP_DIR)
    files = os.listdir(seg_path)
    rest_segs = [ int(file.split('.')[0]) for file in files if int(file.split('.')[0]) not in picked_segs]
    #print(rest_segs[:5])
    rest_segs_df = pd.DataFrame(columns=COLUMNS)
    if len(rest_segs) != 0:
        rest_segs_df['point'] = rest_segs
        rest_segs_df['folder'] = folder
        rest_segs_df['FOV_type'] = fov_type
        rest_segs_df['path'] = rest_segs_df[['folder','point']].apply(lambda x: os.path.join(data_root,
                                                                x['folder'],
                                                                CROP_DIR,
                                                                str(x['point'])+'.png'),
                                            axis=1)

        rest_segs_df['type'] = 0
    else:
        print('All cells in ' + folder + ' are labeled.')
    return rest_segs_df

def getlistnum(li):
    li = list(li)
    set1 = set(li)
    dict1 = {}
    types_remove = []
    for item in set1:
        dict1.update({item:li.count(item)})
        if(li.count(item)) < 2:
            types_remove.append(item)
    return dict1, types_remove

def train_test_from_labelfile(file_list, seg_dir, MORE_NORM, TRAIN_TEST_SPLIT):
    fd = open(file_list,'r')
    content = eval(fd.read())

    df = pd.DataFrame(columns=COLUMNS)

    #convert list file to dataframe
    for folder, label_gt in content:
        pos = False
        neg = False
        df_temp = pd.DataFrame([range(len(COLUMNS))],columns=COLUMNS)
        df_temp['folder'] = folder
        for label, gt in label_gt:
            label = int(label)
            cell_type = int(gt)
            tmp = df_temp.copy()
            if gt in NILM_TYPE:
                neg = True
                cell_type = 0
            else:
                pos = True
            check = df.loc[(df['folder']==folder) & (df['point']==label)]
            if len(check) == 0:
                tmp[['point','type']]=[label,cell_type]
                df = df.append(tmp,ignore_index=True)
            else:
                print("Multiple labeled cells in {}, Label:{}, Type:{}".format(folder, label, cell_type))

    mapping = df[['folder', 'type']].groupby(['folder']).max()
    mapping.columns=['FOV_type']
    df = df.merge(mapping, on='folder')

    df['path'] = df[['folder','point']].apply(lambda x: os.path.join(seg_dir,
                                                                x['folder'],
                                                                CROP_DIR,
                                                                str(x['point'])+'.png'),
                                              axis=1)
    df['point'] = df['point'].astype(np.int32)
    df['type'] = df['type'].astype(np.int32)
    print(df.info())

    #debug
    for_tst_df = df[['folder', 'path']].groupby('path').count()
    assert len(df) == len(df['path'].unique()), "DF has multi labeled samples. "
    show_statics(df,CLASS_MAP)

    #add normal cells
    if MORE_NORM:
        norm_fov = df.loc[df['FOV_type']==0, 'folder'].unique()
        tmp_df = pd.DataFrame()
        if len(norm_fov) == 0:
            print("No Normal FOVs for more normal cells. Please check the dataset manully.")
        else:
            for folder in norm_fov:
                picked_segs = df.loc[(df['folder']==folder)]['point'].values
                rest_seg_df = get_rest_segs(folder, seg_dir, 0, picked_segs)
                tmp_df = tmp_df.append(rest_seg_df, ignore_index=True)
        print(tmp_df)
        df = df.append(tmp_df, ignore_index=True)

    if TRAIN_TEST_SPLIT:
        y = df['type']
        #FIXME: remove raws which count(FOV_type) < 2 ??
        #count of y must >= 2
        static, remove_arr = getlistnum(y)
        org_df = df[~df['type'].isin(remove_arr)]
        y = org_df['type']

        #FIXME: many be nan ??
        #remove all raws which FOV_type=nan
        y = y.dropna(axis=0,how='all')

        y = y.values
        train_set, test_set, _, _ = train_test_split(org_df, y, test_size=0.2,
                                                shuffle=True, stratify=y, random_state=10)
    else:
        train_set = df
        test_set = None

    return train_set, test_set

def copy_data_by_type(df,dst_dir):
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)
    gt = CLASS_MAP.keys()

    for i, t in enumerate(gt):
        tmp_df = df.loc[df['type']==t]
        path = os.path.join(dst_dir, CLASS_MAP[i])
        if not os.path.exists(path):
            os.mkdir(path)
        for _, row in tmp_df.iterrows():
            src_path = row['path']
            names = src_path.split('/')[-3] + '_' + src_path.split('/')[-1]
            dst_path = os.path.join(path,names)
            if os.path.exists(src_path):
                shutil.copy(src_path, dst_path)
            else:
                print("src_path not exist: {}".format(src_path))

def gen_npy(df, dest_dir, npy_fn):
    '''
    npy_fn: npy file name
    '''
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    gt = CLASS_MAP.keys()
    X = np.ndarray(shape=(0,32,32,3))
    Y = np.ndarray(shape=(0,1))
    for i, t in enumerate(gt):
        files = df.loc[df['type']==t, 'path'].values
        for file in files:
            image = imread(file)
            resize_image = imresize(image, [32, 32], interp='nearest')
            x = np.array([resize_image])
            #print(np.shape(x))
            X = np.append(X, x, axis=0)
        Y = np.append(Y, t*np.ones((len(files), 1)), axis=0)

    np.save(os.path.join(dest_dir, 'X_' + npy_fn +'.npy'), X)
    np.save(os.path.join(dest_dir, 'Y_' + npy_fn +'.npy'), Y)

#python3 step5_gendata.py --annot_path datasets/classify/annot_out/annotation_default.txt --seg_dir datasets/classify
#                         --output_dir datasets/classify/train_datasets --train_test_split
def step5_gendatav2(annot_file, seg_dir, output_dir, TRAIN_TEST_SPLIT):
    MORE_NORM = False
    batch_id = 'default'
    PATTERN = '*.png'

    CLASSES = CLASS_MAP.values()

    output_dir = os.path.join(output_dir, batch_id)
    dataset_dir = os.path.join(output_dir, 'dataset')
    train_dir = os.path.join(dataset_dir, 'train')
    test_dir = os.path.join(dataset_dir, 'test')
    npy_dir = os.path.join(output_dir, 'npy')
    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    if not os.path.exists(npy_dir):
        os.makedirs(npy_dir)

    if not os.path.exists(annot_file):
        print("标注文件%s不存在,退出..." % annot_file)
        exit(0)

    train_set, test_set = train_test_from_labelfile(annot_file, seg_dir, MORE_NORM, TRAIN_TEST_SPLIT)

    if (train_set is not None) and (len(train_set) >0) :
        assert len(train_set) == len(train_set['path'].unique()),"Train to csv has multi sampled data"
        print("==================================")
        print("=======Train set summary==========")
        print("Total cells in train set:" + str(len(train_set))+'\n')
        show_statics(train_set,CLASSES)

        copy_data_by_type(train_set, train_dir)
        gen_npy(train_set, npy_dir, 'train')

    if (test_set is not None) and (len(test_set) >0) :
        assert len(test_set) == len(test_set['path'].unique()),"Train to csv has multi sampled data"
        print("==================================")
        print("=======Test set summary==========")
        print("Total cells in test set:" + str(len(test_set))+'\n')
        show_statics(test_set,CLASSES)

        copy_data_by_type(test_set, test_dir)
        gen_npy(test_set, npy_dir, 'test')

    if (train_set is not None):
        train_set.to_csv(output_dir+'/train_set.csv', index=False)
    if test_set is not None:
        test_set.to_csv(output_dir+'/test_set.csv', index=False)
