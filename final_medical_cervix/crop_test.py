import numpy as np
import cv2
import os
import sys
import ntpath
from matplotlib import pyplot as plt
import torchvision.utils as vutils
import torchvision.transforms as transforms
import torch
from scipy.misc import imsave, imread, imresize

ROOT_FOLDER = 'datasets/classify'


def crop_file(origin_image_filename, mask_image_filename, filter_val, margin_factor, minArea=150, maxArea= 1300):
    original = cv2.imread(origin_image_filename)
    mask = cv2.imread(mask_image_filename)

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
    h = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #h = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    

    masked = cv2.bitwise_and(original,original,mask=mask_binary)
    masked[np.where((masked == [0,0,0]).all(axis = 2))] = [255,255,255]
    
    
    contours = h[1]
    print(len(contours))
    
    img_preview = original.copy()
    
    final_mask = np.ones(mask.shape,np.uint8)*255
    
    
    base_filename = os.path.splitext(os.path.basename(origin_image_filename))[0]
    
    
    filename = os.path.join('{}/{}_output'.format(ROOT_FOLDER, ntpath.basename(origin_image_filename)))
    if not os.path.exists(filename): os.makedirs(filename)     

    crops_outdir = os.path.join('{}/crops'.format(filename))
    preview_outdir = os.path.join('{}/preview'.format(filename))
    
    mask_filename = os.path.join(preview_outdir, 'mask.png')  
    cv2.imwrite(mask_filename, mask_binary)
    
    if not os.path.exists(crops_outdir): os.makedirs(crops_outdir) 
    if not os.path.exists(preview_outdir): os.makedirs(preview_outdir) 
    
    
    index = 0
    
    image_dict = None
    
    for i in range(len(contours)):
        cnt = contours[i]
        
        area=cv2.contourArea(cnt)
        
        if area < minArea or area > maxArea:
            continue
        
        x, y, w, h = cv2.boundingRect(cnt)
        print(index, area, x, y, w, h)
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
        
        
        x1, y1, w1, h1 = int(x), int(y), int(w), int(h)

        
        cropped = original[y1:y1 + h1, x1:x1 + w1, :]
        cropped_filename = os.path.join(crops_outdir, '{}.png'.format(index))
        
        #print(cropped.mean())
        
        #if cropped.mean() > 15: # a black crop or fail to find bounding box
            #blue_channel = img_highlighted[:, :, 0]
            #blue_channel[img_highlighted > 253] = 255
        cv2.rectangle(img_preview, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 1)
        cv2.drawContours(img_preview,cnt,-1,(0,255,0),1)
            
        text = '{}'.format(index)
    
        cv2.putText(img_preview, text, (x1, y1 + h1), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), lineType=cv2.LINE_AA) 

        #cv2.imwrite(cropped_filename, cropped)
        resize_image = imresize(cropped, [32, 32], interp='nearest')
        #resize_image = cv2.resize(cropped, (32, 32))
        
        cv2.imwrite(cropped_filename, resize_image)
        
        m = np.array([resize_image])
        if image_dict is not None:
            image_dict = np.append(image_dict, m,  axis=0)
        else:
            image_dict = m
        
        index = index + 1
        
        
        
        
    preview_filename = os.path.join(preview_outdir, 'preview.png')    
    cv2.imwrite(preview_filename, img_preview)
    
    
    print(image_dict.shape)
    
    preview_npy = os.path.join(preview_outdir, '%s.npy'%base_filename)    
    image = image_dict #np.array(image_dict)
    
    
    np.save(preview_npy, image)
    
    print(image.shape)
    image = np.transpose(image, (0,3,1,2))
    print(image.shape)
    
    preview_segpng = os.path.join(preview_outdir, '%s_seg.png'%base_filename)   
    vutils.save_image(torch.FloatTensor(image), preview_segpng ,nrow=5,normalize=True)
        


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

        image_filename = 'datasets/segment/test/{}/images/{}.png'.format(base_filename, base_filename)
        mask_filename = 'datasets/segment/output/predict/test/colour/{}/channel_0.png'.format(base_filename)
        print('image_filename:{} mask_filename:{}'.format(image_filename, mask_filename))
        crop_file(image_filename, mask_filename, 60, 0.2, 120, 2000)

                
    
if __name__ == '__main__':
    process_origin_image()
    
