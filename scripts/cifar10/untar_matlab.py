import os
import numpy as np
import scipy.io
import PIL.Image as Image

outputroot = "cifar10_untar"
outputdir = os.path.join(outputroot, "output")
test_outputdir = os.path.join(outputroot, "output_test")
inputdir="cifar-10-batches-mat"
batches_meta = os.path.join(inputdir, "batches.meta.mat")
test_batch = os.path.join(inputdir, "test_batch.mat")

def load_cifar10_batch(batch_data_path, batch_index, classnames, _outputdir):
    if not os.path.exists(batch_data_path):
        print("not found %s !!" % batch_data_path)
        return
    print("untar %s ..." % batch_data_path)
    data_dict = scipy.io.loadmat(batch_data_path)
    data = data_dict['data']
    labels = data_dict['labels'].flatten()

    #创建batch文件夹
    batch_dir = os.path.join(_outputdir, str(batch_index))
    if not os.path.exists(batch_dir):
        os.makedirs(batch_dir)

    airplane_cnt, bird_cnt = 0, 0
    for i in range(0, data.shape[0]):
        label = labels[i]
        label = classnames[int(label)]
        if label != "airplane" and label != "bird":
            continue
        if label == "airplane":
            if airplane_cnt >= 100:
                continue
            airplane_cnt = airplane_cnt + 1
        if label == "bird":
            if bird_cnt >= 100:
                continue
            bird_cnt = bird_cnt + 1
        #创建label文件夹
        label_dir = os.path.join(batch_dir, str(label))
        if not os.path.exists(label_dir):
            os.makedirs(label_dir)

        img1 = data[i]
        a = img1.reshape(3, 32, 32)

        # 得到RGB通道
        r = Image.fromarray(a[0]).convert('L')
        g = Image.fromarray(a[1]).convert('L')
        b = Image.fromarray(a[2]).convert('L')
        image = Image.merge("RGB", (r, g, b))

        # 显示图片
        img_path = os.path.join(label_dir, ("%05d.png") % (i))
        image.save(img_path, 'png')
    return

#加载分类名字与数字的对应关系
def load_cifar10_classname(classname_path):
    dic = {}
    if not os.path.exists(classname_path):
        print("not found %s !!" % classname_path)
        return
    data_dict = scipy.io.loadmat(classname_path)
    data_dict = data_dict['label_names'].flatten()
    for i in range(0, data_dict.shape[0]):
        dic[i] = data_dict[i][0]
    return dic


if __name__ == '__main__':
    dic = load_cifar10_classname(batches_meta)
    print(dic)
    for i in range(1, 6):
        batch_data = ("data_batch_%d.mat") % (i)
        batch_data = os.path.join(inputdir, batch_data)
        load_cifar10_batch(batch_data, i, dic, outputdir)

    load_cifar10_batch(test_batch, 0, dic, test_outputdir)
