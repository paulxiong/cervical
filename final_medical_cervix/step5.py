import csv
import cv2
import numpy as np
import pandas as pd
import glob
import ntpath
import os

import multiprocessing as mp

'''for time costs analysis'''
import time
import re

def time_it(fun):
    def new_fun(*args, **kwargs):
        start = time.time()
        result = fun(*args, **kwargs)
        end = time.time()
        duration = (end-start)*1000
        name = re.search(r' [a-zA-Z_]*',str(fun)).group()[1:]
        cp_list.append([name, duration])
        return result
    return new_fun



def mark_wrapper(images):
    for image_path in images:
       # print("/---------path:",image_path)
        filename = ntpath.basename(image_path)
        #print(filename)
        new_path = os.path.join(DATASET_DIR, filename)+'_output/preview'
        #print("////---------new path:",new_path)
        #image_path = new_path
        #print("image_path:",image_path)
        final_result_path = new_path+'/final_result.csv'
        #print("Final csv_path:",final_result_path)
        index_path = new_path+'/index_file.txt'
        #print("index_path:",index_path)
        #image_write = new_path+'/test.png'
        image_write = os.path.join(OUTPUT_DIR, filename)
        #print("image_write:",image_write)
        if CLF_MODE == 'Binary':
            mark_file(image_path, final_result_path, index_path, image_write)
        elif CLF_MODE == 'MultiClass':
            mark_multi(image_path, final_result_path, index_path, image_write)


def mark_multi(image_path, 
               final_result_path, 
               index_path, 
               image_write,
               mark_class=[1,2,3,4]
               ):
                   
    #mark_point, score_point, x1, y1, w1, h1 = list(), list(), list(), list(), list(), list()
    #room = list()
    print("---------inside image_path:",image_path)
    re_img = cv2.imread(image_path,1)
    if not os.path.exists(final_result_path):
        return 0
    res_df = pd.read_csv(final_result_path)
    if res_df.empty:
        return 0
    
    res_df['index'] = res_df.apply(lambda x: int(x['name'].split('.')[0]), axis=1)

    co_df = pd.read_csv(index_path, sep=' ', header=None)
    co_df.columns = ['index', 'x', 'y', 'w', 'h']
    
    res_df = pd.merge(res_df, co_df, on=['index'])
    
    for clazz in mark_class:
        np.random.seed(clazz)
        color = np.random.randint(255, size=3)
        color = (int(color[0]), int(color[1]), int(color[2]))
        df = res_df.loc[res_df['positive'] == clazz]
        for _, series in df.iterrows():
            x1, y1, w1, h1 = series['x':'h']
            score = series['preds_' + str(clazz)]
            if score > THRESHOLD:
                img_num = series['index']
                print("Mark cell: {}, Class: {}, Score: {}".format(img_num, clazz, score))
                score = np.round(score*100)/100
                cv2.rectangle(re_img, (x1, y1), (x1 + w1, y1 + h1), color, 1)
                cv2.putText(re_img, str(clazz)+':'+str(score), (x1, y1 + h1 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), lineType=cv2.LINE_AA)
                cv2.putText(re_img, str(img_num), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), lineType=cv2.LINE_AA)
                                    
    cv2.imwrite(image_write,re_img)


#@time_it
def mark_file(image_path, final_result_path, index_path, image_write):
    setting_value = THRESHOLD
    mark_point,score_point, x1,y1,w1,h1 = list(),list(),list(),list(),list(), list()
    room = list()
    print("---------inside image_path:",image_path)
    re_img = cv2.imread(image_path,1)
    
    with open(final_result_path) as csvfile:
        read_CSV = csv.reader(csvfile, delimiter=',')
        next(csvfile)
        for row in read_CSV:
            if float(row[1]) > setting_value:
                mark_point.append(row[0].replace(".png",""))
                score_point.append(row[1])
        print("mark_point", mark_point)
        print("score_point", score_point)
        
    with open(index_path, 'r') as f:
        index_data = f.readlines()  
        for cell in mark_point:
            for line_num in index_data:
            	odom = line_num.split()
            	ele = cell.split()
            	
            	if int(ele[0]) == int(odom[0]):
                    
                    x1,y1,w1,h1 = int(odom[1]),int(odom[2]),int(odom[3]),int(odom[4])
                    cv2.rectangle(re_img, (x1, y1), (x1 + w1, y1 + h1), (0, 0, 255), 1)
                    print("point", ele[0],  x1,y1,w1,h1)
                    
                    with open(final_result_path) as csvfile:
                        read_CSV = csv.reader(csvfile, delimiter=',')
                        next(csvfile)
                        for row in read_CSV:
                            if float(row[1]) > setting_value:
                                testodom = odom[0]+'.png'
                                if row[0] == testodom:
                                    print("-----final_row:",row[0])
                                    print("testodom:",testodom)
                                    text = row[1]
                                    img_num = row[0]
                                    print("------ text",text)
                                    print("img_num:",img_num)
                                    cv2.putText(re_img, text, (x1, y1 + h1), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), lineType=cv2.LINE_AA)
                                    cv2.putText(re_img, img_num, (x1, y1 + h1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), lineType=cv2.LINE_AA)
                                    print("------end write in :",image_write)
                    cv2.imwrite(image_write,re_img)
@time_it
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
    
    '''
    for image_path in total_images:
       # print("/---------path:",image_path)
        filename = ntpath.basename(image_path)
        #print(filename)
        new_path = 'datasets/classify/'+filename+'_output/preview'
        #print("////---------new path:",new_path)
        #image_path = new_path
        #print("image_path:",image_path)
        final_result_path = new_path+'/final_result.csv'
        #print("Final csv_path:",final_result_path)
        index_path = new_path+'/index_file.txt'
        #print("index_path:",index_path)
        #image_write = new_path+'/test.png'
        image_write = 'datasets/classify/marked_image/'+filename
        #print("image_write:",image_write)
        mark_file(image_path, final_result_path, index_path, image_write)
        '''



    
if __name__ == '__main__':
    cp_list = []
    
    import argparse
   
    parser = argparse.ArgumentParser(
        description='Cervix Cancer Detection Step 5: Positive cell Mark')
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
    parser.add_argument('--threshold', 
                        default=0.7,
                        help='threshold for predicted positive examples, float, (0,1) ',
                        type=float)
    parser.add_argument('--clf_mode',
                        default='Binary',
                        help='select the files with the suffix pattern,e.g. *.png,*.jpg ')
    
    args = parser.parse_args()
    
    #ORIGIN_DIR = 'datasets/origin/'
    #DATASET_DIR = 'datasets/classify/
    #FILE_PATTERN = '*.png'
    #THRESHOLD = '0.48'
    
    ORIGIN_DIR = args.origindir
    DATASET_DIR = args.datasets
    FILE_PATTERN = args.filepattern
    OUTPUT_DIR = os.path.join(DATASET_DIR,args.outputdir)
    THRESHOLD = args.threshold 
    CLF_MODE = args.clf_mode
    
    process_origin_image()
    
    sum_duration = 0
    for name,duration in cp_list:
        print('Function {} time costs: {} ms'.format(name,duration))
        if name == 'mark_file':
            sum_duration += duration
            
#    print('Function mark_file average time cost: {} ms'.format(sum_duration/(len(cp_list)-1)))
    
    fd = open('./check_point_step5.txt','w')
    fd.write(str(cp_list))
    fd.close()