from PIL import Image
import numpy as np
import os, pickle
import scipy.io

inputdirroot = "cifar10_untar"
inputdir = os.path.join(inputdirroot, "output")
test_inputdir = os.path.join(inputdirroot, "output_test")
outputdir = "cifar10_tar"
batches_meta = os.path.join(outputdir, "batches.meta.mat")
test_batch = os.path.join(outputdir, "test_batch.mat")

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

def get_train_test(batchdir, _labels):
    x_train = None
    y_train = []
    labels = os.listdir(batchdir)
    for label in labels:
        path1 = os.path.join(batchdir, label)
        for imgname in os.listdir(path1):
            imgpath = os.path.join(path1, imgname)
            imgnpy = img21Dnumpy(imgpath)
            if imgnpy is None:
                continue
            if label not in _labels.keys():
                continue
            #字符串类别名字换成数字
            y_train.append(_labels[label])
            if x_train is None:
                x_train = np.array([img21Dnumpy(imgpath)])
            else:
                x_train = np.concatenate((x_train, [img21Dnumpy(imgpath)]))
    return x_train, y_train

#生成data_batch文件
def make_data_batch(_inputdir, _test_inputdir, _labels):
    if not os.path.exists(_inputdir):
        print("not found %s !!" % _inputdir)
        return

    _batches = os.listdir(_inputdir)
    for batch_index in range(1, len(_batches) + 1):
        path1 = os.path.join(_inputdir, str(batch_index))
        x, y = get_train_test(path1, _labels)

        data_dict = scipy.io.loadmat("data_batch_1.mat.empty.mat")
        data_dict['data'] = x
        data_dict['labels'] = y
        data_dict['batch_label'] = ("training batch %d of %d") % (batch_index + 1, len(_batches))
        batch_data_path = os.path.join(outputdir, ("data_batch_%d.mat") % (batch_index))
        scipy.io.savemat(batch_data_path, data_dict)

    _batches = os.listdir(_test_inputdir)
    for batch_index in range(1, len(_batches) + 1):
        path1 = os.path.join(_inputdir, str(batch_index))
        x, y = get_train_test(path1, _labels)

        data_dict = scipy.io.loadmat("test_batch.mat.empty.mat")
        data_dict['data'] = x
        data_dict['labels'] = y
        scipy.io.savemat(test_batch, data_dict)


def make_batches_meta(_inputdir):
    if not os.path.exists(_inputdir):
        print("not found %s !!" % _inputdir)
        return

    #遍历所有图片目录，找出所有类的名字
    label_names = []
    classnames = {}
    for batch_index in os.listdir(_inputdir):
        for classname in os.listdir(os.path.join(_inputdir, str(batch_index))):
            classnames[classname] = ""  #用字典的key避免冲突

    classnames = classnames.keys()
    classnames = sorted(classnames, key=str.lower)

    data_dict = scipy.io.loadmat("batches.meta.mat.empty")

    #batches.meta.mat.empty 是一个模板，里面有10个分类，我们自己的不到10个所以多余的要删除
    delete_row = {}
    for i in range(data_dict['label_names'].shape[0]):
        classname = data_dict['label_names'][i][0][0]
        delete_row[classname] = 1

    dic = {}
    for i in range(len(classnames)):
        classname = classnames[i]
        data_dict['label_names'][i][0][0] = classname
        #修改后名字长度要和dtype匹配
        data_dict['label_names'][i][0] = data_dict['label_names'][i][0].astype("<U%d" % len(classname))
        delete_row[classname] = 0
        dic[classname] = i

    for i in delete_row.keys():
        if delete_row[i] == 0:
            continue
        for j in range(data_dict['label_names'].shape[0]):
            if data_dict['label_names'][j][0][0] == delete_row[i]:
                data_dict['label_names'] = np.delete(data_dict['label_names'], j, axis = 0)

    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    scipy.io.savemat(batches_meta, data_dict)
    return dic

labels = make_batches_meta(inputdir)
print(labels)
make_data_batch(inputdir, test_inputdir, labels)
