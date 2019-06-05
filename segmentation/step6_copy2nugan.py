import os
import parser
import glob
import pandas as pd
import shutil

from sklearn.model_selection import StratifiedKFold, train_test_split


class NPDataDivider():
    def __init__(self, origin_dir,  csv_dir, npy_dir, output_dir, data_type, pattern, train_test_split):
        self.df = pd.read_csv(csv_dir)
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
        print(self.org_df)
        
    def copy_original(self, org_df, path_fix):
        original_dir = os.path.join(self.output_dir, 'original')
        pos_dir = os.path.join(original_dir, 'positive{}_images'.format(path_fix))
        neg_dir = os.path.join(original_dir, 'negative{}_images'.format(path_fix))
        
        if not os.path.exists(pos_dir):
            os.makedirs(pos_dir)
        if not os.path.exists(neg_dir):
            os.makedirs(neg_dir)
            
        for _, row in org_df.iterrows():
            folder = row['folder']
            dst_name = folder[:-7]
            src = row['org_path']
            fov_type = self.df.loc[self.df['folder']==folder, 'FOV_type'].values[0]
            #print(fov_type)
            if fov_type != 0:
                dst = os.path.join(pos_dir, dst_name)
                shutil.copy(dst=dst, src=src)
            else:
                dst = os.path.join(neg_dir, dst_name)
                shutil.copy(dst=dst, src=src)
    
    def copy_npy(self, org_df, path_fix):
        npy_dir = os.path.join(self.output_dir, 'segmented')
        pos_dir = os.path.join(npy_dir, 'positive{}_npy/160'.format(path_fix))
        neg_dir = os.path.join(npy_dir, 'negative{}_npy/160'.format(path_fix))
        
        if not os.path.exists(pos_dir):
            os.makedirs(pos_dir)
        if not os.path.exists(neg_dir):
            os.makedirs(neg_dir)
        
        for _, row in org_df.iterrows():
            folder = row['folder']
            file_name = folder.split('.')[0] + '.npy'
            src = os.path.join(self.npy_dir, file_name)
            fov_type = self.df.loc[self.df['folder']==folder, 'FOV_type'].values[0]
            #print(fov_type)
            if fov_type != 0:
                dst = os.path.join(pos_dir, file_name)
                shutil.copy(dst=dst, src=src)
            else:
                dst = os.path.join(neg_dir, file_name)
                shutil.copy(dst=dst, src=src)
    
    def train_test_split(self):
        if len(self.df) <= 0:
            train_org, test_org = train_test_split(self.org_df, test_size=0.2,
                                                shuffle=True, random_state=10)
        else:
            df = pd.merge(self.org_df, self.df, how='left', on='folder')
            #import pdb; pdb.set_trace()
            print(df)
            y = df['FOV_type']
            train_org, test_org, _, _ = train_test_split(self.org_df, y, test_size=0.2,
                                                shuffle=True,stratify=y, random_state=10)
        return train_org, test_org
        
                
    def copy(self):
        if self.split_flag:
            train_org, test_org = self.train_test_split()
        else:
            train_org = self.org_df
            test_org = None
            
            
        #have annotated informations, we can define the pos & neg fov
        if len(self.df) > 0:
            print("Found annotation, copy file with positive & negative labels")
            self.copy_original(train_org, '')
            self.copy_npy(train_org, '')
            if test_org is not None:
                self.copy_original(test_org, '_test')
                self.copy_npy(test_org, '_test')
                
        else:
            print("No annotation file found, just copy the files to the output dir")
            #just copy the original and npy to the dest dir
            #copy images
            folders = self.org_df['folder']
            images_dir = os.path.join(self.output_dir, 'original/images')
            npy_dir = os.path.join(self.output_dir, 'segmented/npy/160')
            if not os.path.exists(images_dir):
                os.makedirs(images_dir)
            if not os.path.exists(npy_dir):
                os.makedirs(npy_dir)
            for folder in folders:
                dst_name = folder[:-7]
                src = self.org_df.loc[self.org_df['folder']==folder, 'org_path'].values[0]
                dst = os.path.join(images_dir, dst_name)
                shutil.copy(dst=dst, src=src)
            
                npy_name = folder.split('.')[0] + '.npy'
                src = os.path.join(self.npy_dir, npy_name)
                dst = os.path.join(npy_dir, npy_name)
                shutil.copy(dst=dst, src=src)
            



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
        
    