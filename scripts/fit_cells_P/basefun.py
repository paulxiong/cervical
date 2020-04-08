import os,time
import cv2
import numpy as np
import matplotlib.pyplot as plt
import copy
from numba import jit

def get_fit_img(img):
    dst = cv2.fastNlMeansDenoising(img,None,8,7,21)
    return dst

@jit
def get_mean(temp, long_=10):
    temp_1 = []
    for m in range(0+long_, 255-long_):
        temp_1.append(temp[m-long_:m+long_].mean())
    temp_2 = np.array(temp_1)
    temp_out = np.zeros(255)
    temp_out[0+long_: 255-long_] = temp_2
    return temp_out

@jit
def grien_value(temp):
    temp_1 = np.zeros(255)
    temp_1[1:255] = temp[0:254]
    temp_out = temp - temp_1
    temp_out = get_mean(temp_out, 10)
    return temp_out

@jit
def get_last2value(temp):
    sign1 = 0
    sign2 = 0
    cnt = 0
    value = 0
    temp_4 = temp[::-1]
    for k in range(0, len(temp_4)-1):
        if temp_4[k+1] > temp_4[k]:
            sign2 = sign1
            sign1 = 1
            if sign1 != sign2:
                cnt = cnt + 1
        else:
            sign2 = sign1
            sign1 = 0
            if sign1 != sign2:
                cnt = cnt + 1
        if cnt == 3:
            value = k
            break #!!!!!!!!!
    return 255-value

def get_2value(img, long_ = 10, chan = 0, mask = None, grien = 2):
    temp_2 = cv2.calcHist([img],[chan],mask,[256],[0,255])
    temp_4 = get_mean(temp_2, long_)
    temp_4 = get_mean(temp_4, 5)
    if grien == 2:
        temp_4 = grien_value(temp_4) #使用二阶导数更容易检测到细胞核像素阈值
    else:
        temp_4 = grien_value(grien_value(temp_4)) #用于检测细胞团或颜色深的细胞核
#    plt.figure("Image")
#    plt.imshow(img)
#    plt.figure("Image_value")
#    plt.plot(temp_4)
#    plt.figure("Image_value_gre")
#    plt.plot(grien_value(temp_4))
#    plt.figure("Image_value_gre2")
#    plt.plot(grien_value(grien_value(temp_4)))
#    plt.show()
    sign1 = 0
    sign2 = 0
    cnt = 0
    value_1 = 0
    value_2 = 0
    for k in range(0, len(temp_4)-1):
        if temp_4[k+1] > temp_4[k]:
            sign2 = sign1
            sign1 = 1
            if sign1 != sign2:
                cnt = cnt + 1
        else:
            sign2 = sign1
            sign1 = 0
            if sign1 != sign2:
                cnt = cnt + 1
        if cnt == 3:
            value_1 = k
            break #!!!!!!!!!
            #print(temp_4[k])
    value_2 = get_last2value(temp_4)
    return value_1,value_2
 
def get_img_open(img,fit):
    img_open = cv2.morphologyEx(img, cv2.MORPH_OPEN, fit)
    return img_open
 
def get_img_close(img,fit):
    img_close = cv2.morphologyEx(img, cv2.MORPH_CLOSE, fit)
    return img_close
 
