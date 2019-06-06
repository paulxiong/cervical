import numpy as np
import pandas as pd
import cv2
import os
import shutil
from tqdm import tqdm


def get_annot_coordinate(image, color_map):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    class_centroid = {}
    for gt in color_map.keys():
        color = color_map[gt]
        annotation = (image == color).all(axis=-1)
        if annotation.any():
            annotation = annotation.astype(np.uint8)*255
            annotation = cv2.morphologyEx(annotation, cv2.MORPH_OPEN, kernel, iterations=1)
            annotation = cv2.dilate(annotation, kernel, iterations=3)
            output = cv2.connectedComponentsWithStats(annotation)
            centroid = output[3][1:]
            class_centroid[gt] = centroid
    return class_centroid
            
def get_central_label(label_mask, class_centr):
    abnormal_labels = []
    hit_annotat = {}
    missed_annotat = {}
    for gt in class_centr.keys():
        coords = class_centr[gt].astype(np.int16)
        for centr in coords:
            #print(centr)
            label = label_mask[centr[1],centr[0]]
            #print(label.shape)
            if label != 0:
                abnormal_labels.append(label)
                try:
                    hit_annotat[gt].append(centr) 
                except:
                    hit_annotat[gt] = [centr]
            else:
                try:
                    missed_annotat[gt].append(centr) 
                except:
                    missed_annotat[gt] = [centr]
    
    return abnormal_labels, hit_annotat, missed_annotat
            
def mark_missed_annotation(annotat_img, missed_centr, color_map):
    for gt in missed_centr.keys():
        coords = missed_centr[gt]
        for centr in coords:
            #print(centr)
            annotat_img = cv2.rectangle(annotat_img, tuple(centr-10), tuple(centr+10), color_map[gt], -1)
            
    return annotat_img


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
    annot_path = ['/opt/zhuoyao_workspace/github/final_medical_cervix/datasets/origin_annotation/orgin_02052019_cells']
    seg_path = ['/opt/zhuoyao_workspace/github/final_medical_cervix/datasets/classify/']
    
    debug = True
    #debug
    if debug:
        debug_path = './debug_annot'
        missed_annotat_folder = os.path.join(debug_path, 'annot_fov')
        if not os.path.exists(missed_annotat_folder):
            os.makedirs(missed_annotat_folder)
        
    
    color_map = {1: (0, 255, 255), #yellow
             2: (0, 255, 0), #Green
             3: (0, 0, 255), #Red
             5: (255, 255, 0) #cyan
            }
    class_map ={1: 'LSIL', 
                2: 'HSIL',
                3: 'LSIL_HPV',
                5: 'SCC'}
    
    
    for a_path, s_path in zip(annot_path, seg_path):
        files = os.listdir(a_path)
        
        annotations_name = 'annotation_' + os.path.basename(a_path) + '.txt'
        annotations = []
        missed_df = pd.DataFrame()
        hit_df = pd.DataFrame()
        for file in tqdm(files):
            annotat_img_path = os.path.join(a_path, file)
            folder_name = file + '_output'
            label_mask_path = os.path.join(s_path, folder_name, 'preview', 'label.png')
            if not os.path.exists(label_mask_path):
                print("label.png did not exists, %s " % label_mask_path)
                continue
            
            img = cv2.imread(annotat_img_path)
            label = cv2.imread(label_mask_path, 0)
            
            class_centr = get_annot_coordinate(img, color_map)
            abnormal_crops, hit_centr, missed_centr = get_central_label(label, class_centr)
            
            #mark missed annotations
            if debug:
                missed_annotat_path = os.path.join(missed_annotat_folder, file)
                marked_img = mark_missed_annotation(img, missed_centr, color_map)
                cv2.imwrite(missed_annotat_path, marked_img)
            
            #generate df
            tmp_missed_df = generate_df(missed_centr, file, class_map)
            tmp_hit_df = generate_df(hit_centr, file, class_map)
            
            missed_df = missed_df.append(tmp_missed_df, ignore_index=True)
            hit_df = hit_df.append(tmp_hit_df, ignore_index=True)
            
            #write output list for annotation
            annotat = [folder_name, abnormal_crops, []]
            annotations.append(annotat)
            
        
        #print(hit_df)
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
            hit_df.to_csv(os.path.join(debug_path,'hit.csv'))
            missed_df.to_csv(os.path.join(debug_path,'miss.csv'))
        
        with open(annotations_name, 'w') as fp:
            fp.write(str(annotations))
