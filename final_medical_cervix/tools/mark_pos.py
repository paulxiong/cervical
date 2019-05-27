import csv
import cv2
import numpy as np
import glob
import ntpath
import os
import pandas as pd

import multiprocessing as mp

'''for time costs analysis'''
import time
import re

def time_it(fun):
    def new_fun(*args,**kwargs):
        start = time.time()
        result = fun(*args,**kwargs)
        end = time.time()
        duration = (end-start)*1000
        name = re.search(r' [a-zA-Z_]*',str(fun)).group()[1:]
        cp_list.append([name,duration])
        return result
    return new_fun
'''----------------------------'''

def read_listfile(filepath):
    '''return a list of namedtuples with [filename,positive,negative]'''
    try:
        fd = open(filepath,'r')
        content = eval(fd.read())
    
    except:
        print("Can't open file {}" % (filepath))
        exit(-1)
        
    pos_dict={}
    neg_dict={}
        
    for filename,positive,negative in content:
        pos_dict[filename] = positive
        neg_dict[filename] = negative
    return pos_dict, neg_dict


def mark_wrapper(images):
    for image_path in images:
       # print("/---------path:",image_path)
        filename = ntpath.basename(image_path)
        #print(filename)
        folder_name = filename+'_output'
        print(folder_name)
        new_path = os.path.join(DATASET_DIR,filename)+'_output/preview'
        #print("////---------new path:",new_path)
        #image_path = new_path
        #print("image_path:",image_path)
        final_result_path = new_path+'/final_result.csv'
        #print("Final csv_path:",final_result_path)
        index_path = new_path+'/index_file.txt'
        #print("index_path:",index_path)
        #image_write = new_path+'/test.png'
        image_write = os.path.join(OUTPUT_DIR,filename)
        print("image_write:",image_write)
        mark_file(image_path, final_result_path, index_path, image_write,folder_name)

def merge_index_to_result(final_result_path,index_path):
    final_res_df = pd.read_csv(final_result_path)
    index_df = pd.read_csv(index_path,sep=' ',names = ['index','x1','y1','w1','h1'])
    final_res_df['index'] = final_res_df['name'].apply(lambda x: np.int64(x.split('.')[0]))
    final_df = pd.merge(final_res_df,index_df,how='left',on='index').set_index('index').sort_index()
    del final_res_df,index_df
    return final_df


def marking(img,df,mark_point,prefix,rec_color,txt_color,write_path):   
    for cell in mark_point:
        '''
        if cell==117:
            print(df)
            print(write_path)
        '''
        try:
            x1,y1,w1,h1 = df.loc[cell][['x1','y1','w1','h1']]
        except:
            #print(df)
            print("Image {}, Cell {} didn't exists.".format(write_path, cell))
            continue
        
        img_num = prefix+'_'+str(cell)
        cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1),rec_color, 1)
        cv2.putText(img, img_num, (x1, y1 + h1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, txt_color, lineType=cv2.LINE_AA)
        print("point", cell,  x1,y1,w1,h1)
        cv2.imwrite(write_path,img)


#@time_it
def mark_file(image_path, final_result_path, index_path, image_write, folder_name):
    mark_point,score_point, x1,y1,w1,h1 = list(),list(),list(),list(),list(), list()
    room = list()
    print("---------inside image_path:",image_path)
    re_img = cv2.imread(image_path,1)
    
    final_df = pd.read_csv(index_path,sep=' ',names = ['index','x1','y1','w1','h1'])
    #final_df = merge_index_to_result(final_result_path,index_path)
    pos_point = POS_MASK[folder_name]
    neg_point = NEG_MASK[folder_name]
    
    marking(re_img,final_df,pos_point,'abnorm',(0,0,255),(255,0,255),image_write)
    marking(re_img,final_df,neg_point,'norm',(255,0,0),(255,0,255),image_write)

        

def process_origin_image():
    
    # Split train set
    total_images = np.sort(glob.glob(os.path.join(ORIGIN_DIR, FILE_PATTERN)))
    print(total_images)

    # create marked_image
    folder = os.path.exists(OUTPUT_DIR)
    if not folder:
        os.makedirs(OUTPUT_DIR)
    
    
    cpus = mp.cpu_count() 
    images_split = np.array_split(total_images,cpus)
    
    p = mp.Pool(processes=cpus)
    p.map(mark_wrapper, images_split)
    p.close()
    p.join()
    


    
if __name__ == '__main__':
    cp_list = []
    
    import argparse
   
    parser = argparse.ArgumentParser(
        description='Tools: mark positive')
    parser.add_argument('--origindir', required=True,
                        metavar="/path/to/origin/FOV/images/*/*...",
                        help='Directory to FOV images, for images in subdir, use */*/')
    parser.add_argument('--filepattern',
                        default='*.png',
                        help='select the files with the suffix pattern,e.g. *.png,*.jpg ')
    parser.add_argument('--datasets', required=True,
                        metavar="/path/to/datasets",
                        help='Directory to Segment cell images for classfication ')
    parser.add_argument('--outputdir', required=True,
                        metavar="/path/to/output",
                        help='Directory of Mark outputs, absolute dir = /path/to/datasets +/path/to/output')
    parser.add_argument('--listfile', required=True,
                        metavar="/path/to/listfile",
                        help='path to list file')

    
    args = parser.parse_args()
    
    ORIGIN_DIR = args.origindir
    DATASET_DIR = args.datasets
    FILE_PATTERN = args.filepattern
    OUTPUT_DIR = args.outputdir
    
    
    POS_MASK, NEG_MASK = read_listfile(args.listfile)
    
    process_origin_image()
    


