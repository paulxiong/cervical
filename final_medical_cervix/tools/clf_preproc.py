import sys
print(sys.version)

import shutil
import os
import numpy as np
import pandas as pd
import re
from sklearn.model_selection import StratifiedKFold, train_test_split


def show_statics(df,classes):
    #print(df.head())
    folders = df['folder'].unique()
    print("Total images: "+ str(len(folders))+'\n')
    print("Total cells :" + str(len(df)))
    for i in range(len(classes)):
        print("Number of {} cells:{}".format(classes[i],np.sum(df['type']==i)))
        if i ==0:
            print('===================')
    print("========================")
    for i in range(1,len(classes)):
        count = np.sum((df['FOV_type']==i)&(df['type']==0))
        print("Number of {} Norm cells:{}".format(classes[i],count))
    print('========================')
    tmp_df = df[['folder','FOV_type']].groupby(['FOV_type','folder']).count().reset_index()
    for i in range(1,len(classes)):
        print("Number of {} FOVs:{}".format(classes[i],np.sum(tmp_df['FOV_type']==i)))
    print('\n')

def get_rest_segs(folder, data_root, fov_type, picked_segs):
    seg_path = os.path.join(data_root, folder, CROP_DIR)
    files = os.listdir(CLF_ROOT + seg_path)
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

def copy_data(folder, src_root, dst_root, force=False):
    src_dir = os.path.join(ROOT, src_root, folder)
    dst_dir = os.path.join(CLF_ROOT, dst_root, folder)
    #print(src_dir)
    #print(dst_dir)
    
    if os.path.exists(dst_dir):
        if force:
            print("Force Copy Datasets to %s" % dst_dir)
            os.removedirs(dst_dir)
        else:
            print("Destination exists: %s" % dst_dir)
            return 0
    try:
        shutil.copytree(src_dir, dst_dir)
    except Exception as e:
        print(e)
        #print("Dictionary exists: %s" % dst_dir)
        

def train_test_from_labelfile(file_list, dst_dir):

    fd = open(file_list,'r')
    content = eval(fd.read())

    df = pd.DataFrame(columns=COLUMNS)

    for folder,pos,neg in content:
        pos = set(pos)
        neg = set(neg)
        #copy data
        copy_data(folder,SRC_DATAROOT, dst_dir, force=FORCE_COPY)
        #add norm cell
        df_temp = pd.DataFrame([range(len(COLUMNS))],columns=COLUMNS)
        df_temp['folder'] = folder
        for i,clazz in enumerate(CLASSES[1:]):
            if re.match(clazz,folder):
                cell_type = i+1
                break
        df_temp['FOV_type']=cell_type
    
        for cell in neg:
            tmp = df_temp.copy()
            tmp[['point','type']]=[int(cell),0]
            df = df.append(tmp,ignore_index=True)
        #add ab norm cell
        for cell in pos:
            tmp = df_temp.copy()
            tmp[['point','type']]=[int(cell),cell_type]
            df = df.append(tmp,ignore_index=True)

    #add the file path to images 
    df['path'] = df[['folder','point']].apply(lambda x: os.path.join(dst_dir,
                                                                x['folder'],
                                                                CROP_DIR,
                                                                str(x['point'])+'.png'),
                                              axis=1) 
    df['point'] = df['point'].astype(np.int32)
    df['type'] = df['type'].astype(np.int32)
    print(df.info())

    #debug
    for_tst_df = df[['folder', 'path']].groupby('path').count()
    print("The multi labeled samples:")
    print(for_tst_df.loc[for_tst_df['folder'] != 1].index)
    assert len(df) == len(df['path'].unique()), "DF has multi labeled samples. "
    #debug-end 
    show_statics(df,CLASSES)
    
    #do the splits for FOVs
    tmp_df = df[['folder','FOV_type']].groupby(['FOV_type','folder']).count().reset_index()
    X = tmp_df['folder'].values
    y = tmp_df['FOV_type'].values

    train_fov, test_fov, _, _ =  train_test_split(X, y, test_size=0.2, 
                                              shuffle=True, stratify=y, random_state=10)
    #print(train_fov)
    #print(test_fov)
    train_set = df.loc[df['folder'].apply(lambda x: x in train_fov)]
    test_set = df.loc[df['folder'].apply(lambda x: x in test_fov)]


    #skf = StratifiedKFold(n_splits=6,random_state=1)
    #skf.get_n_splits(X,y)

    #for train_index, test_index in (skf.split(X,y)):
        #for SCC only have 1 FOV, we want to put it into train set.
        #so here we select the only split with SCC in train set
    #    if 'SCC_IMG001x001.png_output' in X[train_index]:
    #        train_set = df.loc[df['folder'].apply(lambda x: x in X[train_index])]
    #        test_set = df.loc[df['folder'].apply(lambda x: x in X[test_index])]
    #        break
    #print(test_index)

    #pick up all normal cells
    tmp_df = pd.DataFrame(columns=COLUMNS)
    #for folder in X[train_index]:
    for folder in train_fov:
        #print(train_set.loc[test_set['folder']==folder]['FOV_type'])
        fov_type = train_set.loc[train_set['folder']==folder]['FOV_type'].values[0]
        #if HSIL or SCC, don't add rest cells for most cells in them are abnormal
        if fov_type in [2,5]:
            if not INC_ABN_UNLABEL:
                continue
        picked_segs = train_set.loc[(train_set['folder']==folder)]['point'].values
        rest_seg_df = get_rest_segs(folder, dst_dir, fov_type, picked_segs)
        tmp_df = tmp_df.append(rest_seg_df, ignore_index=True)
        
    train_set = train_set.append(tmp_df, ignore_index=True)


    #Get the rest normal cells in test set
    #for folder in X[test_index]:
    for folder in test_fov:
        #print(test_set.loc[test_set['folder']==folder]['FOV_type'])
        fov_type = test_set.loc[test_set['folder']==folder]['FOV_type'].values[0]
        #if HSIL or SCC, don't add rest cells for most cells in them are abnormal
        if fov_type in [2,5]:
            if not INC_ABN_UNLABEL:
                continue
        picked_segs = test_set.loc[test_set['folder']==folder]['point'].values
        rest_seg_df = get_rest_segs(folder, dst_dir, fov_type, picked_segs)
        test_set = test_set.append(rest_seg_df, ignore_index=True)

    assert len(test_set['path']) == len(test_set['path'].unique()), test_set.info()
    assert len(train_set['path']) == len(train_set['path'].unique()), train_set
    
    return train_set, test_set







if __name__ == '__main__':
    ROOT = '../'
    #LABELFILE_PATH = ['./listfile5.txt', './listfile_2019.txt']
    
    LABELFILE_PATH = ['./listfile_2019.txt']
    SRC_DATAROOT = 'datasets/classify'
    DST_DATAROOT = ['datasets/classify_recrop_2019']
    
    CROP_DIR = 'crops'
    CLF_ROOT = '../src/CLASSIFY/inceptionV3_final_1/'
    TRAINSET_PATH = CLF_ROOT+'input/train_labels.csv'
    #TRAINSET_PATH = CLF_ROOT+'datasets/train_labels_2018.csv'
    TESTSET_PATH = CLF_ROOT+'input/sample_submission.csv'
    #TESTSET_PATH = CLF_ROOT+'datasets/sample_submission_2018.csv'
    
    CLASSES = ['NORM','LSIL_IMG','HSIL','LSIL_HPV','NILM','SCC']
    COLUMNS = ['folder','point','FOV_type','type']
    FORCE_COPY = False
    # add the unlabeled cells in HSIL & SCC FOVs as normal ones(we may use this df for NMI)
    INC_ABN_UNLABEL = False
    #INC_ABN_UNLABEL = True

    train_set = pd.DataFrame()
    test_set = pd.DataFrame()
    
    for labelfile, dest in zip(LABELFILE_PATH, DST_DATAROOT):
        train_df, test_df = train_test_from_labelfile(labelfile, dest)
        train_set = pd.concat([train_set, train_df])
        test_set = pd.concat([test_set, test_df])
    
    
    print("==================================")
    print("=======Train set summary==========") 
    print("Total cells in train set:" + str(len(train_set))+'\n')
    show_statics(train_set,CLASSES)
    print("==================================")
    print("======= Test set summary==========")
    print("Total cells in test set:" + str(len(test_set)))
    show_statics(test_set,CLASSES)
    
    #Generate train set
    train_to_csv = train_set[['path','type']]
    train_to_csv.columns = ['name','positive']
    print(train_to_csv.head())
    assert len(train_to_csv) == len(train_to_csv['name'].unique()),"Train to csv has multi sampled data"
    for name in train_to_csv['name']:
        assert os.path.exists(os.path.join(CLF_ROOT,name)), "File does exists: %s" % name
    train_to_csv.to_csv(TRAINSET_PATH,index=False)
    
    #Generate test set
    test_to_csv = test_set[['path','type']]
    #print(test_set['folder'].unique())
    test_to_csv['positive'] = 0.5
    test_to_csv.columns = ['name','gt','positive']
    print(test_to_csv.head())
    assert len(test_to_csv) == len(test_to_csv['name'].unique()),"Test to csv has multi sampled data"
    for name in test_to_csv['name']:
        assert os.path.exists(os.path.join(CLF_ROOT,name)), "File does not exists %s" % name
    test_to_csv.to_csv(TESTSET_PATH,index=False)




