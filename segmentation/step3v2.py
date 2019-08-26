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
from scipy.misc import imsave, imread, imresize
import torchvision.utils as vutils
import torchvision.transforms as transforms
import torch
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
#        cp_list.append([name,duration])
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
            A[row, col] = abs((src2 * coeff).sum())

    return np.average(A)


#=========================================
# calculate a contour's p^2/area
#=========================================
def perimeter_vs_area(contour, area):
    perimeter = cv2.arcLength(contour, True)
    p_vs_a = perimeter**2/(area + 1e-6)

    return p_vs_a, perimeter

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
    if cv2.__version__.split('.')[0]=='3':
        contours = h[1]
    elif cv2.__version__.split('.')[0]=='4':
        contours = h[0]
    else:
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
    total_images = np.sort(glob.glob(os.path.join(ORIGIN_DIR + '/*/', FILE_PATTERN)))

    # Random choose 10 images to calculate average intensity
    np.random.seed(10)
    samples = np.random.choice(total_images, 10, replace=False)

    mean_intenses = []
    for source in samples:
        filename = ntpath.basename(source)
        path_split = source.split('/')
        slide_name = path_split[-3] if path_split[-2] == 'Images' else path_split[-2]
        base_filename = slide_name + '_' + os.path.splitext(filename)[0]
        print(base_filename)

        image_filename = source
        mask_filename = os.path.join(SEGMENT_TEST_DIR,'../output/predict/test/colour/{}/channel_0.png'.format(base_filename))

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

def get_labels_old(img, mask, filter_val):
    original = img
    img_shape = np.shape(img)[:-1]

    if (np.shape(mask) != img_shape):
        mask = cv2.resize(mask, (img_shape[-1], img_shape[0]))

    mask[mask > filter_val] = 255
    mask[mask <= filter_val] = 0

    #binaryImg = cv2.Canny(mask,100,200)

    #h = cv2.findContours(binaryImg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

#    mask[mask > t] = 255
#    mask[mask <= t] = 0

    ### To grayscale and normalize
    #mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    mask_gray = mask
    mask_gray = cv2.normalize(src=mask_gray, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

    ### Auto binary threshold
    (thresh, mask_binary) = cv2.threshold(mask_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    ret, thresh = cv2.threshold(mask_binary, 127, 255, 0)
    output = cv2.connectedComponentsWithStats(thresh)

    labels = output[1]
    stats = output[2]
    centroids = output[3]

    c_labels = labels

    return labels, c_labels, stats, centroids

def box_resize(box, mask_shape, margin_factor, crop_method='Mask'):
    x, y, w, h = box
    if crop_method == 'Margin':
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
    elif crop_method == 'Square':
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
    elif crop_method == 'Mask':
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
    return np.array([x, y, w, h]).astype(np.int16)

def get_contour(box, labels, i):
    w, h = box[-2:]
    crop_mask = np.zeros([h, w]).astype(np.uint8)
    crop_label = labels[box[1]:box[1]+box[3], box[0]:box[0]+box[2]]
    crop_mask[crop_label==i] = 255
    contours = cv2.findContours(crop_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if cv2.__version__.split('.')[0]=='3':
        contours = contours[1]
    elif cv2.__version__.split('.')[0]=='4':
        contours = contours[0]
    else:
        contours = contours[1]
    if len(contours)>0:
        area = cv2.contourArea(contours[0])
    else:
        area = 0
    return contours[0], area

def get_label_cnt(box, labels):
    crop_label = labels[box[1]:box[1]+box[3], box[0]:box[0]+box[2]]
    unique_labels = np.unique(crop_label)
    return len(unique_labels)

def crop_and_save_for_debug(box, image, path, margin_factor):
    image_shape = np.shape(image)
    box = box_resize(box, image_shape, margin_factor, crop_method='Square')
    x, y, w, h = box
    cropped = image[y:y + h, x:x + w, :]
    cv2.imwrite(path, cropped)

def crop_file(origin_image_filename, mask_filename, contour_filename, args, margin_factor, minArea=150, maxArea=1300):
    ###prepare dirs
    path_split = origin_image_filename.split('/')
    slide_name = path_split[-3] if path_split[-2] == 'Images' else path_split[-2]
    filename = os.path.join('{}/{}_{}_output'.format(args['ROOT_FOLDER'], slide_name, ntpath.basename(origin_image_filename)))
    base_filename = slide_name + '_' + os.path.splitext(ntpath.basename(origin_image_filename))[0]
    if not os.path.exists(filename): os.makedirs(filename)

    crops_outdir = os.path.join('{}/crops'.format(filename))
    preview_outdir = os.path.join('{}/preview'.format(filename))

    if not os.path.exists(crops_outdir): os.makedirs(crops_outdir)
    if not os.path.exists(preview_outdir): os.makedirs(preview_outdir)

    #print(mask_filename)
    #print(origin_image_filename)

    #========>>>>>>whether denoising for classifier??
    original = cv2.imread(origin_image_filename)
    original = original[..., ::-1]
    #original = cv2.fastNlMeansDenoisingColored(original, None, 7, 7, 7, 21)

    mask = cv2.imread(mask_filename, 0)
    contours = cv2.imread(contour_filename, 0)

    if (mask is None) or (contours is None):
        no_mask.append(origin_image_filename)
        return 0

    if args['LABEL_GEN'] == "Kaggle":
        labels, c_labels, stats, centroids = get_labels(original, mask, contours)
    elif args['LABEL_GEN'] == "Private":
        labels, c_labels, stats, centroids = get_labels_old(original, mask, args['FILTER_VAL'])
    else:
        print("Unsupported Label generate method! %s " % args['LABEL_GEN'])
        exit(-1)

    ###coordinator files###
    index_name = os.path.join(preview_outdir, 'index_file.txt')
    index_file = open(index_name,"w+")
    #####
    ## image preview
    img_preview = original[...,::-1].copy()

    npy_outdir = os.path.join('{}/npy/'.format(args['ROOT_FOLDER']))
    if not os.path.exists(npy_outdir): os.makedirs(npy_outdir)

    #prepare for debug
    if args['DEBUG']:
        debug_path = os.path.join(filename, 'debug')
        debug_area_path = os.path.join(debug_path, 'area')
        debug_pva_path = os.path.join(debug_path, 'pva')
        debug_rzm_path = os.path.join(debug_path, 'rzm')
        debug_intens_path = os.path.join(debug_path, 'intens')
        if not os.path.exists(debug_area_path): os.makedirs(debug_area_path, exist_ok=True)
        if not os.path.exists(debug_pva_path): os.makedirs(debug_pva_path, exist_ok=True)
        if not os.path.exists(debug_rzm_path): os.makedirs(debug_rzm_path, exist_ok=True)
        if not os.path.exists(debug_intens_path): os.makedirs(debug_intens_path, exist_ok=True)
        area_filter_mask = np.zeros(np.shape(labels)).astype(np.uint8)
        pva_filter_mask = np.zeros(np.shape(labels)).astype(np.uint8)
        rzm_filter_mask = np.zeros(np.shape(labels)).astype(np.uint8)
        intens_filter_mask = np.zeros(np.shape(labels)).astype(np.uint8)
        #save original labels for debug
        org_label_path = os.path.join(debug_path, ntpath.basename(origin_image_filename)+'_'+'org_label.png')
        cv2.imwrite(org_label_path, labels)

        #Table 1
        # 0 is background
        debug_df1 = pd.DataFrame()
        debug_df1['Label'] = np.array(range(1, len(stats))).astype(np.uint16)
        debug_df1['Fov_Name'] = slide_name + '_' + ntpath.basename(origin_image_filename).split('.')[0]
        debug_df1[['O_X', 'O_Y', 'O_W', 'O_H']] = pd.DataFrame(stats[1:, :-1]).astype(np.int16)
        debug_df1['Area'] = stats[1:, -1].astype(np.float32)
        debug_df1[['Center_X', 'Center_Y']] = pd.DataFrame(centroids[1:]).astype(np.int16)
        #debug_df1[['C_X', 'C_Y', 'C_W', 'C_H']] = pd.DataFrame([[np.nan, np.nan, np.nan, np.nan]]).astype(np.float16)
        #mapping with Fov_Name

        #Table 2
        debug_df2 = pd.DataFrame()

    #prepare label mask
    label_mask = np.zeros(np.shape(labels)).astype(np.uint8)
    index = 1
    #print(minArea)
    #except background
    image_dict = None
    for i in range(1, np.max(labels) + 1):
        #filtered flag
        f_flag = True

        c_area = stats[i, cv2.CC_STAT_AREA]
        # coarse area filter
        if ( c_area < minArea) or (c_area > maxArea):
            if args['DEBUG']:
                save_path = os.path.join(debug_area_path, ntpath.basename(origin_image_filename)+'_'+str(i)+'.png')
                area_filter_mask[labels==i] = 255
                debug_df1.loc[debug_df1['Label']==i, 'Filter_By'] = 'Area'
                debug_df1.loc[debug_df1['Label']==i, 'Crop_path'] = save_path
                crop_and_save_for_debug(stats[i,:-1], original[...,::-1], save_path, 0)
            continue

        #get box with Mask crop for PVA, because 75x75 square may missed some labels and cause pva failed
        box = stats[i, :-1]
        box = box_resize(box, np.shape(labels), margin_factor, crop_method='Mask')

        #fine area filter, coarse area always smaller than fine area
        #calculate perimeter vs area
        if args['PVA_THRESH'] is not None:
            if c_area < 300: # small cells, use c_labels to do pva
                #get contours
                cnt, f_area = get_contour(box, c_labels, i)
                pva_thres = 16
            elif c_area < 1000:
                cnt, f_area = get_contour(box, c_labels, i)
                pva_thres = 17
            else: #big cells , use fine labels to do pva
                cnt, f_area = get_contour(box, labels, i)
                pva_thres = 18.5

            p_vs_a, perimeter = perimeter_vs_area(cnt, f_area)

            #save perimeter
            if args['DEBUG']:
                c_cnt, c_area = get_contour(box, c_labels, i)
                c_perimeter = cv2.arcLength(c_cnt, True)
                f_cnt, f_area = get_contour(box, labels, i)
                f_perimeter = cv2.arcLength(f_cnt, True)
                debug_df1.loc[debug_df1['Label']==i, 'C_Perimeter'] = np.float32(c_perimeter)
                debug_df1.loc[debug_df1['Label']==i, 'F_Perimeter'] = np.float32(f_perimeter)
                debug_df1.loc[debug_df1['Label']==i, 'C_Pixel_Area'] = np.float32(c_area)
                debug_df1.loc[debug_df1['Label']==i, 'F_Pixel_Area'] = np.float32(f_area)

            if p_vs_a > pva_thres:
                if args['DEBUG'] and f_flag:
                    save_path = os.path.join(debug_pva_path, ntpath.basename(origin_image_filename)+'_'+str(i)+'.png')
                    pva_filter_mask[labels==i] = 255
                    debug_df1.loc[debug_df1['Label']==i, 'Filter_By'] = 'PVA'
                    debug_df1.loc[debug_df1['Label']==i, 'Crop_path'] = save_path
                    crop_and_save_for_debug(stats[i,:-1], original[...,::-1], save_path, 0)
                    f_flag = False
                elif not args['DEBUG']:
                    continue

        # cropping
        box = stats[i, :-1]
        box = box_resize(box, np.shape(labels), margin_factor, crop_method=args['CROP_METHOD'])

        x, y, w, h = box
        cropped = original[y:y + h, x:x + w, :]

        #save cropped box
        #saved in indexfile.txt, no need to save again
        #if DEBUG:
        #    debug_df1.loc[debug_df1['Label']==i, ['C_X', 'C_Y', 'C_W', 'C_H']] = box

        #calculate RZM to ignore blurry images.
        if args['RZM_THRESH'] is not None:
            rzm = RegionalZernikeMoment(cropped, Z_COEFF,R_SIZE)

            if DEBUG:
                debug_df1.loc[debug_df1['Label']==i, 'RZM'] = np.float32(rzm)

            if rzm > 24:
                if DEBUG and f_flag:
                    save_path = os.path.join(debug_rzm_path, ntpath.basename(origin_image_filename)+'_'+str(i)+'.png')
                    rzm_filter_mask[labels==i] = 255
                    debug_df1.loc[debug_df1['Label']==i, 'Filter_By'] = 'RZM'
                    debug_df1.loc[debug_df1['Label']==i, 'Crop_path'] = save_path
                    crop_and_save_for_debug(stats[i,:-1], original[...,::-1], save_path, 0)
                    f_flag = False
                elif not DEBUG:
                    continue

        #check the intensity of a cell
        if args['INTENS_THRES'] is not None:
            avg_intens = np.average(cropped)
            if DEBUG:
                debug_df1.loc[debug_df1['Label']==i, 'Crop_Intens'] = np.float32(avg_intes)
            if (avg_intens > (INTENS_MEAN + INTENS_THRES)) or (avg_intens < (INTENS_MEAN - INTENS_THRES)):
                if DEBUG and f_flag:
                    save_path = os.path.join(debug_intens_path, ntpath.basename(origin_image_filename)+'_'+str(i)+'.png')
                    intens_filter_mask[labels==i] = 255
                    debug_df1.loc[debug_df1['Label']==i, 'Filter_By'] = 'Intens'
                    debug_df1.loc[debug_df1['Label']==i, 'Crop_path'] = save_path
                    crop_and_save_for_debug(stats[i,:-1], original[...,::-1], save_path, 0)
                    f_flag = False
                elif not DEBUG:
                    continue

        if f_flag == False:
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
        cv2.imwrite(cropped_filename, cropped[..., ::-1])

        #1.save index for mapping Crop box,2.save Crop path,
        if args['DEBUG']:
            debug_df1.loc[debug_df1['Label']==i, 'Index'] = index
            debug_df1.loc[debug_df1['Label']==i, 'Crop_path'] = cropped_filename

        #marks on image preview
        cv2.rectangle(img_preview, (x, y), (x + w, y + h), (0, 0, 255), 4)
        #can't draw contours, for the contours are in the crop now
        #cv2.drawContours(img_preview,cnt,-1,(0,255,0),1)
        cv2.putText(img_preview, str(index), (x, y + h), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), lineType=cv2.LINE_AA)

        index += 1

        resize_image = imresize(cropped, [32, 32], interp='nearest')
        #resize_image = cv2.resize(cropped, (32, 32))

        m = np.array([resize_image])
        if image_dict is not None:
            image_dict = np.append(image_dict, m,  axis=0)
        else:
            image_dict = m

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

    preview_npy = os.path.join(npy_outdir, '%s.npy'%base_filename)
    image = image_dict #np.array(image_dict)

    if image is None:
        return pd.DataFrame({'name': base_filename, 'npy': []}), None
    np.save(preview_npy, image)

    #print(image.shape)
    image = np.transpose(image, (0,3,1,2))
    #print(image.shape)

    preview_segpng = os.path.join(npy_outdir, '%s_seg.png'%base_filename)
    vutils.save_image(torch.FloatTensor(image), preview_segpng ,nrow=5,normalize=True)

    if args['DEBUG']:
        df1_path = os.path.join(debug_path, ntpath.basename(origin_image_filename)+'_'+'table1.csv')
        area_mask_path = os.path.join(debug_path, ntpath.basename(origin_image_filename)+'_'+'area_mask.png')
        pva_mask_path = os.path.join(debug_path, ntpath.basename(origin_image_filename)+'_'+'pva_mask.png')
        rzm_mask_path = os.path.join(debug_path, ntpath.basename(origin_image_filename)+'_'+'rzm_mask.png')
        intens_mask_path = os.path.join(debug_path, ntpath.basename(origin_image_filename)+'_'+'intens_mask.png')
        cv2.imwrite(area_mask_path, area_filter_mask)
        cv2.imwrite(pva_mask_path, pva_filter_mask)
        cv2.imwrite(rzm_mask_path, rzm_filter_mask)
        cv2.imwrite(intens_mask_path, intens_filter_mask)
        debug_df1.to_csv(df1_path, columns=debug_df1.columns)

        #use [] to prevent from data missing
        debug_df2['Fov_Name'] = [slide_name + '_'+ntpath.basename(origin_image_filename).split('.')[0]]
        debug_df2['Mask_Path'] = [mask_filename]
        debug_df2['Preview_Path'] = [preview_filename]
        debug_df2['Label_Path'] = [label_filename]
        debug_df2['Indexfile_Path'] = [index_name]
        debug_df2['Orignal_Label_Path'] = [org_label_path]
        debug_df2[['Area_Mask','PVA_Mask', 'RZM_Mask','Intens_Mask']] = pd.DataFrame([[area_mask_path,
                                                                                        pva_mask_path,
                                                                                        rzm_mask_path,
                                                                                        intens_mask_path
                                                                                        ]], index=debug_df2.index)
        debug_df2['Tabel1_Path'] = df1_path

        #print(debug_df2)

        return pd.DataFrame({'name': base_filename, 'npy': [image_dict]}), debug_df2
    return pd.DataFrame({'name': base_filename, 'npy': [image_dict]}), None

def worker(workerargs):
    images = workerargs['images_split']
    args = workerargs['args']
    bar = tqdm.tqdm
    debug_df2 = pd.DataFrame()

    npy_df = pd.DataFrame()
    for source in bar(images):
        filename = ntpath.basename(source)
        path_split = source.split('/')
        slide_name = path_split[-3] if path_split[-2] == 'Images' else path_split[-2]
        base_filename = slide_name + '_' + os.path.splitext(filename)[0]
        #print(base_filename)

        image_filename = source
        mask_filename = os.path.join(args['MASK_DIR'],'predict/test/colour/{}/channel_0.png'.format(base_filename))
        contours_filename = os.path.join(args['MASK_DIR'],'predict/test/colour/{}/channel_1.png'.format(base_filename))

        assert os.path.exists(mask_filename), "Segmentation: {} channel_0 not exists".format(mask_filename)
        assert os.path.exists(contours_filename), "Segmentation: {} channel_1 not exists".format(contours_filename)

        #print('image_filename:{} mask_filename:{}'.format(image_filename, mask_filename))
        img_npy, df = crop_file(image_filename, mask_filename, contours_filename, args, args['CROP_MARGIN'], args['AREA_THRESH'], args['AREA_MAX_THRESH'])
        #print(df)

        npy_df = npy_df.append(img_npy, ignore_index=True)

        if args['DEBUG']:
            if df is None:
                print("Debug table 2 DataFrame is not existed!")
                exit(-1)
            else:
                debug_df2 = pd.concat([debug_df2, df], ignore_index=True)

    return npy_df, debug_df2

@time_it
def process_origin_image(args):
    slide_npy_outdir = os.path.join(args['ROOT_FOLDER'], 'slide_npy')
    if not os.path.exists(slide_npy_outdir):
        os.makedirs(slide_npy_outdir)
    # Split train set
    total_images = np.sort(glob.glob(os.path.join(args['ORIGIN_DIR'] + '/*/', args['FILE_PATTERN'])))
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

    images_split2 = []
    for _images_split in images_split:
        images_split2.append({'images_split': _images_split, 'args': args})

    p = mp.Pool(processes=cpus)
    res = p.map(worker, images_split2)
    p.close()
    p.join()

    npy_ls = []
    debug_ls = []
    for npy_df, debug_df in res:
        npy_ls.append(npy_df)
        debug_ls.append(debug_df)

    if args['DEBUG']:
        table2_df = pd.concat(debug_ls, ignore_index=True)
        print(table2_df)
        table2_name = "step3_table2.csv"
        save_path = os.path.join(DEBUG_PATH, table2_name)
        table2_df.to_csv(save_path, columns=table2_df.columns)

    tot_df = pd.concat(npy_ls, axis=0, ignore_index=True)
    print(tot_df.iloc[0])
    tot_df['slide'] = tot_df['name'].apply(lambda x: re.search(r'(.*)_IMG', x).group(1))

    slides = tot_df['slide'].unique()

    try:
        for slide in slides:
            df = tot_df.loc[tot_df['slide'] == slide]
            tmp = df['npy'].values
            slide_npy = np.ndarray([0]+list(np.shape(tmp[0])[1:]))
            for npy in tqdm.tqdm(tmp):
                slide_npy = np.append(slide_npy, npy, axis=0)
            shape = np.shape(slide_npy)
            ##print(shape)
            slide_path = os.path.join(slide_npy_outdir, '%s.npy'%slide)

            np.save(slide_path, slide_npy)
    except:
        import pdb; pdb.set_trace()

@time_it
def process_one():

    # Split train set
    total_images = np.sort(glob.glob(os.path.join(ORIGIN_DIR + '/*/', FILE_PATTERN)))
    #print(total_images)

    filename = ntpath.basename(total_images[0])
    path_split = source.split('/')
    slide_name = path_split[-3] if path_split[-2] == 'Images' else path_split[-2]
    base_filename = slide_name + '_' + os.path.splitext(filename)[0]
    #print(base_filename)

    image_filename = os.path.join(SEGMENT_TEST_DIR,'{}/images/{}.png'.format(base_filename, base_filename))
    mask_filename = os.path.join(SEGMENT_TEST_DIR,'../output/predict/test/colour/{}/channel_0.png'.format(base_filename))
        #mask_filename = os.path.join(SEGMENT_TEST_DIR,'../output/predict/test/grey/{}/channel_0.png'.format(base_filename))
    #print('image_filename:{} mask_filename:{}'.format(image_filename, mask_filename))
    #crop_file(image_filename, mask_filename, 100, 0.2, 150, 2000)
    crop_file(image_filename, mask_filename, FILTER_VAL, CROP_MARGIN, AREA_THRESH, AREA_MAX_THRESH)

def step3v2(origindir, filepattern, datasetspath, segtestdir, maskdir, crop_method, area_thresh, square_edge, perimeter_vs_area):
    cp_list = []
    crop_margin=0.2
    intensity_thresh=None
    zernike_thresh=None

    ROOT_FOLDER = datasetspath
    ORIGIN_DIR = origindir
    SEGMENT_TEST_DIR = segtestdir
    FILE_PATTERN = filepattern
    MASK_DIR = maskdir
    CROP_MARGIN = crop_margin
    SQUARE_EDGE = square_edge
    CROP_METHOD = crop_method
    AREA_THRESH = area_thresh
    PVA_THRESH = perimeter_vs_area
    RZM_THRESH = zernike_thresh
    INTENS_THRES = intensity_thresh

    #PRECISE_MASK = True
    COARSE_LABEL = 'SureForeground'
    LABEL_GEN = "Private"

    DEBUG = False
    DEBUG_PATH = './Debug_DF'
    if not os.path.exists(DEBUG_PATH):
        os.makedirs(DEBUG_PATH)

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
    args = {'ROOT_FOLDER': ROOT_FOLDER, 'ORIGIN_DIR': ORIGIN_DIR,
            'FILE_PATTERN': FILE_PATTERN, 'DEBUG': DEBUG, 'DEBUG_PATH': DEBUG_PATH,
            'SEGMENT_TEST_DIR': SEGMENT_TEST_DIR, 'CROP_MARGIN': CROP_MARGIN,
            'AREA_THRESH': AREA_THRESH, 'AREA_MAX_THRESH': AREA_MAX_THRESH, 'LABEL_GEN': LABEL_GEN,
            'FILTER_VAL': FILTER_VAL, 'PVA_THRESH': PVA_THRESH, 'CROP_METHOD': CROP_METHOD,
            'RZM_THRESH': RZM_THRESH, 'INTENS_THRES': INTENS_THRES, 'MASK_DIR': MASK_DIR}
    process_origin_image(args)

    if no_mask:
        if not os.path.exists(os.path.join(ORIGIN_DIR,'no_mask')):
            os.makedirs(os.path.join(ORIGIN_DIR,'no_mask'))
        for img in no_mask:
            base_name = os.path.basename(img)
            shutil.move(img, os.path.join(ORIGIN_DIR,'no_mask') + '/' + base_name)

    #process_one()
    for name,duration in cp_list:
        print('Function {} time costs: {} ms'.format(name,duration))

    #fd = open('./check_point_step3.txt','w')
    #fd.write(str(cp_list))
    #fd.close()
