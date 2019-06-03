import numpy as np
import pandas as pd
import cv2
import os
import shutil
from tqdm import tqdm
import glob
import re
import time

from tools_new.annot import get_annot_coordinate, get_central_label, mark_missed_annotation, mark_origin_fov 



def generate_df(annotat_dict, fov_name, class_map):
    dic = {'coord': [], 'type':[], 'fov_name':[]}
    for gt in annotat_dict.keys():
        coords = annotat_dict[gt]
        cnt = len(coords)
        dic['coord'] += coords
        dic['type'] += [class_map[gt]] * cnt
        dic['fov_name'] += [fov_name] * cnt
            
    df = pd.DataFrame(dic)
    return df

def show_statistics(df):
    total = len(df)
    cnt_img = len(df['fov_name'].unique())
    avg = float(total)/cnt_img
    lsil_cnt = len(df.loc[df['type']=='LSIL'])
    hsil_cnt = len(df.loc[df['type']=='HSIL'])
    hpv_cnt = len(df.loc[df['type']=='LSIL_HPV'])
    scc_cnt = len(df.loc[df['type']=='SCC'])
    
    print("Total: %s" % total)
    print("Num of Fov: %s" % cnt_img)
    print("Annotation per image: %f " % avg)
    print("LSIL Num: %s " % lsil_cnt)
    print("HSIL Num: %s " % hsil_cnt)
    print("HPV Num: %s " % hpv_cnt)
    print("SCC Num: %s " % scc_cnt)
    
    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Cervix Cancer Auto Annotation')
        
    parser.add_argument('--origin_dir', required=True,
                        metavar="/path/to/original/FOV/images",
                        help='path to original fovs')
    parser.add_argument('--seg_dir', 
                        default='./datasets/classify/',
                        metavar="/path/to/segment/result",
                        help='path to segmentation result')
    parser.add_argument('--output_dir', 
                        metavar="/path/to/output/result",
                        default='./step4_out',
                        help='path to annotation list file')
    parser.add_argument('--pattern',
                        default='*.png',
                        metavar="Original file pattern")
    parser.add_argument('--mark_origin',
                        default=True,
                        metavar="Whether to output a marked original fov")
    parser.add_argument('--batch_id',
                        default='default',
                        metavar="Whether to output a marked original fov")
    
    debug=False                    
    args = parser.parse_args()
    print(args)
    ORIGIN_DIR = args.origin_dir
    SEG_DIR = args.seg_dir
    OUTPUT_DIR = args.output_dir
    PATTERN = args.pattern
    
    if args.output_dir is None:
        output_path = './annot_out'
    else:
        output_path = args.output_dir
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    #id = time.time()
    id = args.batch_id
    annotations_name = 'annotation_{}'.format(id)+'.txt'
    #search_pat = os.path.join(ORIGIN_DIR, PATTERN)
    #origin_fovs = glob.glob(search_pat)
    annot_csv = glob.glob(os.path.join(ORIGIN_DIR, '*.csv'))
    
    if len(annot_csv) == 0:
        print('No annotation found,  exit...')
        exit()
    
    #debug = True
    #debug
    #if debug:
    #    debug_path = './debug_annot'
    #    missed_annotat_folder = os.path.join(debug_path, 'annot_fov')
    #    if not os.path.exists(missed_annotat_folder):
    #        os.makedirs(missed_annotat_folder)
        
    
    color_map = {0: (0, 255, 255), #yellow
             1: (0, 255, 0), #Green
             2: (0, 0, 255), #Red
             3: (255, 255, 0), #cyan
             4: (255, 0, 255), #?
             5: (255, 128, 128), #?
             6: (128, 128, 255), #?
             7: (0, 255, 128),
             8: (0, 128, 255),
             9: (128, 0, 255),
             10:(200, 200, 200),
             11: (0, 128, 255),
             12: (128, 0, 255),
             13:(128, 200, 128)
            }
            
    csv_class_map = {
        1: 'Norm',
        2: 'LSIL',
        3: 'HSIL',
        4: 'HPV',
        5: 'NILM',
        6: 'SCC',
        7: 'ASCUS',
        8: 'ASCH',
        9: 'AGC',
        10:'AIS',
        11:'ADC',
        12:'T',
        13:'M',
        14:'HSV'
    }
    
    class_map = {
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
    annotations = []
    missed_df = pd.DataFrame()
    hit_df = pd.DataFrame()
    
    for annot in tqdm(annot_csv):
        org_fov = annot[:-3] + PATTERN.split('.')[-1]
        if not os.path.exists(org_fov):
            print('FOV not exists: {}'.format(org_fov))
            continue
        #prepare dirs
        path_split = annot.split('/')
        slide_name = (path_split[-2] if path_split[-2] != 'Images' else path_split[-3])
        file = slide_name + '_' + os.path.basename(org_fov)
        seg_folder_name = file + '_output'
        
        #load label
        label_mask_path = os.path.join(SEG_DIR, seg_folder_name, 'preview', 'label.png')
        if not os.path.exists(label_mask_path):
            print("label.png did not exists, %s " % label_mask_path)
            continue
        
        label = cv2.imread(label_mask_path, 0)
        #load csv
        df = pd.read_csv(annot)
        
        #get class_centr
        class_centr = {}
        for gt in csv_class_map.keys():
            coords = df.loc[df['Type']==gt, ['X', 'Y']].values
            if len(coords) > 0:
                class_centr[gt-1] = coords
        
        labeled_crops, hit_centr, missed_centr = get_central_label(label, class_centr)
            
        #generate df
        tmp_missed_df = generate_df(missed_centr, file, class_map)
        tmp_hit_df = generate_df(hit_centr, file, class_map)
        
        missed_df = missed_df.append(tmp_missed_df, ignore_index=True)
        hit_df = hit_df.append(tmp_hit_df, ignore_index=True)
        
        #write output list for annotation
        annotat = [seg_folder_name, labeled_crops]
        annotations.append(annotat)
        
        #mark missed annotations
        if debug:
            missed_annotat_folder = './debug_annot'
            if not os.path.exists(missed_annotat_folder):
                os.makedirs(missed_annotat_folder)
            img = cv2.imread(org_fov)
            missed_annotat_path = os.path.join(missed_annotat_folder, file)
            marked_img = mark_missed_annotation(img, missed_centr, color_map)
            cv2.imwrite(missed_annotat_path, marked_img)
        
        if args.mark_origin:    
            origin_mark_path = './origin_mark'
            if not os.path.exists(origin_mark_path):
                os.makedirs(origin_mark_path)
            dst = os.path.join(origin_mark_path, file)
            img = cv2.imread(org_fov)
            marked_img = mark_origin_fov(img, class_centr, color_map)
            cv2.imwrite(dst, marked_img)
            
            
        
            
        
    print(hit_df)
    print("===========================")
    print("Total statistic:")
    show_statistics(hit_df.append(missed_df))
    print("===========================")
    print("Missed statistic:")
    show_statistics(missed_df)
    print("===========================")
    print("Hit statistic:")
    show_statistics(hit_df)
    print("===========================")
    if debug:
        hit_df.to_csv(os.path.join(debug_path,'hit_{}.csv'.format(id)))
        missed_df.to_csv(os.path.join(debug_path,'miss_{}.csv'.format(id)))
    
    with open(os.path.join(output_path, annotations_name), 'w') as fp:
        fp.write(str(annotations))
