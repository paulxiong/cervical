import numpy as np
import cv2
import os
import sys
import ntpath
from matplotlib import pyplot as plt

ROOT_FOLDER = 'datasets/classify'


def crop_file(origin_image_filename, mask_image_filename, filter_val, margin):
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
    #h = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    h = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    

    
    contours = h[1]
    print(len(contours))
    
    final_mask = np.ones(mask.shape,np.uint8)*255
    cv2.drawContours(final_mask,contours,-1,(0,255,0),3)


    img_preview = original.copy()
    
    filename = os.path.join('{}/{}_output'.format(ROOT_FOLDER, ntpath.basename(origin_image_filename)))
    if not os.path.exists(filename): os.makedirs(filename)     

    crops_outdir = os.path.join('{}/crops'.format(filename))
    preview_outdir = os.path.join('{}/preview'.format(filename))
    
    mask_filename = os.path.join(preview_outdir, 'mask.png')  
    cv2.imwrite(mask_filename, mask)
    
    if not os.path.exists(crops_outdir): os.makedirs(crops_outdir) 
    if not os.path.exists(preview_outdir): os.makedirs(preview_outdir) 
    
    minArea=40
    index = 0

    for i in range(len(contours)):
        cnt = contours[i]
        
        area=cv2.contourArea(cnt)
        print(area)
        if area < minArea:
            continue
        
        x, y, w, h = cv2.boundingRect(cnt)

        wm = min(w + margin, 250)
        hm = min(h + margin, 250)

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
        
        if cropped.mean() > 15: # a black crop or fail to find bounding box
            #blue_channel = img_highlighted[:, :, 0]
            #blue_channel[img_highlighted > 253] = 255
            cv2.rectangle(img_preview, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 3)
    
            text = '{}'.format(index)
    
            cv2.putText(img_preview, text, (x, y + h1), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA) 

            cv2.imwrite(cropped_filename, cropped)
        
        index = index + 1
        
    preview_filename = os.path.join(preview_outdir, 'preview.png')    
    cv2.imwrite(preview_filename, img_preview)
    


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
        crop_file(image_filename, mask_filename, 253, 0)

                
    
if __name__ == '__main__':
    process_origin_image()
    
