import glob
import ntpath
import os
import shutil

import numpy as np
import cv2

import multiprocessing as mp


def resize_img(img, resize_ratio):
    if (resize_ratio == 1) or (resize_ratio <=0):
        return img
    else:
        h, w, _ = img.shape
        img = cv2.resize(img, (int(w * resize_ratio), int(h * resize_ratio)))
        
    return img

def wrapper(images):
    for source in images:
        filename = ntpath.basename(source)
        base_filename = os.path.splitext(filename)[0]
        print(base_filename)

        base_outdir = os.path.join('{}/{}/images'.format(SEGMENT_TEST_DIR, base_filename))
        if not os.path.exists(base_outdir): os.makedirs(base_outdir) 

        target = os.path.join(base_outdir, base_filename+'.png')
        
        
                
        
        if COLOR_ONLY:
            if DENOISING:
                img = cv2.imread(source)
                img = resize_img(img, RESIZE_RATIO)
                img_dn = cv2.fastNlMeansDenoisingColored(img, None, 7, 7, 7, 21)
                cv2.imwrite(target, img_dn)
                print("Color image %s denoising & copy complete!" % filename)
            elif (FILE_PATTERN != '*.png') or (RESIZE_RATIO != 1):
                img = cv2.imread(source)
                img = resize_img(img, RESIZE_RATIO)
                cv2.imwrite(target, img)
            else:
                shutil.copy(source, target)
                print("Color image %s copy complete!" % filename)
            
            

            '''if DENOISING:
                img = cv2.imread(source)
                if RESIZE_RATIO != 1:
                    img = cv2.resize(img, (int(img.shape[1]*RESIZE_RATIO),int(img.shape[0]*RESIZE_RATIO)) )
                img_dn = cv2.fastNlMeansDenoisingColored(img, None, 7, 7, 7, 21)
                cv2.imwrite(target, img_dn)
                print("Color image %s denoising & copy complete!" % filename)
            else:
                if FILE_PATTERN != '*.png':
                    img = cv2.imread(source)
                    cv2.imwrite(target, img)
                else:
                    shutil.copy(source, target)
                    print("Color image %s copy complete!" % filename)'''
                
        if GREY_ONLY:
            img = cv2.imread(source, 0)
            if DENOISING:
                img_dn = cv2.fastNlMeansDenoising(img,None, 10, 7, 21)
            else:
                img_dn = img
            cv2.imwrite(target, img_dn)
            print("Grey image {} with denoising:{} copy complete!".format(filename, DENOISING))
            

    


def process_origin_image():
    #FILE_PATTERN = '*.png'

    # Split train set
    total_images = np.sort(glob.glob(os.path.join(DATASETS_DIR, FILE_PATTERN)))
    print(total_images)
    
    cpus = mp.cpu_count()
    images_split = np.array_split(total_images, cpus)
    
    p = mp.Pool(processes=cpus)
    p.map(wrapper, images_split)
    p.close()
    p.join()

'''    for source in total_images:
        filename = ntpath.basename(source)
        base_filename = os.path.splitext(filename)[0]
        print(base_filename)

        base_outdir = os.path.join('{}/{}/images'.format(SEGMENT_TEST_DIR, base_filename))
        if not os.path.exists(base_outdir): os.makedirs(base_outdir) 

        target = os.path.join(base_outdir, filename)
        shutil.copy(source, target)'''

        
def process_grey_image():
    FILE_PATTERN = '*.png'

    # Split train set
    total_images = np.sort(glob.glob(os.path.join(DATASETS_DIR, FILE_PATTERN)))
    print(total_images)

    for source in total_images:
        filename = ntpath.basename(source)
        base_filename = os.path.splitext(filename)[0]
        print(base_filename)

        base_outdir = os.path.join('{}/{}/images'.format(SEGMENT_TEST_DIR, base_filename))
        if not os.path.exists(base_outdir): os.makedirs(base_outdir) 

        target = os.path.join(base_outdir, filename)
        img = cv2.imread(source, 0)
        cv2.imwrite(target, img)

        
    
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Cervix Cancer Detection Step 1: Copy FOV to segmentation path')
        
    
    parser.add_argument('--origindir', required=True,
                        metavar="/path/to/origin/FOV/images/*/*...",
                        help='Directory to FOV images, for images in subdir, use */*/')
    parser.add_argument('--segtestdir', required=True,
                        metavar="/path/to/segment/test/dir",
                        help='Directory of segmentation test datasets')
    parser.add_argument('--greyonly', action="store_true",
                        help='Set: only grey models will be trained and does predictions on grey images')     
    parser.add_argument('--colouronly', action="store_true", 
                        help='Set: only colour models will be trained and does predictions on colour images')
    parser.add_argument('--denoising', action="store_true", 
                        help='Set: denoising the gaussian noise caused by camera')
    parser.add_argument('--filepattern', 
                        default='*.png',
                        metavar="file pattern to search",
                        help='file pattern to search')
    parser.add_argument('--resize_ratio', 
                        default=1,
                        type=float,
                        metavar="aspect resize ratio",
                        help='resize image to (w*ratio, h*ratio')
    
    args = parser.parse_args()
    #DATASETS_DIR = 'datasets/origin/*/*'
    #SEGMENT_TEST_DIR = 'datasets/segment/test/'
    
    DATASETS_DIR = args.origindir
    SEGMENT_TEST_DIR = args.segtestdir
    COLOR_ONLY = args.colouronly
    GREY_ONLY = args.greyonly
    DENOISING = args.denoising
    FILE_PATTERN = args.filepattern
    RESIZE_RATIO = args.resize_ratio
    
    process_origin_image()
    
    
    #if args.colouronly:
        #process_origin_image()
        
    #if args.greyonly:
        #process_grey_image()
        #print("Copy grey images done.")
        
    
