import glob
import ntpath
import os
import shutil

import numpy as np

ROOT_FOLDER = '../../../datasets'            

ClassNames = ['normal', 'abnormal']


TRAINSET_OUTPUT_FOLDER = ROOT_FOLDER + '/classify/train'

if __name__ == '__main__':
    # Png is better
    INPUT_FILE_PATTERN = '*.png'
    classify_text = "train_labels.csv"
    
    with open(classify_text, 'w') as f:
        print('{},{}'.format('name', 'positive'), file=f)
        for index, clazz in enumerate(ClassNames):
            total_images = np.sort(glob.glob(os.path.join(TRAINSET_OUTPUT_FOLDER, clazz, INPUT_FILE_PATTERN)))
        
            for i in range(len(total_images)):
                filename = ntpath.basename(total_images[i])
                print('{},{}'.format(filename, index), file=f)
