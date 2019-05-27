import csv
import cv2
import numpy as np
import pandas as pd
import glob
import ntpath
import os
import shutil


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
        crop_path = os.path.join(DATASET_DIR, filename)+'_output/crops'
        #print("////---------new path:",new_path)
        #image_path = new_path
        #print("image_path:",image_path)
        final_result_path = new_path+'/final_result.csv'
        #print("Final csv_path:",final_result_path)
        index_path = new_path+'/index_file.txt'
        #print("index_path:",index_path)
        #image_write = new_path+'/test.png'
        image_write = os.path.join(OUTPUT_DIR, filename)
        print("image_write:",image_write)
        #crop_folder = 
        if CLF_MODE == 'Binary':
            mark_file(image_path, final_result_path, index_path, image_write, crop_path, filename)
        elif CLF_MODE == 'MultiClass':
            mark_multi(image_path, final_result_path, index_path, image_write, crop_path, filename)


def mark_multi(image_path, 
               final_result_path, 
               index_path, 
               image_write,
               crop_path,
               filename,
               mark_class=[1,2,3]
               ):
                   
    #mark_point, score_point, x1, y1, w1, h1 = list(), list(), list(), list(), list(), list()
    #room = list()
    global NUM_TOTAL
    global NUM_ABNORMAL
    global abnormal_table
    global abnormal_FOVs_Folder
    global abnormal_cells_Folder
    FLAG = False

    re_img = cv2.imread(image_path,1)
    if not os.path.exists(final_result_path):
        return 0
    res_df = pd.read_csv(final_result_path)
    if res_df.empty:
        return 0

    print("curr file is:", filename)
    #print("--------row is:", res_df.shape[0] )
    NUM_TOTAL += res_df.shape[0]
    
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
                FLAG = True
                NUM_ABNORMAL += 1
                img_num = series['index']
                abnormal_table[clazz] += 1
                print("Mark cell: {}, Class: {}, Score: {}".format(img_num, clazz, score))
                """
                copy single cell images to a folder
                """
                cell_file = str(img_num) + ".png"
                cell_path = os.path.join(crop_path, cell_file)
                orig_filename = os.path.splitext(filename)[0]
                print("cell_file is: ", cell_path)
                print("abnormal_cells_Folder is: ", abnormal_FOVs_Folder)
                print("new cell file name is: ", abnormal_cells_Folder+str(clazz)+"/"+orig_filename+"_"+cell_file)
                if os.path.exists(cell_path):
                    shutil.copy(cell_path, abnormal_cells_Folder+str(clazz))
                    shutil.move(abnormal_cells_Folder+str(clazz)+"/"+cell_file,
                                abnormal_cells_Folder+str(clazz)+"/"+orig_filename+"_"+cell_file)
                score = np.round(score*100)/100
                cv2.rectangle(re_img, (x1, y1), (x1 + w1, y1 + h1), color, 1)
                cv2.putText(re_img, str(clazz)+':'+str(score), (x1, y1 + h1 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), lineType=cv2.LINE_AA)
                cv2.putText(re_img, str(img_num), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), lineType=cv2.LINE_AA)
                                    
    cv2.imwrite(image_write,re_img)
    
    if FLAG:
        #print("image_write is: ", image_write)
        #print("final result path is: ",final_result_path)
        shutil.copy(image_write, abnormal_FOVs_Folder)

        


#@time_it
def mark_file(image_path, final_result_path, index_path, image_write, crop_path, filename):
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
    
    """
    p = mp.Pool(processes=cpus)
    p.map(mark_wrapper, images_split)
    p.close()
    p.join()
    
    """
    for file in images_split:
        mark_wrapper(file)


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
    parser.add_argument('--abnormalfovs', required=True,
                        metavar="/path/to/abnormal_FOVs",
                        help='Directory of abnormal fovs, absolute dir = /path/to/datasets +/path/to/abnormal_FOVs')
    parser.add_argument('--abnormalcells', required=True,
                        metavar="/path/to/abnormalcells",
                        help='Directory of abnormal cells, absolute dir = /path/to/datasets +/path/to/abnormalcells')
    parser.add_argument('--slidename', required=True,
                        metavar="slidename",
                        help='Use to diff different slide results')
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
    
    abnormal_FOVs_Folder = args.abnormalfovs
    abnormal_cells_Folder = args.abnormalcells
    slidename = args.slidename
    
    NUM_TOTAL = 0
    NUM_ABNORMAL = 0
    abnormal_table = {1:0, 2:0, 3:0, 4:0}
    
    if not os.path.exists(abnormal_FOVs_Folder): os.makedirs(abnormal_FOVs_Folder)
    if not os.path.exists(abnormal_cells_Folder): os.makedirs(abnormal_cells_Folder)
    
    if not os.path.exists(abnormal_cells_Folder+"/1"): os.makedirs(abnormal_cells_Folder+"/1")
    if not os.path.exists(abnormal_cells_Folder+"/2"): os.makedirs(abnormal_cells_Folder+"/2")
    if not os.path.exists(abnormal_cells_Folder+"/3"): os.makedirs(abnormal_cells_Folder+"/3")
    if not os.path.exists(abnormal_cells_Folder+"/4"): os.makedirs(abnormal_cells_Folder+"/4")

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
    
    """
    abnormal_FOVs_Folder = "datasets/abnormal_FOVs/"
    abnormal_cells_Folder = "datasets/abnormal_cells/"
    """
    
    if os.path.exists(abnormal_FOVs_Folder):
        newFolder = abnormal_FOVs_Folder[:-1]+'_'+slidename
        if os.path.exists(newFolder):
            shutil.rmtree(newFolder)
        shutil.move(abnormal_FOVs_Folder, newFolder)
        
    if os.path.exists(abnormal_cells_Folder):
        newFolder = abnormal_cells_Folder[:-1]+'_'+slidename
        if os.path.exists(newFolder):
            shutil.rmtree(newFolder)
        shutil.move(abnormal_cells_Folder, newFolder)
        
    if os.path.exists(DATASET_DIR):
        newFolder = DATASET_DIR[:-1]+'_'+slidename
        if os.path.exists(newFolder):
            shutil.rmtree(newFolder)
        shutil.move(DATASET_DIR, newFolder)
    
    print("------SUMMARY------")
    print("------Finish predicting one slide, number of total cells is :",NUM_TOTAL)
    print("------number of abnormal cells is :",NUM_ABNORMAL)
    print("------abnormal cells ratio is :",NUM_ABNORMAL/NUM_TOTAL)
    for clazz in abnormal_table:
        print("Class: {}, number: {}".format(clazz, abnormal_table[clazz]))
