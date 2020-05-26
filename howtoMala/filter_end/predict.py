# -*- coding: utf-8 -*-
# coding:utf-8
from ctypes import *
import math, cv2, time, os, random, json, shutil
import pandas as pd
import numpy as np
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

def sample(probs):
    s = sum(probs)
    probs = [a/s for a in probs]
    r = random.uniform(0, 1)
    for i in range(len(probs)):
        r = r - probs[i]
        if r <= 0:
            return i
    return len(probs)-1

def c_array(ctype, values):
    arr = (ctype*len(values))()
    arr[:] = values
    return arr

class BOX(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("w", c_float),
                ("h", c_float)]
class DETECTION(Structure):
    _fields_ = [("bbox", BOX),
                ("classes", c_int),
                ("prob", POINTER(c_float)),
                ("mask", POINTER(c_float)),
                ("objectness", c_float),
                ("sort_class", c_int)]


class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]

class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]



#lib = CDLL("/home/pjreddie/documents/darknet/libdarknet.so", RTLD_GLOBAL)
lib = CDLL("./libdarknet.so", RTLD_GLOBAL)
lib.network_width.argtypes = [c_void_p]
lib.network_width.restype = c_int
lib.network_height.argtypes = [c_void_p]
lib.network_height.restype = c_int

predict = lib.network_predict
predict.argtypes = [c_void_p, POINTER(c_float)]
predict.restype = POINTER(c_float)

set_gpu = lib.cuda_set_device
set_gpu.argtypes = [c_int]

make_image = lib.make_image
make_image.argtypes = [c_int, c_int, c_int]
make_image.restype = IMAGE

get_network_boxes = lib.get_network_boxes
get_network_boxes.argtypes = [c_void_p, c_int, c_int, c_float, c_float, POINTER(c_int), c_int, POINTER(c_int)]
get_network_boxes.restype = POINTER(DETECTION)

make_network_boxes = lib.make_network_boxes
make_network_boxes.argtypes = [c_void_p]
make_network_boxes.restype = POINTER(DETECTION)

free_detections = lib.free_detections
free_detections.argtypes = [POINTER(DETECTION), c_int]

free_ptrs = lib.free_ptrs
free_ptrs.argtypes = [POINTER(c_void_p), c_int]

network_predict = lib.network_predict
network_predict.argtypes = [c_void_p, POINTER(c_float)]

reset_rnn = lib.reset_rnn
reset_rnn.argtypes = [c_void_p]

load_net = lib.load_network
load_net.argtypes = [c_char_p, c_char_p, c_int]
load_net.restype = c_void_p

do_nms_obj = lib.do_nms_obj
do_nms_obj.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

do_nms_sort = lib.do_nms_sort
do_nms_sort.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

free_image = lib.free_image
free_image.argtypes = [IMAGE]

letterbox_image = lib.letterbox_image
letterbox_image.argtypes = [IMAGE, c_int, c_int]
letterbox_image.restype = IMAGE

load_meta = lib.get_metadata
lib.get_metadata.argtypes = [c_char_p]
lib.get_metadata.restype = METADATA

load_image = lib.load_image_color
load_image.argtypes = [c_char_p, c_int, c_int]
load_image.restype = IMAGE

rgbgr_image = lib.rgbgr_image
rgbgr_image.argtypes = [IMAGE]

predict_image = lib.network_predict_image
predict_image.argtypes = [c_void_p, IMAGE]
predict_image.restype = POINTER(c_float)

def classify(net, meta, im):
    out = predict_image(net, im)
    res = []
    for i in range(meta.classes):
        res.append((meta.names[i], out[i]))
    res = sorted(res, key=lambda x: -x[1])
    return res

def detect(net, meta, image, thresh=.5, hier_thresh=.5, nms=.45):
    im = load_image(image, 0, 0)
    num = c_int(0)
    pnum = pointer(num)
    predict_image(net, im)
    dets = get_network_boxes(net, im.w, im.h, thresh, hier_thresh, None, 0, pnum)
    num = pnum[0]
    if (nms): do_nms_obj(dets, num, meta.classes, nms);

    res = []
    for j in range(num):
        for i in range(meta.classes):
            if dets[j].prob[i] > 0:
                b = dets[j].bbox
                res.append((meta.names[i], dets[j].prob[i], (b.x, b.y, b.w, b.h)))
    res = sorted(res, key=lambda x: -x[1])
    free_image(im)
    free_detections(dets, num)
    return res

def save_json(info, savefile):
    with open(savefile, 'w') as file:
        file.write(json.dumps(info, indent=2, ensure_ascii=False))
    return

#box去重
def _filter3(boxes):
    for i in range(len(boxes)-1):
        b1 = boxes[i]
        b1x, b1y = int((b1["x2"] + b1["x1"]) / 2), int((b1["y2"] + b1["y1"]) / 2)
        for j in range(i+1, len(boxes)):
            b2 = boxes[j]
            if b2['class'] == 'drop':
                continue
            b2x, b2y = int((b2["x2"] + b2["x1"]) / 2), int((b2["y2"] + b2["y1"]) / 2)
            dst = int(math.sqrt(math.pow((b2x - b1x), 2) + math.pow((b2y - b1y), 2)))
            if dst <= 5:
                #print("same ", dst, b1, b2)
                if b1['score'] > b2['score']:
                    boxes[j]['class'] = "drop"
                else:
                    boxes[i]['class'] = "drop"
    newlists = []
    for i in boxes:
        if i['class'] == 'drop':
            continue
        newlists.append(i)
    return newlists

def _filter2(boxes):
    invalid = False
    cntk, cntm = 0, 0
    #个数检查
    for j in boxes:
        classname = j["class"]
        if classname == 'kernel':
            cntk = cntk + 1
        elif classname == 'mid':
            cntm = cntm + 1
    if cntk < 1 or (cntk + cntm) >= 5 or cntm >=2 :
        invalid = True
        return invalid

    #得分检查, 大于70分能够基本保留valid，valid只删除了51个
    invalid = True
    for j in boxes:
        score, classname = j["score"], j["class"]
        if classname != 'kernel':
            continue
        if int(score*100) >= 60:
            invalid = False
            break
    if invalid is True:
        return invalid

    #长宽检查
    invalid = True
    wh_threhold = 9
    for j in boxes:
        w, h, classname = j["w"], j["h"], j["class"]
        if classname != 'kernel':
            continue
        if w > wh_threhold and h > wh_threhold:
            invalid = False
            break
        if w < wh_threhold or h < wh_threhold:
            invalid = True

    return invalid

def _findmaxbox(boxes):
    if len(boxes) == 0:
        return {}
    if len(boxes) < 2:
        return boxes[0]
    maxwh = 0
    _boxes = {}
    for i in boxes:
        w, h = int(i['w']), int(i['h'])
        if (w*h) > maxwh:
            maxwh = w * h
            _boxes = i
    return _boxes

def get_filePath_fileName_fileExt(filename):
    (filepath, tempfilename) = os.path.split(filename)
    (shotname, extension) = os.path.splitext(tempfilename)
    return filepath, shotname, extension

def yolo_init(cfg, weights, metadata):
    _net = load_net(cfg.encode('utf-8'), weights.encode('utf-8'), 0)
    _meta = load_meta(metadata.encode('utf-8'))
    return _net, _meta

# 计算16个小图中心点在大图的坐标
def get_XYo(long1=400, long2=100):
    out = []
    start_long = int(long2/2)
    N = int(long1/long2)
    for n in range(N*N):
        x = (n%N) * long2 + start_long
        y = (int(n/N)) * long2 + start_long
        xy = [x,y]
        out.append(xy)
    return out

# 计算矩形框相对于距离最近的小图的相对坐标
def seg_xoy(x1, y1, x2, y2):
    Xo = int((x1+x2)/2)
    Yo = int((y1+y2)/2)
    XYo_16 = get_XYo(400, 100)
    long_1 = 1000
    sign = -1
    cnt = 0
    for n in XYo_16:
        x = n[0]
        y = n[1]
        long_2 = ((x-Xo)**2 + (y-Yo)**2)**(1/2)
        if long_2 < long_1:
            long_1 = long_2
            sign = cnt
        cnt = cnt + 1
    XY = XYo_16[sign]
    x1_out = min(100, max(0, x1-XY[0]+50))
    y1_out = min(100, max(0, y1-XY[1]+50))
    x2_out = min(100, max(0, x2-XY[0]+50))
    y2_out = min(100, max(0, y2-XY[1]+50))
    return sign,x1_out,y1_out,x2_out,y2_out

# 在小图上画框
def plot_oncell(imgpath, x1, y1, x2, y2):
    img = cv2.imread(imgpath)
    first_point = (x1, y1)
    last_point = (x2, y2)
    cv2.rectangle(img, first_point, last_point, (0,255,0),1)
    cv2.imwrite(imgpath, img)

def save_limit_cells(_imgpath, _x1, _y1, _x2, _y2, limit):
    area = (_x2 - _x1)*(_y2 - _y1)
    if area > limit:
        newname = os.path.join('cells_1400/temp', _imgpath.split('/')[1])
        shutil.copy(_imgpath, newname)


#if __name__ == "__main__":
def main1(net, meta, concat_info):
    print("================")
    testdir="output2/"
    dir_or_files = os.listdir(testdir)
    columns = ["cell", "x1", "y1", "x2", "y2", "w", "h", "score"]
    cellsinfo = []
    imgs = []
    for i in dir_or_files:
        path1 = os.path.join(testdir, i)
        ext = os.path.splitext(path1)[1]
        ext = ext.lower()
        if not ext in ['.jpg', '.png', '.jpeg', '.bmp']:
            continue

        imgs.append(path1)

    if len(imgs) < 1:
        exit()

    cfg, metadata = "names-data/yolov3-voc-predict.cfg", "names-data/voc.data"
    weights = "yolov3-voc_40100.weights.0501.concat"
    #weights = "yolov3-voc_27900.weights.0505"
    #net, meta = yolo_init(cfg, weights, metadata)
    
    dst_dict = concat_info

    cnti, cntv = 0, 0
    for k in range(len(imgs)):
        imgpath = imgs[k]
        t1 = int(time.time()*1000)
        r = detect(net, meta, imgpath.encode('utf-8'), thresh=0.5, hier_thresh=0.5, nms=0.45)
        t2 = int(time.time()*1000)
        print("%d/%d %d  %d" %(k, len(imgs), len(r), t2 - t1))
        original_image = cv2.imread(imgpath)
        dic = {"boxes": []}

        _temp1 = dst_dict[imgpath]
        for i in range(len(r)):
            classname = str(r[i][0])
            x1, y1 = int(r[i][2][0]-r[i][2][2]/2), int(r[i][2][1]-r[i][2][3]/2)
            x2, y2 = int(r[i][2][0]+r[i][2][2]/2), int(r[i][2][1]+r[i][2][3]/2)
            w, h, score, classname = x2 - x1, y2 - y1, round(r[i][1], 2), str(r[i][0])

            _sign, _x1, _y1, _x2, _y2 = seg_xoy(x1, y1, x2, y2)
            _imgpath = tuple(_temp1[_sign].values())[0]
            #plot_oncell(_imgpath, _x1, _y1, _x2, _y2)
            if score < 0.85:
                continue
            save_limit_cells(_imgpath, _x1, _y1, _x2, _y2, 1400)

            #if score < 0.90:
            #    continue
