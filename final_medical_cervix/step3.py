import numpy as np
import pandas as pd
import cv2
import os
import sys
import ntpath
from matplotlib import pyplot as plt
import shutil
import multiprocessing as mp
import tqdm

import glob
import ntpath
from scipy import misc


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

#=========================================
# Zernike Moments
#=========================================
from math import factorial
# -------------------------------------------------------------------------
# Function to compute Zernike Polynomials:
#
# rad = radialpoly(r,n,m)
# where
#   r = radius
#   n = the order of Zernike polynomial
#   m = the repetition of Zernike moment
# -------------------------------------------------------------------------
def radialpoly(r, n, m):
    rad = np.zeros(r.shape, r.dtype)
    P = int((n - abs(m)) / 2)
    Q = int((n + abs(m)) / 2)
    for s in range(P+1):
        c = (-1) ** s * factorial(n - s)
        c /= factorial(s) * factorial(Q - s) * factorial(P - s)
        rad += c * r ** (n - 2 * s)
    return rad
    
def ZernikeCoeff(src_shape, n, m):
    #if src.dtype != np.float32:
        #src = np.where(src > 0, 0, 1).astype(np.float32)
    if len(src_shape) == 3:
        print('the input image src should be in gray')
        return

    H, W = src_shape
    assert (H == W), "Not a square filter"

    N = src_shape[0]
    x = range(N)
    y = x
    X, Y = np.meshgrid(x, y)
    R = np.sqrt((2 * X - N + 1) ** 2 + (2 * Y - N + 1) ** 2) / N
    Theta = np.arctan2(N - 1 - 2 * Y, 2 * X - N + 1)
    R = np.where(R <= 1, 1, 0) * R

    # get the radial polynomial
    Rad = radialpoly(R, n, m)
    
    coeff = Rad * np.exp(-1j * m * Theta)
    # count the number of pixels inside the unit circle
    cnt = np.count_nonzero(R) + 1
    
    coeff = (n+1) * coeff/cnt
    
    assert len(coeff.shape) == len(src_shape), "coeff len: {}, src len: {}".format(len(coeff.shape), len(src_shape))
    for i in range(len(coeff.shape)):
        assert coeff.shape[i] == src_shape[i], "Coeff shape {}, src_shape {}".format(coeff.shape, src_shape)
    
    return coeff
    
def RegionalZernikeMoment(img, coeff, region_size):
    assert len(img.shape) == 3, "Must be a color image"
    assert img.shape[0] > region_size
    img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)[..., 0]
    r_n = img.shape[0] - region_size + 1
    c_n = img.shape[1] - region_size + 1
    
    A = np.zeros((r_n, c_n))
    
    for row in range(r_n):
        for col in range(c_n):
            src = img[row:row+region_size, col:col+region_size]
            #Intensity Normalization within disk prior
            src2 = cv2.normalize(src, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
            A[row, col] = abs((src * coeff).sum())
           
    return np.average(A)


#=========================================
# calculate a contour's p^2/area
#=========================================
def perimeter_vs_area(contour, area):
    
    perimeter = cv2.arcLength(contour, True)
    p_vs_a = perimeter**2/(area + 1e-6)
    
    return p_vs_a

#=========================================
# Nuclei Area Average Intensity Deviation
#=========================================
def cells_intensity_in_fov(origin_image_filename, mask_filename, filter_val, minArea=150, maxArea=1300):
    original = cv2.imread(origin_image_filename)
    mask = cv2.imread(mask_filename)
    if mask is None:
        no_mask.append(origin_image_filename)
        return []

    mask[mask > filter_val] = 255
    mask[mask <= filter_val] = 0
    
    ### To grayscale and normalize
    mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    mask_gray = cv2.normalize(src=mask_gray, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

    ### Auto binary threshold
    (thresh, mask_binary) = cv2.threshold(mask_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    ret, thresh = cv2.threshold(mask_binary, 127, 255, 0)
    h = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #h = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    contours = h[1]
    
    mean_intenses = []
    
    for i in range(len(contours)):
        cnt = contours[i]
        
        #Area threshold for Filtering
        area = cv2.contourArea(cnt)
        if area < minArea or area > maxArea:
            continue
        
        x, y, w, h = cv2.boundingRect(cnt)
        
        x1, y1, w1, h1 = int(x), int(y), int(w), int(h)
        
        cropped_mask = mask_binary[y1:y1 + h1, x1:x1 + w1]
        cropped = original[y1:y1 + h1, x1:x1 + w1, :]
        cropped = cropped[cropped_mask==255]
        mean_intens = np.average(cropped)
    
        mean_intenses.append(mean_intens)
        
    return mean_intenses

def intensity_statistics():
    # Split train set
    total_images = np.sort(glob.glob(os.path.join(ORIGIN_DIR, FILE_PATTERN)))
    
    # Random choose 10 images to calculate average intensity
    np.random.seed(10)
    samples = np.random.choice(total_images, 10, replace=False)
    
    mean_intenses = []
    for source in samples:
        filename = ntpath.basename(source)
        base_filename = os.path.splitext(filename)[0]
        print(base_filename)

        image_filename = source
        if SEG_COLOR == 'colouronly':
            mask_filename = os.path.join(SEGMENT_TEST_DIR,'../output/predict/test/colour/{}/channel_0.png'.format(base_filename))
        else:
            mask_filename = os.path.join(SEGMENT_TEST_DIR,'../output/predict/test/grey/{}/channel_1.png'.format(base_filename))
     
        #print('image_filename:{} mask_filename:{}'.format(image_filename, mask_filename))
        res = cells_intensity_in_fov(image_filename, mask_filename, FILTER_VAL, AREA_THRESH, AREA_MAX_THRESH)
        mean_intenses += res
        
    
    #print("Slide Nuclei Intesity Mean: %f" % INTENS_MEAN)
    #print("Slide Nuclei Intesity Var(Delta): %f" % INTENS_DELTA)
    return np.mean(mean_intenses), np.sqrt(np.var(mean_intenses))

def get_labels(img, mask, contours, precise_mask=True):
    img_shape = np.shape(img)[:-1]
    
    if (np.shape(mask) != img_shape):
        mask = cv2.resize(mask, (img_shape[-1], img_shape[0]))
    
    if (np.shape(contours) != img_shape):
        contours = cv2.resize(contours, (img_shape[-1], img_shape[0]))
        
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    #open operation to clean some noisies
    new_mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    #auto threshold with OTSU method
    _, thresh_mask = cv2.threshold(new_mask,0,255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    _, thresh_contour = cv2.threshold(contours,0,255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    #divide regions into background, foreground and unknown
    sure_foreground = cv2.subtract(thresh_mask, thresh_contour)
    
    output = cv2.connectedComponentsWithStats(sure_foreground)
    #get label mask
    labels = output[1]
    stats = output[2]
    centroids = output[3]
    #get coarse label
    if COARSE_LABEL == 'SureForeground':
        c_labels = output[1]
    else:
        _, c_labels, _, _ = cv2.connectedComponentsWithStats(thresh_mask)
    
    #generate precise mask
    sure_background = cv2.dilate(thresh_mask, kernel, iterations=3)
    mask_plus_contour = cv2.add(thresh_mask, thresh_contour)
    mask_plus_contour = cv2.cvtColor(mask_plus_contour, cv2.COLOR_GRAY2RGB)
    unknown = cv2.subtract(sure_background, sure_foreground)
 
    #set unknown to 0
    labels = labels + 1 
    labels[unknown==255] = 0
 
    labels = cv2.watershed(mask_plus_contour, labels)
    labels = labels - 1
    labels[labels < 0] = 0
    
    
   
    return labels, c_labels, stats, centroids
        


def box_resize(box, mask_shape, margin_factor):
    x, y, w, h = box
    if CROP_METHOD == 'Margin':
        wm = w * margin_factor
        hm = h * margin_factor

        x -= wm
        y -= hm
        w += 2 * wm
        h += 2 * hm
        x = max(0, x)
        y = max(0, y)
        X = min(x + w, mask_shape[1])
        Y = min(y + h, mask_shape[0])
        w = X - x
        h = Y - y
    elif CROP_METHOD == 'Square': 
        x = x + int(w/2) - int(SQUARE_EDGE/2)
        x = max(x, 0)
        y = y + int(h/2) - int(SQUARE_EDGE/2)
        y = max(y, 0)
        w = SQUARE_EDGE
        h = SQUARE_EDGE
        X = min(x + w, mask_shape[1])
        Y = min(y + h, mask_shape[0])
        w = X - x
        h = Y - y
    elif CROP_METHOD == 'Mask':
        center_x = x+(w/2)
        center_y = y+(h/2)
        side_len = max(w, h)
        margin = side_len * margin_factor
        side_margin_len = int(side_len + margin*2)
        x = center_x - int(side_margin_len/2)
        y = center_y - int(side_margin_len/2)
        x = max(0, x)
        y = max(0, y)
        X = min(x + side_margin_len, mask_shape[1])
        Y = min(y + side_margin_len, mask_shape[0])
        w = X - x
        h = Y - y
        #print("Frank: {}, {}, {}, {}, {}, {}, side_margin_len={}".format(x, y, X, Y, w, h, side_margin_len))
        if (w != h) or (w > 299) :
            return None
    return np.array([x, y, w, h]).astype(np.int16)        
        
def get_contour(box, labels, i):
    w, h = box[-2:]
    crop_mask = np.zeros([h, w]).astype(np.uint8)
    crop_label = labels[box[1]:box[1]+box[3], box[0]:box[0]+box[2]]
    crop_mask[crop_label==i] = 255
    contours = cv2.findContours(crop_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[1]
    area = cv2.contourArea(contours[0])
    return contours[0], area
    
    
def crop_and_save_for_debug(box, image, path, margin_factor):
    image_shape = np.shape(image)
    box = box_resize(box, image_shape, margin_factor)
    x, y, w, h = box
    cropped = image[y:y + h, x:x + w, :]
    cv2.imwrite(path, cropped)
    
    

def crop_file(origin_image_filename, mask_filename, contour_filename, margin_factor, minArea=150, maxArea=1300):
    
    ###prepare dirs
    filename = os.path.join('{}/{}_output'.format(ROOT_FOLDER, ntpath.basename(origin_image_filename)))
    if not os.path.exists(filename): os.makedirs(filename)     

    crops_outdir = os.path.join('{}/crops'.format(filename))
    preview_outdir = os.path.join('{}/preview'.format(filename))
    
    if not os.path.exists(crops_outdir): os.makedirs(crops_outdir) 
    if not os.path.exists(preview_outdir): os.makedirs(preview_outdir) 
    
    #print(mask_filename)
    #print(origin_image_filename)
    
    #========>>>>>>whether denoising for classifier??
    original = cv2.imread(origin_image_filename)
    #original = cv2.fastNlMeansDenoisingColored(original, None, 7, 7, 7, 21)
    
    mask = cv2.imread(mask_filename, 0)
    contours = cv2.imread(contour_filename, 0)
    
    if (mask is None) or (contours is None):
        no_mask.append(origin_image_filename)
        return 0
    
    labels, c_labels, stats, centroids = get_labels(original, mask, contours)
    
    ###coordinator files###
    index_name = os.path.join(preview_outdir, 'index_file.txt')
    index_file = open(index_name,"w+")
    #####
    ## image preview
    img_preview = original.copy()
    
    
    
    #prepare for debug
    if DEBUG:
        debug_path = os.path.join(filename, 'debug')
        debug_area_path = os.path.join(debug_path, 'area')
        debug_pva_path = os.path.join(debug_path, 'pva')
        debug_rzm_path = os.path.join(debug_path, 'rzm')
        if not os.path.exists(debug_area_path): os.makedirs(debug_area_path, exist_ok=True)
        if not os.path.exists(debug_pva_path): os.makedirs(debug_pva_path, exist_ok=True)
        if not os.path.exists(debug_rzm_path): os.makedirs(debug_rzm_path, exist_ok=True)
        area_filter_mask = np.zeros(np.shape(labels)).astype(np.uint8)
        box_filter_mask = np.zeros(np.shape(labels)).astype(np.uint8)
        pva_filter_mask = np.zeros(np.shape(labels)).astype(np.uint8)
        rzm_filter_mask = np.zeros(np.shape(labels)).astype(np.uint8)
        
    #prepare label mask
    label_mask = np.zeros(np.shape(labels)).astype(np.uint8)
    index = 1
    #print(minArea)
    #except background
    for i in range(1, np.max(labels) + 1):
        c_area = stats[i, cv2.CC_STAT_AREA]
        # coarse area filter
        if ( c_area < minArea) or (c_area > maxArea):
            if DEBUG:
                save_path = os.path.join(debug_area_path, ntpath.basename(origin_image_filename)+'_'+str(i)+'.png')
                area_filter_mask[labels==i] = 255
                #crop_and_save_for_debug(stats[i,:-1], original, save_path, margin_factor)
            
            continue
        
        # do cropping
        box = stats[i, :-1]
        box = box_resize(box, np.shape(labels), margin_factor)
        #for "Mask" cropping
        if box is None:
            box_filter_mask[labels==i] = 255
            continue
        
        #fine area filter, coarse area always smaller than fine area
        #cnt, f_area = get_contour(box, labels, i)
        
        #get contours
        #calculate perimeter vs area
        if PVA_THRESH is not None:
            if c_area < 500: # small cells, use c_labels to do pva
                cnt, f_area = get_contour(box, c_labels, i)
                pva_thres = 15
            elif c_area < 1000:
                cnt, f_area = get_contour(box, c_labels, i)
                pva_thres = 17
            else: #big cells , use fine labels to do pva
                cnt, f_area = get_contour(box, labels, i)
                pva_thres = 18.5
            
            p_vs_a = perimeter_vs_area(cnt, f_area)
            #if p_vs_a > PVA_THRESH:
            if p_vs_a > pva_thres:
                if DEBUG:
                    save_path = os.path.join(debug_pva_path, ntpath.basename(origin_image_filename)+'_'+str(i)+'.png')
                    pva_filter_mask[labels==i] = 255
                    #crop_and_save_for_debug(stats[i,:-1], original, save_path, margin_factor)
                continue
               
        
                
            
        x, y, w, h = box
        cropped = original[y:y + h, x:x + w, :]
        
        #calculate RZM to ignore blurry images.
        if RZM_THRESH is not None:
            rzm = RegionalZernikeMoment(cropped, Z_COEFF,R_SIZE)
            if rzm < RZM_THRESH:
                if DEBUG:
                    save_path = os.path.join(debug_rzm_path, ntpath.basename(origin_image_filename)+'_'+str(i)+'.png')
                    rzm_filter_mask[labels==i] = 255
                    #crop_and_save_for_debug(stats[i,:-1], original, save_path, margin_factor)
                continue
        
        #check the intensity of a cell
        if INTENS_THRES is not None:
            avg_intens = np.average(cropped)
            if (avg_intens > (INTENS_MEAN + INTENS_THRES))  \
            or (avg_intens < (INTENS_MEAN - INTENS_THRES)):
                continue
        
        #write coordinator
        index_file.write("%d " % (index))
        index_file.write("%d " % (x))
        index_file.write("%d " % (y))
        index_file.write("%d " % (w))
        index_file.write("%d\r\n" % (h))
        ###done ###
        
        #write label to label mask
        label_mask[labels==i] = index
        
        #crop files
        cropped_filename = os.path.join(crops_outdir, '{}.png'.format(index))
        #this is commented, for we will resize the input image in the classifier.
        #if w != SQUARE_EDGE or h != SQUARE_EDGE:
        #    cropped = misc.imresize(cropped, (SQUARE_EDGE, SQUARE_EDGE), interp='bilinear')
        cv2.imwrite(cropped_filename, cropped)
        
        #marks on image preview
        cv2.rectangle(img_preview, (x, y), (x + w, y + h), (0, 255, 0), 1)
        #can't draw contours, for the contours are in the crop now
        #cv2.drawContours(img_preview,cnt,-1,(0,255,0),1)
        cv2.putText(img_preview, str(index), (x, y + h), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), lineType=cv2.LINE_AA) 
        
        index += 1
        
    
    #Generate Label, after cleaning the labels
    label_filename = os.path.join(preview_outdir, 'label.png')  
    cv2.imwrite(label_filename, label_mask)
    
    #Generate Mask, after cleaning the labels
    mask = np.zeros(np.shape(labels))
    mask[label_mask > 0] = 255
    mask_filename = os.path.join(preview_outdir, 'mask.png')  
    cv2.imwrite(mask_filename, mask)
    
    #write preview file    
    preview_filename = os.path.join(preview_outdir, 'preview.png')    
    cv2.imwrite(preview_filename, img_preview)
    #close coordinator file
    index_file.close()    
    
    if DEBUG:
        area_mask_path = os.path.join(debug_path, ntpath.basename(origin_image_filename)+'_'+'area_mask.png')
        box_mask_path = os.path.join(debug_path, ntpath.basename(origin_image_filename)+'_'+'box_mask.png')
        pva_mask_path = os.path.join(debug_path, ntpath.basename(origin_image_filename)+'_'+'pva_mask.png')
        rzm_mask_path = os.path.join(debug_path, ntpath.basename(origin_image_filename)+'_'+'rzm_mask.png')
        cv2.imwrite(area_mask_path, area_filter_mask)
        cv2.imwrite(box_mask_path, box_filter_mask)
        cv2.imwrite(pva_mask_path, pva_filter_mask)
        cv2.imwrite(rzm_mask_path, rzm_filter_mask)


def worker(images):
    bar = tqdm.tqdm
    for source in bar(images):
        filename = ntpath.basename(source)
        base_filename = os.path.splitext(filename)[0]
        #print(base_filename)

        image_filename = source
        if SEG_COLOR == 'colouronly':
            mask_filename = os.path.join(SEGMENT_TEST_DIR,'../output/predict/test/colour/{}/channel_0.png'.format(base_filename))
            contours_filename = os.path.join(SEGMENT_TEST_DIR,'../output/predict/test/colour/{}/channel_1.png'.format(base_filename))
        else:
            mask_filename = os.path.join(SEGMENT_TEST_DIR,'../output/predict/test/grey/{}/channel_0.png'.format(base_filename))
            contours_filename = os.path.join(SEGMENT_TEST_DIR,'../output/predict/test/grey/{}/channel_1.png'.format(base_filename))
     
        #print('image_filename:{} mask_filename:{}'.format(image_filename, mask_filename))
        crop_file(image_filename, mask_filename, contours_filename, CROP_MARGIN, AREA_THRESH, AREA_MAX_THRESH)


@time_it
def process_origin_image():

    # Split train set
    total_images = np.sort(glob.glob(os.path.join(ORIGIN_DIR, FILE_PATTERN)))
    #input_images = []
    #for image in total_images:
    #    filename = os.path.basename(image)
    #    name = filename.split('.')[0]
    #    path = os.path.join(SEGMENT_TEST_DIR, name, 'images', name + '.png')
    #    assert os.path.exists(path), "File not exists: %s" % path
    #    input_images.append(path)
    
    print(total_images)
    print('Num of total images: {}'.format(len(total_images)))
    

    cpus = mp.cpu_count() 
    images_split = np.array_split(total_images,cpus)
    
    p = mp.Pool(processes=cpus)
    p.map(worker, images_split)
    p.close()
    p.join()
    
    

@time_it
def process_one():

    # Split train set
    total_images = np.sort(glob.glob(os.path.join(ORIGIN_DIR, FILE_PATTERN)))
    #print(total_images)
    
    filename = ntpath.basename(total_images[0])
    base_filename = os.path.splitext(filename)[0]
    #print(base_filename)

    image_filename = os.path.join(SEGMENT_TEST_DIR,'{}/images/{}.png'.format(base_filename, base_filename))
    if SEG_COLOR == 'colouronly':
        mask_filename = os.path.join(SEGMENT_TEST_DIR,'../output/predict/test/colour/{}/channel_0.png'.format(base_filename))
    else:
        mask_filename = os.path.join(SEGMENT_TEST_DIR,'../output/predict/test/grey/{}/channel_0.png'.format(base_filename))
        #mask_filename = os.path.join(SEGMENT_TEST_DIR,'../output/predict/test/grey/{}/channel_0.png'.format(base_filename))
    #print('image_filename:{} mask_filename:{}'.format(image_filename, mask_filename))
    #crop_file(image_filename, mask_filename, 100, 0.2, 150, 2000)
    crop_file(image_filename, mask_filename, FILTER_VAL, CROP_MARGIN, AREA_THRESH, AREA_MAX_THRESH)
                
    
if __name__ == '__main__':
    cp_list = []
    
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Cervix Cancer Detection Step 3: Crop FOV into cells')
    parser.add_argument('--origindir', required=True,
                        metavar="/path/to/origin/FOV/images/*/*...",
                        help='Directory to FOV images, for images in subdir, use */*/')
    parser.add_argument('--filepattern',
                        default='*.png',
                        help='select the files with the suffix pattern,e.g. *.png,*.jpg ')
    parser.add_argument('--datasets', required=True,
                        metavar="/path/to/datasets",
                        help='Directory to cell images for classfication ')
    parser.add_argument('--segtestdir', required=True,
                        metavar="/path/to/segment/dir",
                        help='Directory of segmentations datasets')
    parser.add_argument('--crop_margin',
                        default=0.2,
                        help='margin factor for crop the segmentation image',
                        type=float)
    parser.add_argument('--square_edge',
                        default=75,
                        help='size of square edge for crop the segmentation image',
                        type=float)
    parser.add_argument('--seg_color',
                        default='colouronly',
                        help='segment on gray or color.')
    parser.add_argument('--crop_method',
                        default='Margin',
                        help='method for cropping, default: Margin, others: Square')
    parser.add_argument('--area_thresh',
                        #default=300,
                        default=100,
                        type=float,
                        help='Area threshold for cropping')
    parser.add_argument('--perimeter_vs_area',
                        #default=22.5,
                        default=None,
                        type=float,
                        help='Perimeter vs Area threshold for cropping')
    parser.add_argument('--zernike_thresh',
                        #default=3.7,
                        default=None,
                        type=float,
                        help='Regional Zernike Moments threshold for cropping')
                        
    parser.add_argument('--intensity_thresh',
                        #default=30,
                        default=None,
                        type=float,
                        help='Regional Zernike Moments threshold for cropping')
    
    args = parser.parse_args()
    #ROOT_FOLDER = 'datasets/classify'
    #ORIGIN_DIR = 'datasets/origin/*/*'
    #SEGMENT_TEST_DIR = 'datasets/segment/test/'
    #FILE_PATTERN = '*.png'
    ROOT_FOLDER = args.datasets 
    ORIGIN_DIR = args.origindir
    SEGMENT_TEST_DIR = args.segtestdir
    FILE_PATTERN = args.filepattern
    SEG_COLOR = args.seg_color
    CROP_MARGIN = args.crop_margin
    SQUARE_EDGE = args.square_edge
    CROP_METHOD = args.crop_method
    AREA_THRESH = args.area_thresh
    PVA_THRESH = args.perimeter_vs_area
    RZM_THRESH = args.zernike_thresh
    INTENS_THRES = args.intensity_thresh
    
    #PRECISE_MASK = True
    COARSE_LABEL = 'SureForeground'
    DEBUG = True
    
    AREA_MAX_THRESH = 50000
    FILTER_VAL = 100
    
    no_mask = []
    
    z_order = 5
    z_repitition = 3
    R_SIZE = 6
    
    Z_COEFF = ZernikeCoeff([R_SIZE]*2, z_order, z_repitition)
    
    
    if INTENS_THRES is not None:
        INTENS_MEAN, INTENS_DELTA = intensity_statistics()
        print("Slide Nuclei Intesity Mean: %f" % INTENS_MEAN)
        print("Slide Nuclei Intesity Var(Delta): %f" % INTENS_DELTA)
        
    
    
    #process_origin_image(args.crop_margin)
    process_origin_image()
    
    if no_mask:
        if not os.path.exists(os.path.join(ORIGIN_DIR,'no_mask')):
            os.makedirs(os.path.join(ORIGIN_DIR,'no_mask'))   
        for img in no_mask:
            base_name = os.path.basename(img)
            shutil.move(img, os.path.join(ORIGIN_DIR,'no_mask') + '/' + base_name)
            
    
    #process_one()
    for name,duration in cp_list:
        print('Function {} time costs: {} ms'.format(name,duration))
        
    
    fd = open('./check_point_step3.txt','w')
    fd.write(str(cp_list))
    fd.close()
    
    

