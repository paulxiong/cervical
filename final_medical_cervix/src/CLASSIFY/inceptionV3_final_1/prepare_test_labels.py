import glob
import ntpath
import os
import shutil
import sys
import numpy as np

ROOT_FOLDER = '../../../datasets'            

ClassNames = ['normal', 'abnormal']


TEST_FOLDER = ROOT_FOLDER + '/classify/fold_0/val_split/normal'
#TEST_FOLDER = '../../../datasets/classify/{}.png_output/crops/'.format(sys.argv[1])



if __name__ == '__main__':
    # Png is better
    INPUT_FILE_PATTERN = '*.png'
    classify_text = "input/submission.csv"
    
    with open(classify_text, 'w') as f:
        print('{},{}'.format('name', 'positive'), file=f)
        total_images = np.sort(glob.glob(os.path.join(TEST_FOLDER, INPUT_FILE_PATTERN)))
        
        for i in range(len(total_images)):
            filename = ntpath.basename(total_images[i])
            print('{},{}'.format(filename, 0.5), file=f)
