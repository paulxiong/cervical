import numpy as np
import cv2
import os
import sys
import ntpath
from matplotlib import pyplot as plt

ROOT_FOLDER = 'datasets/segment/'


def crop_file(origin_image_filename, mask_image_filename, clazz,  filter_val, margin_factor, minArea=0, maxArea= 10000):
    original = cv2.imread(origin_image_filename)
    mask = cv2.imread(mask_image_filename)

    mask[mask < 255] = 0 
    mask[:, :, 1] = 0
    mask[:, :, 2] = 0
    mask[np.where((mask == [255,0,0]).all(axis = 2))] = [255,255,255]

    mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    mask_gray = cv2.normalize(src=mask_gray, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

    ### Auto binary threshold
    (thresh, mask_binary) = cv2.threshold(mask_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    h = cv2.findContours(mask_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #h = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    
    masked = cv2.bitwise_and(original,original,mask=mask_binary)
    masked[np.where((masked == [0,0,0]).all(axis = 2))] = [255,255,255]

    
    contours = h[1]
    print(len(contours))
    
    img_preview = original.copy()
    
    final_mask = np.ones(mask.shape,np.uint8)*255
   
    crops_outdir = os.path.join(ROOT_FOLDER, 'train_crops', clazz)
    preview_outdir = os.path.join(ROOT_FOLDER, 'train_crops_preview', clazz)
    
    
    if not os.path.exists(crops_outdir): os.makedirs(crops_outdir) 
    if not os.path.exists(preview_outdir): os.makedirs(preview_outdir) 
    
    filename = ntpath.basename(origin_image_filename)
    base_filename = os.path.splitext(filename)[0]
    index = 0

    for i in range(len(contours)):
        cnt = contours[i]
        
        area=cv2.contourArea(cnt)
        
        if area < minArea :
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

        
        cropped = masked[y1:y1 + h1, x1:x1 + w1, :]
        cropped_filename = os.path.join(crops_outdir, '{}.png'.format(base_filename))
        #print("cropped", cropped_filename)
        #print(cropped.mean())
        
        cv2.rectangle(img_preview, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 1)
        cv2.drawContours(img_preview,cnt,-1,(0,255,0),1)
            
        text = '{}'.format(index)
    
        cv2.putText(img_preview, text, (x1, y1 + h1), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), lineType=cv2.LINE_AA) 

        cv2.imwrite(cropped_filename, cropped)
        
        index = index + 1
        
        
    preview_filename = os.path.join(preview_outdir, '{}.png'.format(base_filename))    
    cv2.imwrite(preview_filename, img_preview)
    


import glob
import ntpath
import os
import shutil

import numpy as np

ClassNames = ["abnormal", "normal"]

def process_origin_image():
    FILE_PATTERN = '*.BMP'

    
    for clazz in ClassNames:
        total_images = np.sort(glob.glob(os.path.join('datasets/segment/train1/', clazz, FILE_PATTERN)))
        print(total_images)

        for source in total_images:
            filename = ntpath.basename(source)
            base_filename = os.path.splitext(filename)[0]
            print(base_filename)

            image_filename = 'datasets/segment/train1/{}/{}.BMP'.format(clazz, base_filename)
            mask_filename = 'datasets/segment/train1_mask/{}/{}-d.bmp'.format(clazz, base_filename)
            print('image_filename:{} mask_filename:{}'.format(image_filename, mask_filename))
            crop_file(image_filename, mask_filename, clazz, 70, 0)

                
    
if __name__ == '__main__':
    process_origin_image()
    
