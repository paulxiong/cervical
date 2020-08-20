from cv2 import cv2
import os, torch, time
import numpy as np
from utils.datasets import LoadImages
from models.experimental import attempt_load
from utils.datasets import letterbox
from utils.general import check_img_size, non_max_suppression, scale_coords, plot_one_box
from utils.torch_utils import select_device

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
    def __init__(self, weights_path, device='', img_size=640, conf_thres=0.4, iou_thres=0.5, augment=False, agnostic_nms=False, classes=None):
        self.device = select_device(device)
        self.weights_name = os.path.split(weights_path)[-1]
        self.model = attempt_load(weights_path, map_location=self.device)
        self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names
        self.colors = [[np.random.randint(0, 255) for _ in range(3)] for _ in range(len(self.names))]
        self.imgsz = check_img_size(img_size, s=self.model.stride.max())
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.augment = augment
        self.agnostic_nms = agnostic_nms
        self.classes = classes
        self.half = self.device.type != 'cpu'
        if self.half:
            self.model.half()
        if self.device.type != 'cpu':
            self.burn()

    def __str__(self):
        out = ['Model: %s' % self.weights_name]
        out.append('Image size: %s' % self.imgsz)
        out.append('Confidence threshold: %s' % self.conf_thres)
        out.append('IoU threshold: %s' % self.iou_thres)
        out.append('Augment: %s' % self.augment)
        out.append('Agnostic nms: %s' % self.agnostic_nms)
        if self.classes != None:
            filter_classes = [self.names[each_class] for each_class in self.classes]
            out.append('Classes filter: %s' % filter_classes)
        out.append('Classes: %s' % self.names)
        return '\n'.join(out)

    def burn(self):
        img = torch.zeros((1, 3, self.imgsz, self.imgsz), device=self.device)  # init img
        _ = self.model(img.half() if self.half else img)  # run once

    def predict(self, img0, img=None, draw_bndbox=False, bndbox_format='min_max_list'):
        if img is None:
            img = self.send_whatever_to_device(img0)
        else:
            img = self.send_to_device(img)

        pred = self.model(img, augment=self.augment)[0]
        pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, classes=self.classes, agnostic=self.agnostic_nms)

        det = pred[0]

        if det is not None and len(det):
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()

        if draw_bndbox:
            for *xyxy, conf, cls in det:
                label = '%s %.2f' % (self.names[int(cls)], conf)
                plot_one_box(xyxy, img0, label=label, color=self.colors[int(cls)])

        if bndbox_format == 'min_max_list':
            min_max_list = self.min_max_list(det)
            return min_max_list

    def predict_batch(self, img0s, draw_bndbox=False, bndbox_format='min_max_list'):
        time_start=time.time()
        imgs = self.send_whatever_to_device(img0s)
        with torch.no_grad():
            # Run model
            inf_out, _ = self.model(imgs, augment=self.augment)  # inference and training outputs
            # Run NMS
            preds = non_max_suppression(inf_out, conf_thres=self.conf_thres, iou_thres=self.iou_thres)
        batch_output = []
        for pred in preds:
            if pred is None:
                batch_output.append({})
            else:
                batch_output.append(self.min_max_list(pred))
        results = {}
        for i in range(len(img0s)):
            results[str(i)] = []
            for obj in batch_output[i]:
                label, score = obj['name'], obj["conf"]
                x1, y1, x2, y2 = int(obj['bndbox']['xmin']), int(obj['bndbox']['ymin']), int(obj['bndbox']['xmax']), int(obj['bndbox']['ymax'])
                results[str(i)].append({'label': label, 'labelid': -1, 'score': round(score, 2), 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2})
        time_end=time.time()
        print('totally cost:',time_end-time_start)
        return results

    def send_to_device(self, img_to_send):
        img_to_send = torch.from_numpy(img_to_send).to(self.device)
        img_to_send = img_to_send.half() if self.half else img_to_send.float()
        img_to_send /= 255.0 # 0 - 255 to 0.0 - 1.0
        if img_to_send.ndimension() == 3:
            img_to_send = img_to_send.unsqueeze(0)
        return img_to_send

    def reshape_copy_img(self, img):
        _img = letterbox(img, new_shape=self.imgsz)[0]
        _img = _img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB
        _img = np.ascontiguousarray(_img.copy())  # uint8 to float32
        return _img

    def send_whatever_to_device(self, img_s):
        if isinstance(img_s, list):
            img_to_send = []
            for img in img_s:
                img_to_send.append(self.reshape_copy_img(img))
            img_to_send = np.array(img_to_send)
        elif isinstance(img_s, np.ndarray):
            img_to_send = self.reshape_copy_img(img_s)
        else:
            print(type(img_s), ' is not supported')
            raise
        img_to_send = self.send_to_device(img_to_send)
        return img_to_send

    def min_max_list(self, det):
        min_max_list = []
        for i, c in enumerate(det[:, -1]):
            obj = {
                'bndbox': {
                    'xmin': min(int(det[i][0]),int(det[i][2])),
                    'xmax': max(int(det[i][0]),int(det[i][2])),
                    'ymin': min(int(det[i][1]),int(det[i][3])),
                    'ymax': max(int(det[i][1]),int(det[i][3]))
                    },
                'name': self.names[int(c)],
                'conf': float(det[i][4]),
                'color': self.colors[int(det[i][5])]
                }
            min_max_list.append(obj)
        return min_max_list

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

    def img_slicing(self, slices, _img):
        image_list = []
        for i in range(len(slices.keys())):         #按照上面计算得到的坐标切割
            item = slices[str(i)]
            x1, y1, x2, y2 = item['x1'], item['y1'], item['x2'], item['y2']
            image_list.append(_img[y1:y2, x1:x2])
        return image_list

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

# if __name__ == '__main__':
#     imgdir = "x"
#     outdir = "output"
#     weights_path = 'weights/yolov5m.pt'

#     y = detect(weights_path=weights_path)
#     imglists = get_images(imgdir)
#     for imgpath in imglists:
#         img = cv2.imread(imgpath)
#         slices = y.img_slice(img, size=608, padx=148, pady=128) # FOV 切成多个608x608图片， 默认认为输入尺寸是2448x2048
#         imgslices = y.img_slicing(slices, img)
#         slicesresults = y.predict_batch(imgslices)
#         results = y.resultsConcat(slices, slicesresults) # 把预测结果还原到原FOV图
#         results = y.removeSmall(results) # 删除细胞核太小，以及得分不高的
#         if len(results) > 0:
#             filepath, shotname, extension = get_filePath_fileName_fileExt(imgpath)
#             savepath = os.path.join(outdir, shotname + extension)
#             y.drawRectangle(results, img, savepath)