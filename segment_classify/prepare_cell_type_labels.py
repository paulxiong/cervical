import glob
import ntpath
import os
import shutil
import sys
import numpy as np

ROOT_FOLDER = '/opt/yunhai/GAN/github/cervical/Nu_Gan/CellLevel/2019-05-23+2019-01FJ+RedHouse/dataset/train/'            



ClassNames = ['Norm', 'ASCH', 'ASCUS', 'HPV', 'HSIL','LSIL','SCC']



TEST_FOLDER = ROOT_FOLDER 
#TEST_FOLDER = '../../../datasets/classify/{}.png_output/crops/'.format(sys.argv[1])



if __name__ == '__main__':
    # Png is better
    INPUT_FILE_PATTERN = '*.png'
    classify_text = "/opt/yunhai/GAN/github/cervical/Nu_Gan/CellLevel/2019-05-23+2019-01FJ+RedHouse/sample_submission.csv"
    
    with open(classify_text, 'w') as f:
        print('{},{}'.format('name', 'positive'), file=f)
        
        
        for index, clazz in enumerate(ClassNames):
            total_images = np.sort(glob.glob(os.path.join(TEST_FOLDER, clazz, INPUT_FILE_PATTERN)))
        
            for i in range(len(total_images)):
                filename = clazz + '/' +ntpath.basename(total_images[i])
                print('{},{}'.format(filename, 0.5), file=f)
        
        
    