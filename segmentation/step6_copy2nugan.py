# -*- coding: utf-8 -*-
import os
import parser
import glob
import pandas as pd
import shutil
#import numpy as np
import re

from sklearn.model_selection import StratifiedKFold, train_test_split


class NPDataDivider():
    def __init__(self, origin_dir,  csv_dir, npy_dir, output_dir, data_type, pattern, train_test_split):
        if os.path.exists(csv_dir):
            self.df = pd.read_csv(csv_dir)
        else:
            self.df = pd.DataFrame()
        self.npy_dir = npy_dir
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        assert data_type in ['train', 'test']
        if data_type == 'test':
            self.path_fix = '_test'
        else:
            self.path_fix = ''
        self.pattern = pattern
        self.origin_dir = origin_dir
        self.org_df = None
        self.split_flag = train_test_split
        
    
    def read_origin(self):
        files = glob.glob(os.path.join(self.origin_dir, self.pattern))
        self.org_df = pd.DataFrame({'org_path': files}) 
        def get_folder(path):
            splits = path.split('/')
            if splits[-2] == 'Images':
                return splits[-3] + '_' + splits[-1] + '_output'
            else:
                return splits[-2] + '_' + splits[-1] + '_output'
        self.org_df['folder'] = self.org_df['org_path'].apply(get_folder)
        
    def copy_original_and_npy(self, org_df, path_fix):
        original_dir = os.path.join(self.output_dir, 'original')
        pos_dir = os.path.join(original_dir, 'positive{}images'.format(path_fix))
        neg_dir = os.path.join(original_dir, 'negative{}images'.format(path_fix))
        
        
        npy_dir = os.path.join(self.output_dir, 'segmented')
        npy_pos_dir = os.path.join(npy_dir, 'positive{}npy/160'.format(path_fix))
        npy_neg_dir = os.path.join(npy_dir, 'negative{}npy/160'.format(path_fix))
        
        if not os.path.exists(pos_dir):
            os.makedirs(pos_dir)
        if not os.path.exists(neg_dir):
            os.makedirs(neg_dir)
        if not os.path.exists(npy_pos_dir):
            os.makedirs(npy_pos_dir)
        if not os.path.exists(npy_neg_dir):
            os.makedirs(npy_neg_dir)
            
            
        for _, row in org_df.iterrows():
            folder = row['folder']
            #copy npy
            file_name = folder.split('.')[0] + '.npy'
            src = os.path.join(self.npy_dir, file_name)
            if not os.path.exists(src):
                continue
            if(len(self.df.loc[self.df['folder']==folder, 'FOV_type']) == 0):
                continue
            fov_type = self.df.loc[self.df['folder']==folder, 'FOV_type'].values[0]
            if fov_type != 0:
                dst = os.path.join(npy_pos_dir, file_name)
                shutil.copy(dst=dst, src=src)
            else:
                dst = os.path.join(npy_neg_dir, file_name)
                shutil.copy(dst=dst, src=src)
            
            #copy original
            dst_name = folder[:-7]
            src = row['org_path']
            if fov_type != 0:
                dst = os.path.join(pos_dir, dst_name)
                shutil.copy(dst=dst, src=src)
            else:
                dst = os.path.join(neg_dir, dst_name)
                shutil.copy(dst=dst, src=src)

    def getlistnum(self, li):
        li = list(li)
        set1 = set(li)
        dict1 = {}
        types_remove = []
        for item in set1:
            dict1.update({item:li.count(item)})
            if(li.count(item)) < 2:
                types_remove.append(item)
        return dict1, types_remove

    def train_test_split(self):
        if len(self.df) <= 0:
            train_org, test_org = train_test_split(self.org_df, test_size=0.2,
                                                shuffle=True, random_state=10)
        else:
            df = pd.merge(self.org_df, self.df, how='left', on='folder')
            y = df['FOV_type']
            #FIXME: remove raws which count(FOV_type) < 2 ??
            #count of y must >= 2
            static, remove_arr = self.getlistnum(y)
            org_df = df[~df['FOV_type'].isin(remove_arr)]
            y = org_df['FOV_type']

            #FIXME: many be nan ??
            #remove all raws which FOV_type=nan
            y = y.dropna(axis=0,how='all')

            train_org, test_org, _, _ = train_test_split(org_df, y, test_size=0.2,
                                                shuffle=True,stratify=y, random_state=10)
        return train_org, test_org
    
    def copy_no_annotaions(self, org_df, path_fix):   
        if org_df is None:
            return None
        folders = org_df['folder']
        types = [re.search(r'(.*)_([PN])_', folder).group(2) if re.search(r'(.*)_([PN])_', folder) else 'UNK' for folder in folders]
        
        
        images_dir = os.path.join(self.output_dir, 'original/images')
        npy_dir = os.path.join(self.output_dir, 'segmented/npy/160')
        
        p_images_dir = os.path.join(self.output_dir, 'original/positive{}images'.format(path_fix))
        p_npy_dir = os.path.join(self.output_dir, 'segmented/positive{}npy/160'.format(path_fix))
        
        n_images_dir = os.path.join(self.output_dir, 'original/negative{}images'.format(path_fix))
        n_npy_dir = os.path.join(self.output_dir, 'segmented/negative{}npy/160'.format(path_fix))
        
        for folder, t in zip(folders,types):
            npy_name = folder.split('.')[0] + '.npy'
            src = os.path.join(self.npy_dir, npy_name)
            if not os.path.exists(src):
                continue
            if t == 'N':
                print("检测到类型为正常的图片：%s" % folder)
                if not os.path.exists(n_images_dir):
                    os.makedirs(n_images_dir)
                if not os.path.exists(n_npy_dir):
                    os.makedirs(n_npy_dir)
                tmp_npy_dir = n_npy_dir
                tmp_img_dir = n_images_dir
            elif t == 'P':
                print("检测到类型为异常的图片：%s" % folder)
                if not os.path.exists(p_images_dir):
                    os.makedirs(p_images_dir)
                if not os.path.exists(p_npy_dir):
                    os.makedirs(p_npy_dir)
                tmp_npy_dir = p_npy_dir
                tmp_img_dir = p_images_dir
            elif t == 'UNK':
                if not os.path.exists(images_dir):
                    os.makedirs(images_dir)
                if not os.path.exists(npy_dir):
                    os.makedirs(npy_dir)
                tmp_npy_dir = npy_dir
                tmp_img_dir = images_dir
                
            
            dst = os.path.join(tmp_npy_dir, npy_name)
            shutil.copy(dst=dst, src=src)
            
            dst_name = folder[:-7]
            src = org_df.loc[org_df['folder']==folder, 'org_path'].values[0]
            dst = os.path.join(tmp_img_dir, dst_name)
            shutil.copy(dst=dst, src=src)
        
                
    def copy(self):
        if self.split_flag:
            train_org, test_org = self.train_test_split()
        else:
            train_org = None
            test_org = self.org_df
            
        print("开始生成文件...")
        #have annotated informations, we can define the pos & neg fov
        if len(self.df) > 0:
            #print("Found annotation, copy file with positive & negative labels")
            print("发现标注文件， 把文件拷贝到正常/异常文件夹中...")
            if train_org is not None:
                self.copy_original_and_npy(train_org, '_')
            
            self.copy_original_and_npy(test_org, '_test_')
                
        else:
            #print("No annotation file found, just copy the files to the output dir")
            print("未发现标注文件")
            #just copy the original and npy to the dest dir
            #copy images
            
            if train_org is not None:
                self.copy_no_annotaions(train_org, '_')
            
            self.copy_no_annotaions(test_org, '_test_')
            
        print("生成完成...")    



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Cervix Cancer Auto Annotation')
        
    parser.add_argument('--origin_dir', required=True,
                        metavar="/path/to/original/FOV/images",
                        help='path to original fovs')
    parser.add_argument('--csv_dir', 
                        default='./datasets/classify/train_datasets',
                        metavar="/path/to/divided/train/test/csv/file",
                        help='path to train test csv file')
    parser.add_argument('--npy_dir', required=True,
                        metavar="/path/to/npy/segmentation/results",
                        help='path to original fovs')
    parser.add_argument('--output_dir', 
                        default='./datasets/classify/data',
                        metavar="/path/to/save/dataset",
                        help='path to train test csv file')
    parser.add_argument('--pattern',
                        default='*.png',
                        metavar="Original file pattern")
    parser.add_argument('--train_test_split', action='store_true',
                        help='divide data into train and test')
                        
    args = parser.parse_args()
    origin_dir = args.origin_dir
    csv_dir = args.csv_dir
    npy_dir = args.npy_dir
    output_dir = args.output_dir
    pattern = args.pattern
    split_flag= args.train_test_split
    
    #train_csv = os.path.join(csv_dir, 'train_set.csv')
    #test_csv = os.path.join(csv_dir, 'test_set.csv')
    
    copier = NPDataDivider(origin_dir, csv_dir, npy_dir, output_dir, 'train', pattern, split_flag)
    copier.read_origin()
    copier.copy()
        
    
