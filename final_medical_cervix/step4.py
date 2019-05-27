import glob
import ntpath
import os
import shutil
import sys

sys.path.append('./src/CLASSIFY/inceptionV3_final_1')
#print(sys.path)

import numpy as np

from src.CLASSIFY.inceptionV3_final_1.final_predict import CervixClassifier
from src.CLASSIFY.inceptionV3_final_1.final_predict import cp_list as clf_cp_list


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


@time_it
def process_origin_image(weights_path, threshold, clf_mode, class_num, color_mode, padding_methods):
    
    weights_path = weights_path
    clf = CervixClassifier(weights_path, 
                           TESTSET_DIR, 
                           clf_mode=clf_mode,
                           class_num=class_num,
                           color_mode=color_mode,
                           padding_methods=padding_methods,
                           init_dim=INPUT_SHAPE
                           )
    
    # Split train set
    total_images = np.sort(glob.glob(os.path.join(ORIGIN_DIR, FILE_PATTERN)))
    assert len(total_images)>0, "Original path is empty."
    print(total_images)

    for source in total_images:
        filename = ntpath.basename(source)
        base_filename = os.path.splitext(filename)[0]
        print(base_filename)
        
        clf.run_test_predict(base_filename, threshold)
        
    
if __name__ == '__main__':
    cp_list=[]
    
    import argparse
    #ORIGIN_DIR = 'datasets/origin/*/*'
    #MODEL_PATH = '/medical_data/yunhai/docter_medical_cervix/src/CLASSIFY/inceptionV3_final_1/'
    #WEIGHTS_NAME = 'inception.fold_5.hdf5'
    #FILE_PATTERN = '*.png'
    #TESTSET_DIR = 'datasets/classify'
    
    parser = argparse.ArgumentParser(
        description='Cervix Cancer Detection Step 4: Cervix cell classification')
    parser.add_argument('--origindir', required=True,
                        metavar="/path/to/origin/FOV/images/*/*...",
                        help='Directory to FOV images, for images in subdir, use */*/')
    parser.add_argument('--filepattern',
                        default='*.png',
                        help='select the files with the suffix pattern,e.g. *.png,*.jpg ')
    parser.add_argument('--datasets', required=True,
                        metavar="/path/to/datasets",
                        help='Directory to Segment cell images for classfication ')
    parser.add_argument('--weights', required=True,
                        metavar="/path/to/weights",
                        help="Path to the weights")
    parser.add_argument('--threshold', 
                        default=0.7,
                        help='threshold for predicted positive examples, float, (0,1) ',
                        type=float)
    parser.add_argument('--clf_mode',
                        default='Binary',
                        help='select the files with the suffix pattern,e.g. *.png,*.jpg ')
    parser.add_argument('--color_mode',
                        metavar="{RGB,HSV,HSV&CLAHE}",
                        default='RGB',
                        help='select the files with the suffix pattern,e.g. *.png,*.jpg ')
    parser.add_argument('--padding',
                        metavar="{{Double_ZoomOut_Padding, Padding, Warp}}",
                        default='Warp',
                        help='select the files with the suffix pattern,e.g. *.png,*.jpg ')
    parser.add_argument('--cuda_device',
                        default='0',
                        help='select cuda device')
    parser.add_argument('--input_shape',
                        default=[299, 299],
                        type=int,
                        nargs='+',
                        help='set input shape')
                        
    args = parser.parse_args()
    
    ORIGIN_DIR = args.origindir
    MODEL_PATH = args.weights
    FILE_PATTERN = args.filepattern
    TESTSET_DIR = args.datasets
    threshold = args.threshold
    clf_mode = args.clf_mode
    color_mode = args.color_mode
    padding_methods = args.padding
    INPUT_SHAPE = args.input_shape + [3]
    
    os.environ["CUDA_VISIBLE_DEVICES"] = args.cuda_device
    
    if clf_mode == 'Binary':
        class_num = 1
    elif clf_mode == 'MultiClass':
        class_num = 5
        threshold = None
    
    process_origin_image(MODEL_PATH, threshold, clf_mode, class_num, color_mode, padding_methods)
    
    avg_time = 0
    for _,duration in clf_cp_list:
        avg_time += duration
    avg_time /= len(clf_cp_list)
    #print(len(clf_cp_list))
    print('Function {} time costs: {} ms'.format(clf_cp_list[0][0], avg_time))
    
    for name, duration in cp_list:
        print('Function {} time costs: {} ms'.format(name, duration))
    
    with open('./check_point_step4.txt','w') as fd:
        fd.write(str(cp_list))
        fd.write(str(clf_cp_list))
    
    fd.close()
