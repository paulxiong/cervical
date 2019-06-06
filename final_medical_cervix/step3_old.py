import numpy as np
import cv2
import os
import sys
import ntpath
from matplotlib import pyplot as plt
import shutil
import torchvision.utils as vutils
import torchvision.transforms as transforms
import torch
from scipy.misc import imsave, imread, imresize

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


def crop_file(origin_image_filename, mask_image_filename, filter_val, margin_factor, minArea=150, maxArea=1300):
    print(mask_image_filename)
    print(origin_image_filename)
    
    original = cv2.imread(origin_image_filename)
    original_npy = original.copy()
    original_npy = original_npy[:,:,::-1]
    
    
    mask = cv2.imread(mask_image_filename)
    if mask is None:
        no_mask.append(origin_image_filename)
        return 0

    mask[mask > filter_val] = 255
    mask[mask <= filter_val] = 0

    #binaryImg = cv2.Canny(mask,100,200)

    #h = cv2.findContours(binaryImg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
#    mask[mask > t] = 255
#    mask[mask <= t] = 0

    ### To grayscale and normalize
    mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    mask_gray = cv2.normalize(src=mask_gray, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

    ### Auto binary threshold
    (thresh, mask_binary) = cv2.threshold(mask_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    ret, thresh = cv2.threshold(mask_binary, 127, 255, 0)
    h = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #h = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    

    
    contours = h[1]
    print(len(contours))
    
    img_preview = original.copy()
    
    final_mask = np.ones(mask.shape,np.uint8)*255
    
    base_filename = os.path.splitext(os.path.basename(origin_image_filename))[0]
    npy_outdir = os.path.join('{}/npy/'.format(ROOT_FOLDER))
    if not os.path.exists(npy_outdir): os.makedirs(npy_outdir)
    
    
    filename = os.path.join('{}/{}_output'.format(ROOT_FOLDER, ntpath.basename(origin_image_filename)))
    #if not os.path.exists(filename): os.makedirs(filename)     

    crops_outdir = os.path.join('{}/crops'.format(filename))
    preview_outdir = os.path.join('{}/preview'.format(filename))
    
    mask_filename = os.path.join(preview_outdir, '%s_mask.png'%base_filename)  
    cv2.imwrite(mask_filename, mask_binary)
    
    if not os.path.exists(crops_outdir): os.makedirs(crops_outdir) 
    if not os.path.exists(preview_outdir): os.makedirs(preview_outdir) 
    
    
    index = 1
    
###txt file###
    index_name = os.path.join(preview_outdir, 'sample_submission.csv')
   # print("index_name:",index_name)
   # print("preview_outtdir",preview_outdir)
    #index_file = open(index_name,"w+")
###done###
    image_dict = None
    
    #classify_text = "datasets/sample_submission.csv"
    
    
    f = open(index_name, 'w') 
    print('{},{}'.format('name', 'positive'), file=f)
            
     
    for i in range(len(contours)):
        cnt = contours[i]
        
        area=cv2.contourArea(cnt)
        
        if area < minArea or area > maxArea:
            continue
        
        #index_file.write("%d " % (index))
        print("------i:",index)
        
        x, y, w, h = cv2.boundingRect(cnt)
        
        if CROP_METHOD == 'Margin':
            wm = w * margin_factor
            hm = h * margin_factor

            x -= wm
            y -= hm
            w += 2 * wm
            h += 2 * hm
            x = max(0, x)
            y = max(0, y)
            X = min(x + w, mask.shape[1])
            Y = min(y + h, mask.shape[0])
            w = X - x
            h = Y - y
        elif CROP_METHOD == 'Square': 
            x = x + int(w/2) - int(SQUARE_EDGE/2)
            x = max(x, 0)
            y = y + int(h/2) - int(SQUARE_EDGE/2)
            y = max(y, 0)
            w = SQUARE_EDGE
            h = SQUARE_EDGE
            X = min(x + w, mask.shape[1])
            Y = min(y + h, mask.shape[0])
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
        x1, y1, w1, h1 = int(x), int(y), int(w), int(h)
###txt file###
        #index_file.write("%d " % (i+1))
	#index_file.write("%d " % (x1))
	#index_file.write("%d " % (y1))
	#index_file.write("%d " % (w1))
	#index_file.write("%d\r\n" % (h1))
        #index_file.write("%d " % (i+1))
        #index_file.write("%d " % (x1))
        #index_file.write("%d " % (y1))
        #index_file.write("%d " % (w1))
        #index_file.write("%d\r\n" % (h1))
###done ###
        
        print(index, area, x1, y1, w1, h1)
        
        cropped = original[y1:y1 + h1, x1:x1 + w1, :]
        cropped_npy = original_npy[y1:y1 + h1, x1:x1 + w1, :]
        
        cropped_filename = os.path.join(crops_outdir, '{}_{}.png'.format(base_filename, index))
        name_base = '{}_{}.png'.format(base_filename, index)
        
        print('{},{}'.format(name_base, 0.5), file=f)
    
        
        #index_file.write("%s 0\r\n" % (name_base))
        
        #print(cropped.mean())
        
        #if cropped.mean() > 15: # a black crop or fail to find bounding box
            #blue_channel = img_highlighted[:, :, 0]
            #blue_channel[img_highlighted > 253] = 255
        cv2.rectangle(img_preview, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 1)
        cv2.drawContours(img_preview,cnt,-1,(0,255,0),1)
            
        text = '{}'.format(index)
    
        cv2.putText(img_preview, text, (x1, y1 + h1), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), lineType=cv2.LINE_AA) 

        cv2.imwrite(cropped_filename, cropped)
        
        index = index + 1
        
        resize_image = cv2.resize(cropped_npy, (32, 32))
        
        m = np.array([resize_image])
        if image_dict is not None:
            image_dict = np.append(image_dict, m,  axis=0)
        else:
            image_dict = m
        
        
    preview_filename = os.path.join(preview_outdir, '%s_preview.png'%base_filename)    
    cv2.imwrite(preview_filename, img_preview)
    f.close()    
    print(preview_filename)
    
    
    preview_npy = os.path.join(npy_outdir, '%s.npy'%base_filename)    
    image = image_dict #np.array(image_dict)
    
    if image is None:
        return
    np.save(preview_npy, image)
    
    print(image.shape)
    image = np.transpose(image, (0,3,1,2))
    print(image.shape)
    
    preview_segpng = os.path.join(preview_outdir, '%s_seg.png'%base_filename)   
    vutils.save_image(torch.FloatTensor(image), preview_segpng ,nrow=10,padding=2, normalize=True)
    
    
    
    segpng = cv2.imread(preview_segpng)
    
    for i in range(index-1):
        text = '{}'.format(i+1)
        x1 = 34 * int(i%10)
        y1 = int(i/10) * 34
        h1 = 12
        print("x1, y1:", text, x1, y1+h1)
        cv2.putText(segpng, text, (x1, y1 + h1), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), lineType=cv2.LINE_AA) 

    preview_segpng_idx = os.path.join(preview_outdir, '%s_seg_idx.png'%base_filename) 
    cv2.imwrite(preview_segpng_idx, segpng)
    
    
import glob
import ntpath
import os
import shutil

import numpy as np


@time_it
def process_origin_image():

    # Split train set
    total_images = np.sort(glob.glob(os.path.join(ORIGIN_DIR, FILE_PATTERN)))
    print(total_images)
    print('Num of total images: {}'.format(len(total_images)))

    for source in total_images:
        filename = ntpath.basename(source)
        base_filename = os.path.splitext(filename)[0]
        print(base_filename)

        #image_filename = 'datasets/segment/test/{}/images/{}.png'.format(base_filename, base_filename)
        #mask_filename = 'datasets/segment/output/predict/test/colour/{}/channel_0.png'.format(base_filename)
        #image_filename = os.path.join(SEGMENT_TEST_DIR,'{}/images/{}.png'.format(base_filename, base_filename))
        image_filename = source
        if SEG_COLOR == 'colouronly':
            mask_filename = os.path.join(SEGMENT_TEST_DIR,'../output/predict/test/colour/{}/channel_0.png'.format(base_filename))
        else:
            #mask_filename = os.path.join(SEGMENT_TEST_DIR,'../output/predict/test/grey/{}/channel_0.png'.format(base_filename))
            mask_filename = os.path.join(SEGMENT_TEST_DIR,'../output/predict/test/grey/{}/channel_1.png'.format(base_filename))
     
        print('image_filename:{} mask_filename:{}'.format(image_filename, mask_filename))
        crop_file(image_filename, mask_filename, 100, 0.2, 150, 2000)

@time_it
def process_one(crop_margin):

    # Split train set
    total_images = np.sort(glob.glob(os.path.join(ORIGIN_DIR, FILE_PATTERN)))
    print(total_images)
    
    filename = ntpath.basename(total_images[0])
    base_filename = os.path.splitext(filename)[0]
    print(base_filename)

    image_filename = os.path.join(SEGMENT_TEST_DIR,'{}/images/{}.png'.format(base_filename, base_filename))
    if SEG_COLOR == 'colouronly':
        mask_filename = os.path.join(SEGMENT_TEST_DIR,'../output/predict/test/colour/{}/channel_0.png'.format(base_filename))
    else:
        mask_filename = os.path.join(SEGMENT_TEST_DIR,'../output/predict/test/grey/{}/channel_0.png'.format(base_filename))
        #mask_filename = os.path.join(SEGMENT_TEST_DIR,'../output/predict/test/grey/{}/channel_0.png'.format(base_filename))
    print('image_filename:{} mask_filename:{}'.format(image_filename, mask_filename))
    #crop_file(image_filename, mask_filename, 100, 0.2, 150, 2000)
    crop_file(image_filename, mask_filename, 100,crop_margin, 150, 2000)
                
    
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
    SQUARE_EDGE = args.square_edge
    CROP_METHOD = args.crop_method
    
    no_mask = []
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
    