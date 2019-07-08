import glob
import ntpath
import os
import shutil
import numpy as np
import pandas as pd
import cv2
import multiprocessing as mp

def resize_img(img, resize_ratio):
    if (resize_ratio == 1) or (resize_ratio <=0):
        return img
    else:
        h, w, _ = img.shape
        img = cv2.resize(img, (int(w * resize_ratio), int(h * resize_ratio)))
    return img

def get_intensity(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    return np.average(img[:,:,0])

def wrapper(arg):
    images = arg['images_split']
    SEGMENT_TEST_DIR =  arg['segment_test_dir']
    DENOISING =  arg['denoising']
    FILE_PATTERN = arg['file_pattern']
    RESIZE_RATIO = arg['resize_ratio']
    res = pd.DataFrame()
    for source in images:
        filename = ntpath.basename(source)
        path_split = source.split('/')
        slide_name = path_split[-3] if path_split[-2] == 'Images' else path_split[-2]
        base_filename = slide_name + '_' + os.path.splitext(filename)[0]
        df_dic = {'FOV_Name': base_filename}

        base_outdir = os.path.join('{}/{}/images'.format(SEGMENT_TEST_DIR, base_filename))
        if not os.path.exists(base_outdir): os.makedirs(base_outdir)

        target = os.path.join(base_outdir, base_filename+'.png')

        if DENOISING:
            img = cv2.imread(source)
            img = resize_img(img, RESIZE_RATIO)
            img_dn = cv2.fastNlMeansDenoisingColored(img, None, 7, 7, 7, 21)
            cv2.imwrite(target, img_dn)
            print("Color image {} denoising & copy complete!".format(filename))
        elif (FILE_PATTERN != '*.png') or (RESIZE_RATIO != 1):
            img = cv2.imread(source)
            img = resize_img(img, RESIZE_RATIO)
            cv2.imwrite(target, img)
            print("Image {} copy complete.".format(filename))
        else:
            shutil.copy(source, target)
            print("Color image {} copy complete!".format(filename))
    return None

def process_origin_image(DATASETS_DIR, SEGMENT_TEST_DIR, FILE_PATTERN, DENOISING, RESIZE_RATIO):
    # Split train set
    total_images = np.sort(glob.glob(os.path.join(DATASETS_DIR + '/*/', FILE_PATTERN)))

    cpus = mp.cpu_count()
    images_split = np.array_split(total_images, cpus)
    images_split2 = []

    for _images_split in images_split:
        images_split2.append({'images_split': _images_split, 'segment_test_dir': SEGMENT_TEST_DIR,
                              "denoising": DENOISING, "file_pattern": FILE_PATTERN, 'resize_ratio': RESIZE_RATIO})
    p = mp.Pool(processes=cpus)
    res = p.map(wrapper, images_split2)
    p.close()
    p.join()

def step1v2(origindir, segtestdir, filepattern):
    DATASETS_DIR = origindir
    SEGMENT_TEST_DIR = segtestdir
    FILE_PATTERN = filepattern
    DENOISING = False
    RESIZE_RATIO = 1

    process_origin_image(origindir, segtestdir, filepattern, DENOISING, RESIZE_RATIO)
