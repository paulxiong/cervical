import os, cv2, json
import numpy as np
import pandas as pd
import time

def imglists(_rootdir):
    dir_or_files = os.listdir(_rootdir)
    imgs = []
    for i in dir_or_files:
        path1 = os.path.join(_rootdir, i)
        ext = os.path.splitext(path1)[1]
        ext = ext.lower()
        if not ext in ['.jpg', '.png', '.jpeg', '.bmp']:
            continue
        imgs.append(path1)
    return imgs

def main1():
    testdir="cells_82"
    if not os.path.exists('output2'):
        os.makedirs('output2')
    imgs = imglists(testdir)
    columns = ["img", "cell", "row", "col", "x", "y"]
    cellsinfo = []
    slide = 100
    temp_keys = []
    temp_values = []
    for i in range(0, len(imgs)+16, 16):
        concatimg = os.path.join('output2', str(i) + ".png")
        new_img = np.zeros([400, 400, 3])
        index = 0
        bndbox = []
        cells_16 = []
        for row in range(4):
            for col in range(4):
                x, y = col*slide, row*slide
                if i + index >= len(imgs):
                    continue
                imgfile = imgs[i + index]
                img = cv2.imread(imgfile)
                if not (img.shape[0]==100 and img.shape[1]==100):
                    continue
                cells_16.append({str(index):imgfile})
                index = index + 1
                new_img[y:y+100, x:x+100] = img
                cellsinfo.append([concatimg, imgfile, row, col, x, y])
        cv2.imwrite(concatimg, new_img)
        temp_keys.append(concatimg)
        temp_values.append(cells_16)
    out_dict = dict(zip(temp_keys,temp_values)) # 用字典记录拼图时小图路径、在大图的位置

    df = pd.DataFrame(cellsinfo, columns=columns)
    df.to_csv('all.csv', quoting = 1, mode = 'w', index = False, header = True, encoding='utf-8')
    return out_dict
