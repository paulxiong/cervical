from ctypes import *
import math, cv2, time, os, random, json
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
    with open(savefile, 'w', encoding='utf-8') as file:
        file.write(json.dumps(info, indent=2, ensure_ascii=False))
    return

if __name__ == "__main__":
    testdir="/yolov3/1211_gray/invalid/"
    dir_or_files = os.listdir(testdir)
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

    net = load_net("names-data/yolov3-voc-predict.cfg".encode('utf-8'), "names-data/yolov3-voc_1300.weights.kernel_mid.gray".encode('utf-8'), 0)
    meta = load_meta("names-data/voc.data".encode('utf-8'))

    for k in range(len(imgs)):
        imgpath = imgs[k]
        t1 = int(time.time()*1000)
        r = detect(net, meta, imgpath.encode('utf-8'), thresh=0.2, hier_thresh=0.5, nms=0.45)
        t2 = int(time.time()*1000)
        #original_image = cv2.imread(imgpath)
        print("%d/%d %d  %d" %(k, len(imgs), len(r), t2 - t1))
        dic = {}

        for i in range(len(r)):
            classname = str(r[i][0])
            x1, y1 = int(r[i][2][0]-r[i][2][2]/2), int(r[i][2][1]-r[i][2][3]/2)
            x2, y2 = int(r[i][2][0]+r[i][2][2]/2), int(r[i][2][1]+r[i][2][3]/2)
            w, h = x2 - x1, y2 - y1
            score = round(r[i][1], 2)
            classname = str(r[i][0], encoding = "utf-8")

            key = str(i)
            dic[key] = {}
            dic[key]["x1"], dic[key]["y1"], dic[key]["x2"], dic[key]["y2"], \
            dic[key]["score"], dic[key]["w"], dic[key]["h"], dic[key]["class"] = \
            x1, y1, x2, y2, score, w, h, classname

            #cv2.rectangle(original_image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 1)
            #cv2.putText(original_image, str(score), (int(x1), int(y1)), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)
        #out_img = str(imgpath) + ".yolo.png"
        #cv2.imwrite(out_img, original_image)
        save_json(dic, imgpath + ".json")
