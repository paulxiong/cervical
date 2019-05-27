import numpy as np
import cv2
import os
import sys
import ntpath
from matplotlib import pyplot as plt

ROOT_FOLDER = '../../../datasets/segment'


def crop_file(origin_image_filename, mask_image_filename, filter_val, margin):
    margin_factor = 0.2
    minArea=50
    maxArea= 1300
    
    original = cv2.imread(origin_image_filename)
    mask = cv2.imread(mask_image_filename)

    mask[mask > filter_val] = 255
    mask[mask <= filter_val] = 0

    binaryImg = cv2.Canny(mask,100,200)

    h = cv2.findContours(binaryImg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours = h[1]
    print(len(contours))
    
    final_mask = np.ones(mask.shape,np.uint8)*255
    cv2.drawContours(final_mask,contours,-1,(0,255,0),3)
    #cv2.imwrite('final_mask.png',final_mask)

    img_preview = original.copy()
    
    filename = os.path.join('{}/{}_output'.format(ROOT_FOLDER, ntpath.basename(origin_image_filename)))
    if not os.path.exists(filename): os.makedirs(filename)     

    crops_outdir = os.path.join('{}/crops'.format(filename))
    preview_outdir = os.path.join('{}/preview'.format(filename))
    
    if not os.path.exists(crops_outdir): os.makedirs(crops_outdir) 
    if not os.path.exists(preview_outdir): os.makedirs(preview_outdir) 
    
    for i in range(len(contours)):
        cnt = contours[i]

        area=cv2.contourArea(cnt)
        #if area < minArea or area > maxArea:
        #    continue
        
        x, y, w, h = cv2.boundingRect(cnt)
        
        
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

        #blue_channel = img_highlighted[:, :, 0]
        #blue_channel[img_highlighted > 253] = 255
        cv2.rectangle(img_preview, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 3)

        text = '{}'.format(i)

        cv2.putText(img_preview, text, (x1, y1 + h1), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), lineType=cv2.LINE_AA) 

        cropped = original[y1:y1 + h1, x1:x1 + w1, :]
        cropped_filename = os.path.join(crops_outdir, '{}.png'.format(i))

        if cropped.mean() > 15: # a black crop or fail to find bounding box
            cv2.imwrite(cropped_filename, cropped)
    
    preview_filename = os.path.join(preview_outdir, 'preview.png')    
    cv2.imwrite(preview_filename, img_preview)
    
#crop_file('IMG030x032.png', 'channel_0.png', 254, 25)
if __name__ == "__main__":
    image_filename = '../../../datasets/segment/test/{}/images/{}.png'.format(sys.argv[1], sys.argv[1])
    mask_filename = '../../../datasets/segment/output/predict/test/colour/{}/channel_0.png'.format(sys.argv[1])
    print('image_filename:{} mask_filename:{}'.format(image_filename, mask_filename))
    crop_file(image_filename, mask_filename, 254, 25)


