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
def load_imgs_as_nparray(imgdir, x, y, size=100):
    if len(y) != len(y):
        print("len(x) != len(y)")
        return None, None
    xnp, ynp = None, None
    for i in range(0, len(x)):
        image = imread(os.path.join(imgdir, x[i]))
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
# 返回图片名称的一个数组
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
            image_list.append(i)
    if allfiles_num > len(image_list):
        print(">>> %d files/folder ignored !!" % (allfiles_num - len(image_list)))
    return image_list

# 解析文件名字，返回fov和cell的类型
def get_info_by_cell_name(filename):
    cell_type, fov_type, original_img_name = None, None, None

    if filename is None or len(filename) < 2:
        return fov_type, cell_type, original_img_name
    arr = filename.split('_')
    if len(arr) < 7:
        print("invalied filename: %s" % filename)
        return fov_type, cell_type, original_img_name
    cell_type = arr[2]
    fov_type = arr[1]
    original_img_name = arr[0]
    return fov_type, cell_type, original_img_name

# 按照图片的名字的字段信息，把图片分类成字典
def get_images_type(imgs, cell1_fov0=1):
    dic = {} #fov的统计
    if imgs is None or len(imgs) < 1:
        return None
    for i in range(0, len(imgs)):
        filepath = imgs[i]
        #注意文件名字有严格规定
        fov_type, cell_type, _ = get_info_by_cell_name(filepath)

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
        fov_type, cell_type, _ = get_info_by_cell_name(filepath)
        if cell_type is None:
            continue
        x.append(filepath)
        y.append(cell_type)
    return x, y

# 找出目录里面所有的fov信息
# 返回的结果类似下面这个结构
#{
#  "IMG024x014.JPG": {
#    "1": ["IMG024x014.JPG_n_1_16_1_100_100.png"],
#    "7": ["IMG024x014.JPG_n_7_11_1_100_100.png", "IMG024x014.JPG_n_7_10_1_100_100.png"]
#  },
#}
def _get_fov_datasets(imgs):
    dic = {}
    if imgs is None or len(imgs) < 1:
        return None
    for i in range(0, len(imgs)):
        filepath = imgs[i]
        _, filename = os.path.split(filepath)
        fov_type, cell_type, org_img_name = get_info_by_cell_name(filename)
        if cell_type is None:
            continue
        if org_img_name not in dic.keys():
            dic[org_img_name] = {}
        cells = dic[org_img_name]

        _tmp = []
        if  cell_type in cells.keys():
            _tmp = cells[cell_type]
        _tmp.append(filepath)
        cells[cell_type] = _tmp
        dic[org_img_name] = cells

    return dic

def get_fov_type(celltype):
    p1n0 = 'p'
    n_type = ['1', '5', '12', '13', '14', '15']
    p_type = ['2', '3', '4', '6', '7', '8', '9', '10', '11']
    if celltype in n_type:
        p1n0 = 'n'
    elif celltype in p_type:
        p1n0 = 'p'
    else:
        raise RuntimeError('unkonw cell type %s' % celltype)
    return p1n0

# 把图片按照N/P的fov来组织
# 返回
def _get_fov_positive_negative(imgs):
    nx, ny, px, py = [], [], [], []
    if imgs is None or len(imgs) < 1:
        return nx, ny, px, py
    fov_dic = _get_fov_datasets(imgs)
    if fov_dic is None:
        return nx, ny, px, py

    print("number of fov: %d" % len(fov_dic.keys()))
    #遍历有那些fov图
    for i in fov_dic.keys():
        fov = fov_dic[i]
        print("├── %s: %d types" % (i, len(fov.keys())))
        #遍历某个foiv图里面有哪些细胞分类
        for j in fov.keys():
            cells = fov[j]
            fov_type = get_fov_type(j)
            print("│   ├── fov type: %s cells type: %s cells number: %d" % (j, fov_type, len(cells)))
            if fov_type == 'n':
                nx.append({'original_img_name': i, 'cells': cells})
                ny.append(fov_type)
            elif fov_type == 'p':
                px.append({'original_img_name': i, 'cells': cells})
                py.append(fov_type)
        print("│")
    return nx, ny, px, py

#把fov的n或者p图片load成npy到内存
def _load_fov_as_nparray(imgdir, x, y, size=32):
    n_xnp, n_ynp = [], []
    for i in range(0, len(x)):
        cells = x[i]['cells']
        label = y[i]
        _n_xnp, _n_ynp = None, None
        for i in range(0, len(cells)):
            image = imread(os.path.join(imgdir, cells[i]))
            if image.shape[0] != image.shape[1]:
                print('skip ' + cells[i])
                continue
            if image.shape[0] != size or image.shape[1] != size:
                resize_image = imresize(image, [size, size], interp='nearest')
                image = resize_image
            n_arr_x = np.array([image])
            if _n_xnp is not None:
                _n_xnp = np.append(_n_xnp, n_arr_x, axis=0)
            else:
                _n_xnp = n_arr_x
        n_xnp.append(_n_xnp)
        n_ynp.append([label])
    return n_xnp, n_ynp

def load_fov_as_nparray(imgdir, imgs, size=32, test_size=0.2):
    if not os.path.exists(imgdir) or not os.path.isdir(imgdir):
        raise RuntimeError('not found folder: %s' % rootpath)
    nx, ny, px, py = _get_fov_positive_negative(imgs)
    print(len(nx))

    nX_train, nX_test, ny_train, ny_test = \
        train_test_split(nx, ny, test_size=test_size, random_state=int(time.time()))
    pX_train, pX_test, py_train, py_test = \
        train_test_split(px, py, test_size=test_size, random_state=int(time.time()))

    nX_train_np, ny_train_np = _load_fov_as_nparray(imgdir, nX_train, ny_train, size=32)
    pX_train_np, py_train_np = _load_fov_as_nparray(imgdir, pX_train, py_train, size=32)
    nX_test_np, ny_test_np = _load_fov_as_nparray(imgdir, nX_test, ny_test, size=32)
    pX_test_np, py_test_np = _load_fov_as_nparray(imgdir, pX_test, py_test, size=32)

    return nX_train_np, ny_train_np, nX_test_np, ny_test_np, \
           pX_train_np, py_train_np, pX_test_np, py_test_np
