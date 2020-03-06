from PIL import Image
import numpy as np
import os, pickle

def img21Dnumpy(imgpath):
    img = Image.open(imgpath,"r")
    w, h = img.size[0], img.size[1]
    if w != h:
        print("w!=h, skip !")
        return None
    img = img.resize((32, 32), Image.BILINEAR)
    r, g, b = img.split()
    r1, g1, b1 = np.asarray(r), np.asarray(g), np.asarray(b)
    r2, g2, b2 = r1.flatten(), g1.flatten(), b1.flatten()
    data = np.concatenate((r2, g2, b2))
    return data

def get_train_test(inputdir):
    x_train = None
    y_train = []
    imgpathlists = []
    labels = os.listdir(inputdir)
    for label in labels:
        path1 = os.path.join(inputdir, label)
        for imgname in os.listdir(path1):
            imgpath = os.path.join(path1, imgname)
            imgnpy = img21Dnumpy(imgpath)
            if imgnpy is None:
                continue
            y_train.append(imgname)
            imgpathlists.append(imgname)
            if x_train is None:
                x_train = np.array([img21Dnumpy(imgpath)])
            else:
                x_train = np.concatenate((x_train, [img21Dnumpy(imgpath)]))
    return x_train, y_train, imgpathlists

#生成data_batch文件
def make_data_batch(x, y, filenames):
    dic = {}
    dic['batch_label'] = "training batch 1 of 5"
    dic['labels'] = y
    dic['data'] = x
    dic['filenames'] = filenames
    #print(dic)
    with open('my_data_batch', 'wb') as f:
        pickle.dump(dic, f)

x, y, filenames = get_train_test("input")
make_data_batch(x, y, filenames)
