from PIL import Image
import numpy as np
import os, pickle

inputdir="input"
outputdir="python_tar"

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

def get_train_test(inputdir, _dic):
    x_train = None
    y_train = []
    imgpathlists = []
    labels = os.listdir(inputdir)
    for label in labels:
        path1 = os.path.join(inputdir, label)
        for imgname in os.listdir(path1):
            imgpath = os.path.join(path1, imgname)
            imgnpy = img21Dnumpy(imgpath)
            if imgnpy is None or label not in _dic.keys():
                continue
            y_train.append(int(_dic[label]))
            imgpathlists.append(imgname)
            if x_train is None:
                x_train = np.array([img21Dnumpy(imgpath)])
            else:
                x_train = np.concatenate((x_train, [img21Dnumpy(imgpath)]))
    return x_train, y_train, imgpathlists

#生成data_batch文件
def make_data_batch(x, y, filenames, batch_index, savepath):
    _dic = {}
    _dic['batch_label'] = "training batch %d of 5" % batch_index
    _dic['labels'] = y
    _dic['data'] = x
    _dic['filenames'] = filenames
    with open(savepath, 'wb') as f:
        pickle.dump(_dic, f)

#查找分类和id的对应
def make_batches_meta(_inputdir, _batches_meta_path):
    _dic = {}
    for bid in os.listdir(_inputdir):
        path1 = os.path.join(_inputdir, str(bid))
        for classname in os.listdir(path1):
            if str(classname) not in _dic.keys():
                _dic[classname] = 0
    _labels = _dic.keys()
    _labels = sorted(_labels, key=str.lower)

    _dic = {}
    for i in range(len(_labels)):
        _dic[_labels[i]] = i

    dic2 = {'num_cases_per_batch': 10000, 'label_names': _labels, 'num_vis': 3072}
    with open(_batches_meta_path, 'wb') as f:
        pickle.dump(dic2, f)

    return _labels, _dic


if __name__ == "__main__":
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    #查找所有标签
    batches_meta_path = os.path.join(outputdir, "batches.meta")
    labels, dic = make_batches_meta(inputdir, batches_meta_path)
    print(labels)

    for i in range(1, 6):
        path1 = os.path.join(inputdir, str(i))
        x, y, filenames = get_train_test(path1, dic)
        savepath = os.path.join(outputdir, "data_batch_%d" % i)
        make_data_batch(x, y, filenames, i, savepath)

    path1 = os.path.join(inputdir, "test")
    x, y, filenames = get_train_test(path1, dic)
    savepath = os.path.join(outputdir, "test_batch")
    make_data_batch(x, y, filenames, 0, savepath)
