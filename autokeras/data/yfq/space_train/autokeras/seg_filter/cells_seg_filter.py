import cv2
import numpy as np
import time
print(time.time())
for n in open('list.txt'):
    path = n[:-1]
    img = cv2.imread(path)
    gray =cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 75, 255, cv2.THRESH_BINARY)
    kernel = np.ones((21,21),np.uint8)
    kernel_1 = np.ones((101,101),np.uint8)
    closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel_1)
    opening_x = opening.shape[0]
    opening_y = opening.shape[1]
    opening[:,0] = 255
    opening[:,opening_y-1] = 255
    opening[0,:] = 255
    opening[opening_x-1,:] = 255
    image, contours, hierarchy = cv2.findContours(opening,1,2)
    count2 = 0
    for m in range(len(contours)):
        cnt = contours[m]
        area = cv2.contourArea(cnt)
        if area > 20000:
            count2 = count2 + 1
    if count2-1 > 0:
        f1 = open('record.txt','a')
        f1.write(n)
        f1.close()
print(time.time())

