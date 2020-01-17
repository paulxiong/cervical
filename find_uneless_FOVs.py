import cv2
import numpy as np

def get_cell_cnt(img_, area_limit=12):  # 单张FOV 2.1ms
    x, y = img_.shape[0:2]
    img_ = cv2.resize(img_, (int(y/4), int(x/4)))
    ret, binary = cv2.threshold(img_, 95, 255, cv2.THRESH_BINARY)
    kernel_1 = np.ones((3,3),np.uint8) # 给图像闭运算定义核
    closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel_1)
    closing_x = closing.shape[0]
    closing_y = closing.shape[1]
    closing[:,0] = 255
    closing[:,closing_y-1] = 255
    closing[0,:] = 255
    closing[closing_x-1,:] = 255
    # 检测图像连通区（输入为二值化图像）
    image, contours, hierarchy = cv2.findContours(closing,1,2)
    cnt_cells = 0
    for n in range(len(contours)):
        cnt = contours[n]
        area = cv2.contourArea(cnt)
        if area > area_limit:
            cnt_cells = cnt_cells + 1
    return cnt_cells

def get_FOV_sign(img, limit=2):
    cnt = get_cell_cnt(img)
    sign = 0 # sign=1时，该FOV无效
    if cnt < limit:
        sign = 1
    return sign

for path_ in open('list.txt'):
    path = path_[:-1]
    image = cv2.imread(path,0)
    sign = get_FOV_sign(image)
    if sign == 1:
        print(path)