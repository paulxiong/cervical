# -*- coding: utf-8 -*-
import os, time
import numpy as np
from sklearn.model_selection import train_test_split
from scipy.misc import imsave, imread, imresize

# 找出目录里面所有的图片
# y表示label是文件夹名字, 一维数组
# x是图片的路径，一维数组
# min_num 每个分类最少要求有多少个分类
def get_all_datasets(rootpath, min_num=100):
    x, y = [], []
    for i in os.listdir(rootpath):
        path1 = os.path.join(rootpath, i)
        if not os.path.isdir(path1):
            continue
        if len(os.listdir(path1)) < min_num:
            raise RuntimeError('at least %d images each flod, but %s has %d'
				% (min_num, path1, len(os.listdir(path1))))
        for j in os.listdir(path1):
            path2 = os.path.join(path1, j)
            if os.path.isdir(path2):
                continue
            ext = os.path.splitext(path2)[1]
            ext = ext.lower()
            if not ext in ['.jpg', '.png', '.jpeg', '.bmp']:
                print(path2)
            else:
                x.append(path2)
                y.append(i)
    return x, y

# 统计数据集的信息,调试使用, 返回x为key的字典
def get_datasets_info(x, y):
    if len(y) != len(y):
        print("len(x) != len(y)")
        return None
    dic = {}
    for i in range(0, len(y)):
        _tmp = []
        key = y[i]
        if key in dic.keys():
            _tmp = dic[key]
        _tmp.append(x[i])
        dic[key] = _tmp
    #打印统计个数
    for key in dic:
        print("%s  %s" % (key, len(dic[key])))
    return dic

# 把数据集按照训练和测试分开
def split_datasets_train_test(all_x, all_y, test_size=0.2):
    if len(all_y) != len(all_y):
        print("len(x) != len(y)")
        return None, None, None, None
    X_train, X_test, y_train, y_test = \
        train_test_split(all_x, all_y, test_size=test_size, random_state=int(time.time()))
    return X_train, X_test, y_train, y_test

# 传入x是图片路径的数组，y是对应图片的label
# 把x对应图片load之后转成np.array, y也转成np.array
# 如果图片不是size宽 size长的，转换成sizexsize的
def load_imgs_as_nparray(x, y, size=100):
    if len(y) != len(y):
        print("len(x) != len(y)")
        return None, None
    xnp, ynp = None, None
    for i in range(0, len(x)):
        image = imread(x[i])
        if image.shape[0] != image.shape[1]:
            print('skip ' + x[i])
            continue
        if image.shape[0] != size or image.shape[1] != size:
            resize_image = imresize(image, [size, size], interp='nearest')
            image = resize_image
        n_arr_x = np.array([image])
        n_arr_y = [int(y[i])]
        if xnp is not None:
            xnp = np.append(xnp, n_arr_x, axis=0)
            ynp = np.append(ynp, n_arr_y, axis=0)
        else:
            xnp = n_arr_x
            ynp = n_arr_y
    return xnp, ynp

# 找出目录里面所有的图片, 只查找rootpath这级目录
# 返回rootpath + 图片名称的一个数组
def get_image_lists(rootpath):
    if not os.path.exists(rootpath) or not os.path.isdir(rootpath):
        raise RuntimeError('not found folder: %s' % rootpath)
    image_list = []
    allfiles = os.listdir(rootpath)
    allfiles_num = len(allfiles)
    for i in allfiles:
        path1 = os.path.join(rootpath, i)
        if os.path.isdir(path1):
            print(">>> unexpected folder: %s, must be image." % path1)
            continue
        ext = os.path.splitext(path1)[1]
        ext = ext.lower()
        if not ext in ['.jpg', '.png', '.jpeg', '.bmp']:
            print(">>> unexpected file: %s, must be jpg/png/bmp" % path1)
        else:
            image_list.append(path1)
    if allfiles_num > len(image_list):
        print(">>> %d files/folder ignored !!" % (allfiles_num - len(image_list)))
    return image_list

# 解析文件名字，返回fov和cell的类型
def get_info_by_cell_name(filename):
    if filename is None or len(filename) < 2:
        return None, None
    arr = filename.split('_')
    if len(arr) < 7:
        print("invalied filename: %s" % filename)
        return None, None
    cell_type = arr[2]
    fov_type = arr[1]
    return fov_type, cell_type

# 按照图片的名字的字段信息，把图片分类成字典
def get_images_type(imgs, cell1_fov0=1):
    dic = {} #fov的统计
    if imgs is None or len(imgs) < 1:
        return None
    for i in range(0, len(imgs)):
        filepath = imgs[i]
        #注意文件名字有严格规定
        fov_type, cell_type = get_info_by_cell_name(filepath)

        _tmp = []
        if fov_type in dic.keys():
            _tmp = dic[fov_type]
        _tmp.append(filepath)
        dic[fov_type] = _tmp

    infoname = 'cell'
    if cell1_fov0 == 0:
        infoname = 'fov'
    #打印统计个数
    for key in dic:
        print("%s: %s  %s" % (infoname, key, len(dic[key])))
    return dic

# 找出目录里面所有的cell信息
# y表示label, 一维数组
# x是图片的路径，一维数组
# min_num 每个分类最少要求有多少个分类
def get_cell_datasets(imgs, min_num=10):
    x, y = [], []
    if imgs is None or len(imgs) < 1:
        return None
    for i in range(0, len(imgs)):
        filepath = imgs[i]
        fov_type, cell_type = get_info_by_cell_name(filepath)
        if cell_type is None:
            continue
        x.append(filepath)
        y.append(cell_type)
    return x, y
