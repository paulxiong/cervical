#!python3
# coding: utf-8
#pylint: disable=R, W0401, W0614, W0703
from ctypes import *
import math, random, os, time, platform
import cv2
import numpy as np
from tqdm import tqdm

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
                ("sort_class", c_int),
                ("uc", POINTER(c_float)),
                ("points", c_int),
                ("embeddings", POINTER(c_float)),
                ("embedding_size", c_int),
                ("sim", c_float),
                ("track_id", c_int)]

class DETNUMPAIR(Structure):
    _fields_ = [("num", c_int),
                ("dets", POINTER(DETECTION))]

class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]

class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]

hasGPU = True
lib = None
sys_version = platform.linux_distribution()
sys_arch = platform.uname()[4]   #eg:x86_64 amd64 win32
if sys_arch == 'x86_64':
    lib = CDLL("./libdarknet.so.x64", RTLD_GLOBAL)
elif sys_arch == 'aarch64':
    lib = CDLL("./libdarknet.so.aarch64", RTLD_GLOBAL)
lib.network_width.argtypes = [c_void_p]
lib.network_width.restype = c_int
lib.network_height.argtypes = [c_void_p]
lib.network_height.restype = c_int

copy_image_from_bytes = lib.copy_image_from_bytes
copy_image_from_bytes.argtypes = [IMAGE,c_char_p]

def network_width(net):
    return lib.network_width(net)

def network_height(net):
    return lib.network_height(net)

predict = lib.network_predict_ptr
predict.argtypes = [c_void_p, POINTER(c_float)]
predict.restype = POINTER(c_float)

if hasGPU:
    set_gpu = lib.cuda_set_device
    set_gpu.argtypes = [c_int]

init_cpu = lib.init_cpu

make_image = lib.make_image
make_image.argtypes = [c_int, c_int, c_int]
make_image.restype = IMAGE

get_network_boxes = lib.get_network_boxes
get_network_boxes.argtypes = [c_void_p, c_int, c_int, c_float, c_float, POINTER(c_int), c_int, POINTER(c_int), c_int]
get_network_boxes.restype = POINTER(DETECTION)

make_network_boxes = lib.make_network_boxes
make_network_boxes.argtypes = [c_void_p]
make_network_boxes.restype = POINTER(DETECTION)

free_detections = lib.free_detections
free_detections.argtypes = [POINTER(DETECTION), c_int]

free_batch_detections = lib.free_batch_detections
free_batch_detections.argtypes = [POINTER(DETNUMPAIR), c_int]

free_ptrs = lib.free_ptrs
free_ptrs.argtypes = [POINTER(c_void_p), c_int]

network_predict = lib.network_predict_ptr
network_predict.argtypes = [c_void_p, POINTER(c_float)]

reset_rnn = lib.reset_rnn
reset_rnn.argtypes = [c_void_p]

load_net = lib.load_network
load_net.argtypes = [c_char_p, c_char_p, c_int]
load_net.restype = c_void_p

load_net_custom = lib.load_network_custom
load_net_custom.argtypes = [c_char_p, c_char_p, c_int, c_int]
load_net_custom.restype = c_void_p

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

predict_image_letterbox = lib.network_predict_image_letterbox
predict_image_letterbox.argtypes = [c_void_p, IMAGE]
predict_image_letterbox.restype = POINTER(c_float)

network_predict_batch = lib.network_predict_batch
network_predict_batch.argtypes = [c_void_p, IMAGE, c_int, c_int, c_int,
                                   c_float, c_float, POINTER(c_int), c_int, c_int]
network_predict_batch.restype = POINTER(DETNUMPAIR)

def bounding_box(bounds):
    x, y, w, h = bounds
    xmin = x - (w / 2)
    xmax = x + (w / 2)
    ymin = y - (h / 2)
    ymax = y + (h / 2)
    # xmin, ymin might be negative value
    return int(max(0, xmin)), int(max(0, ymin)), int(xmax), int(ymax)

def get_images(rootpath):
    x = []
    for j in os.listdir(rootpath):
        path2 = os.path.join(rootpath, j)
        if os.path.isdir(path2):
            continue
        ext = os.path.splitext(path2)[1]
        ext = ext.lower()
        if not ext in ['.jpg', '.png', '.jpeg', '.bmp', '.JPG']:
            print('%s not image' % (path2))
        else:
            x.append(path2)
    return x

def get_filePath_fileName_fileExt(filename):
    (filepath, tempfilename) = os.path.split(filename)
    (shotname, extension) = os.path.splitext(tempfilename)
    return filepath, shotname, extension

class detect():
    def __init__(self, configPath, weightPath, metaPath, batch_size=20):
        self.configPath = configPath
        self.weightPath = weightPath
        self.metaPath = metaPath
        self.batch_size = batch_size

        self.net = load_net_custom(self.configPath.encode('utf-8'), self.weightPath.encode('utf-8'), 0, self.batch_size)
        self.meta = load_meta(self.metaPath.encode('utf-8'))
        self.net_width, self.net_height = (network_width(self.net), network_height(self.net))

    def img_slice(self, _img, size=608, padx=148, pady=128):
        w, h = _img.shape[1], _img.shape[0]
        slices, index = {}, 0
        prex2 = 0
        #loop 100的目的是使得滑动窗口能滑完整张图片，滑到边要判断了开始下一次滑动
        for i in range(100):
            x1 = 0
            if prex2 > 0:
                x1 = prex2 - padx #往上一张图片方向滑动pad个像素点
            x2 = x1 + size
            if prex2 >= w:
                break
            if x2 > w: #滑动窗口超出图片，那么对齐边线
                delta = x2 - w
                x1, x2 = x1 - delta, w
            prex2 = x2
            prey2 = 0
            for j in range(100):
                y1 = 0
                if prey2 > 0:
                    y1 = prey2 - pady #往上一张图片方向滑动pad个像素点
                y2 = y1 + size
                if prey2 >= h:
                    break
                if y2 > h: #滑动窗口超出图片，那么对齐边线
                    delta = y2 - h
                    y1, y2 = y1 - delta, h
                slices[str(index)] = {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'indexx': i, 'indexy': j, 'index': index}
                prey2, index = y2, index + 1
        return slices

    def batchDetect(self, slices, _img, thresh= 0.25, hier_thresh=.5, nms=.45):
        image_list = []
        for i in range(len(slices.keys())):         #按照上面计算得到的坐标切割
            item = slices[str(i)]
            x1, y1, x2, y2 = item['x1'], item['y1'], item['x2'], item['y2']
            image_list.append(_img[y1:y2, x1:x2])

        pred_height, pred_width, c = image_list[0].shape
        img_list = []
        for custom_image_bgr in image_list:
            custom_image = cv2.cvtColor(custom_image_bgr, cv2.COLOR_BGR2RGB)
            if custom_image.shape[1] != self.net_width or custom_image.shape[0] != self.net_height:
                custom_image = cv2.resize(custom_image, (self.net_width, self.net_height), interpolation=cv2.INTER_NEAREST)
            custom_image = custom_image.transpose(2, 0, 1)
            img_list.append(custom_image.copy()) #copy()为了加速ascontiguousarray

        _arr = np.concatenate(img_list, axis=0)
        arr = _arr.copy() #copy()为了加速ascontiguousarray
        arr = np.ascontiguousarray(arr.flat, dtype=np.float32) / 255.0
        data = arr.ctypes.data_as(POINTER(c_float))
        im = IMAGE(self.net_width, self.net_height, c, data)

        batch_dets = network_predict_batch(self.net, im, self.batch_size, pred_width, pred_height, thresh, hier_thresh, None, 0, 0)
        results = {}

        for b in range(self.batch_size):
            results[str(b)] = []
            num = batch_dets[b].num
            dets = batch_dets[b].dets
            if nms:
                do_nms_obj(dets, num, self.meta.classes, nms)
            for i in range(num):
                det = dets[i]
                score = -1
                label, labelID = None, -1
                for c in range(det.classes):
                    p = det.prob[c]
                    if p > score:
                        score = p
                        label = self.meta.names[c]
                        labelID = c
                if score > thresh:
                    box = det.bbox
                    x1, y1, x2, y2 = map(int,(box.x - box.w / 2, box.y - box.h / 2, box.x + box.w / 2, box.y + box.h / 2))
                    results[str(b)].append({'label': label, 'labelid': labelID, 'score': round(score, 2), 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2})
        free_batch_detections(batch_dets, self.batch_size)
        return results

    def resultsConcat(self, _slices, _results):
        results = []
        for i in _results.keys():
            for j in _results[i]:
                sx1, sy1 = _slices[i]['x1'], _slices[i]['y1'] # 切片在原FOV图的位置
                cx1, cy1, cx2, cy2 = j['x1'], j['y1'], j['x2'], j['y2'] # 细胞在切片的位置
                x1, y1, x2, y2 = sx1 + cx1, sy1 + cy1, sx1 + cx2, sy1 + cy2 # 细胞在原FOV图的位置
                score, label, labelID = j['score'], j['label'], j['labelid']
                results.append({'label': label, 'labelid': labelID, 'score': int(score*100), 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2})
        return results

    def simpleNMS(self, _results, thresh):
        __results, keep = [], []
        if len(_results) < 1:
            return keep
        for i in _results:
            __results.append([int(i['x1']), int(i['y1']), int(i['x2']), int(i['y2']), int(i['score']), int(i['labelid'])])
        dets = np.array(__results)
        #x1、y1、x2、y2、以及score赋值, （x1、y1）（x2、y2）为box的左上和右下角标
        x1 = dets[:, 0]
        y1 = dets[:, 1]
        x2 = dets[:, 2]
        y2 = dets[:, 3]
        scores = dets[:, 4]
        labels = dets[:, 5]

        areas = (x2 - x1 + 1) * (y2 - y1 + 1) #每一个候选框的面积
        order = scores.argsort()[::-1] #order是按照score降序排序的，得到的是排序的本来的索引，不是排完序的原数组, ::-1表示逆序
        while order.size > 0:
            i = order[0]
            keep.append({'label': labels[i], 'score': scores[i], 'x1': x1[i], 'y1': y1[i], 'x2': x2[i], 'y2': y2[i]})
            #计算当前概率最大矩形框与其他矩形框的相交框的坐标, 由于numpy的broadcast机制，得到的是向量
            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.minimum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.maximum(y2[i], y2[order[1:]])

            #计算相交框的面积,注意矩形框不相交时w或h算出来会是负数，需要用0代替
            w = np.maximum(0.0, xx2 - xx1 + 1)
            h = np.maximum(0.0, yy2 - yy1 + 1)
            inter = w * h
            #计算重叠度IoU
            ovr = inter / (areas[i] + areas[order[1:]] - inter)

            #找到重叠度不高于阈值的矩形框索引
            inds = np.where(ovr <= thresh)[0]
            #将order序列更新，由于前面得到的矩形框索引要比矩形框在原order序列中的索引小1，所以要把这个1加回来
            order = order[inds + 1]
        return keep

    def removeSmall(self, _results):
        __results = []
        for i in _results:
            x1, y1, x2, y2, score = int(i['x1']), int(i['y1']), int(i['x2']), int(i['y2']), int(i['score'])
            w, h = max(x2 - x1, 0), max(y2 - y1, 0)
            if w*h < 1400 or score < 50:
                continue
            __results.append(i)
        return __results

    def drawRectangle(self, _results, img, _savepath):
        for i in _results:
            x1, y1, x2, y2, score = int(i['x1']), int(i['y1']), int(i['x2']), int(i['y2']), int(i['score'])
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
            cv2.putText(img, str(score), (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)
            print("%dx%d=%d, score=%d" % (x2-x1, y2-y1, (x2-x1)*(y2-y1), score))
        cv2.imwrite(_savepath, img)

# if __name__ == "__main__":
#     imgdir = "/yolov3/yolov4/release/0803/1802185/Images"
#     outdir = 'output'
#     configPath = "names-data/yolov4-tiny-custom-predict.cfg"
#     weightPath = "backup/yolov4-tiny-custom_best.weights"
#     metaPath = "names-data/obj.data"
#     batch_size = 20

#     d = detect(configPath, weightPath, metaPath, batch_size)
#     time_start=time.time()
#     imgs = get_images(imgdir)

#     for imgpath in tqdm(imgs):
#         img = cv2.imread(imgpath)
#         slices = d.img_slice(img, size=608, padx=148, pady=128) # FOV 切成多个608x608图片， 默认认为输入尺寸是2448x2048
#         slicesresults = d.batchDetect(slices, img) # 多个切图里面预测细胞核
#         results = d.resultsConcat(slices, slicesresults) # 把预测结果还原到原FOV图
#         # results = d.simpleNMS(results, 0.83) # 通过nms合并预测结果，去掉重复的框, 0.83 是IOU
#         results = d.removeSmall(results) # 删除细胞核太小，以及得分不高的
#         if len(results) > 0:
#             filepath, shotname, extension = get_filePath_fileName_fileExt(imgpath)
#             savepath = os.path.join(outdir, shotname + extension)
#             # d.drawRectangle(results, img, savepath)

#     time_end=time.time()
#     print('totally cost:',time_end-time_start)
