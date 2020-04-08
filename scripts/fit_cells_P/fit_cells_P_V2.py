import cv2,shutil,os
import numpy as np
import basefun as bf
from tqdm import tqdm

def get_cell_nuclei_mask(img, value):
    ret_, thresh = cv2.threshold(img, value, 255, cv2.THRESH_BINARY_INV)
    image_, contours, hierarchy_ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    [_h, _w] = img.shape
    xo = _w/2
    yo = _h/2
    long_ = 200
    contours_best = []
    area_max = 0
    _long = 0
    if len(contours) == 0:
        return 0
    for cnt in range(0, len(contours)):
        x,y,w,h=cv2.boundingRect(contours[cnt])
        xo2 = x+w/2
        yo2 = y+h/2
        _long = ((xo-xo2)**2+(yo-yo2)**2)**(1/2)
        if _long < long_:
            contours_best = contours[cnt]
            long_ = _long
    [w_img,h_img] = thresh.shape
    if (0 in contours_best) or ((w_img-1) in contours_best) or ((h_img-1) in contours_best):
        return 0
    if not type(contours_best) == np.ndarray:
        return 0
    area = cv2.contourArea(contours_best)
    if area < 871:
        return 0
    hull = cv2.convexHull(contours_best)
    area2 = cv2.contourArea(hull)
    
    if area == 0 or area2 == 0:
        return 0
    rule = area/area2
    if rule < 0.9:
        return 0
    return 1

if __name__ == "__main__":
    dstroot = '51'
    listcells = os.listdir(dstroot)
    cellsinfo = []
    for n,i in zip(listcells,tqdm(range(len(listcells)))):
        cellpath = os.path.join(dstroot, n)
#         print(cellpath)
        img = cv2.imread(cellpath)
        img_gray = cv2.imread(cellpath, 0)
        img_gray = bf.get_fit_img(img_gray)
        value_1,value_2 = bf.get_2value(img_gray)
        sign = get_cell_nuclei_mask(img_gray, value_1)
        if sign == 1:
            newpath = os.path.join('valid', n)
            shutil.copy(cellpath, newpath)
