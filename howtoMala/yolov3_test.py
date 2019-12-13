from ctypes import *
import math, cv2, time, os, random, json
from yolov3.predict import yolo_init, detect, _filter2, _filter3

if __name__ == "__main__":
    testdir="yolov3/img/"
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

    cfg, metadata = "yolov3/yolov3-voc-predict.cfg", "yolov3/voc.data"
    weights = "yolov3/yolov3-voc.backup"
    net, meta = yolo_init(cfg, weights, metadata)

    for k in range(len(imgs)):
        imgpath = imgs[k]
        t1 = int(time.time()*1000)
        r = detect(net, meta, imgpath.encode('utf-8'), thresh=0.5, hier_thresh=0.5, nms=0.45)
        t2 = int(time.time()*1000)
        #original_image = cv2.imread(imgpath)
        #print("%d/%d %d  %d" %(k, len(imgs), len(r), t2 - t1))
        dic = {"boxes": []}

        for i in range(len(r)):
            classname = str(r[i][0])
            x1, y1 = int(r[i][2][0]-r[i][2][2]/2), int(r[i][2][1]-r[i][2][3]/2)
            x2, y2 = int(r[i][2][0]+r[i][2][2]/2), int(r[i][2][1]+r[i][2][3]/2)
            w, h, score, classname = x2 - x1, y2 - y1, round(r[i][1], 2), str(r[i][0], encoding = "utf-8")
            dic["boxes"].append({"class": classname, "score": score, "w": w, "h": h, "x1": x1, "y1": y1, "x2": x2, "y2": y2})

        #去重　
        dic["boxes"] = _filter3(dic["boxes"])
        invalid = _filter2(dic["boxes"])
        if invalid is True:
            print(imgpath)

            #cv2.rectangle(original_image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 1)
            #cv2.putText(original_image, str(score), (int(x1), int(y1)), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)
        #out_img = str(imgpath) + ".yolo.png"
        #cv2.imwrite(out_img, original_image)
