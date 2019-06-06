import glob
import ntpath
import os
import shutil

import numpy as np

DATASETS_DIR = 'datasets/origin/'
SEGMENT_TEST_DIR = 'datasets/segment/test/'

def process_origin_image():
    FILE_PATTERN = '*.png'

    # Split train set
    total_images = np.sort(glob.glob(os.path.join(DATASETS_DIR, FILE_PATTERN)))
    print(total_images)

    for source in total_images:
        filename = ntpath.basename(source)
        base_filename = os.path.splitext(filename)[0]
        print(base_filename)

        cmd = 'cd src/CLASSIFY/inceptionV3_final_1/ && python3 final_predict.py {}'.format(base_filename)
        ret = os.popen(cmd).read()
        print(ret)
    
if __name__ == '__main__':
    process_origin_image()
    
