# -*- coding: utf-8 -*-
import os
from sklearn.model_selection import KFold
import numpy as np
from segmentation_functions import *
from gan_model import *
from datasets import *
#from datasets2 import get_image_lists, get_images_type, get_cell_datasets
import multiprocessing
import time

def cell_segmentation(positive_images_root, negative_images_root, positive_npy_root, 
                      negative_npy_root, ref_path, intensity, multi_core):
    
    positive_images_path = [positive_images_root + n for n in os.listdir(positive_images_root)]
    negative_images_path = [negative_images_root + n for n in os.listdir(negative_images_root)]
    
    if 1- os.path.exists(positive_npy_root+str(intensity)+'/'):
        os.makedirs(positive_npy_root+str(intensity)+'/')
    if 1- os.path.exists(negative_npy_root+str(intensity)+'/'):
        os.makedirs(negative_npy_root+str(intensity)+'/')

    if (multi_core == True):
        jobs = []
        for index, i in enumerate(positive_images_path):
            p = multiprocessing.Process(target=cell_segment, args=(i, positive_npy_root+str(intensity)+'/',
                                                                  ref_path, intensity))
            p.start()
            jobs.append(p)
            if (index+1)%7 == 0:
                p.join()
                jobs = []

        for job in jobs:
            p.join()

        jobs = []
        for index, i in enumerate(negative_images_path):
            p = multiprocessing.Process(target=cell_segment, args=(i, negative_npy_root+str(intensity)+'/',
                                                                  ref_path, intensity))
            p.start()
            jobs.append(p)
            if (index+1)%7 == 0:
                p.join()
                jobs = []
            
        for job in jobs:
            p.join()
    else:
        for index, i in enumerate(positive_images_path):
            cell_segment(i, positive_npy_root+str(intensity)+'/',ref_path,intensity)
        for index, i in enumerate(negative_images_path):
            cell_segment(i, negative_npy_root+str(intensity)+'/',ref_path,intensity)

def split_dataset(path, fold=4, random_seed=42):
    np.random.seed(random_seed)
    kf = KFold(n_splits=fold, shuffle=True)
    kf.get_n_splits(path)
    train_list, test_list, train_label_list, test_label_list  = [], [], [], []
    for train_index, test_index in kf.split(path):
        train_list.append([path[n] for n in train_index])
        test_list.append([path[n] for n in test_index])
    return train_list, test_list

def cell_representation(X_train_path, X_test_path, y_train_path, y_test_path, experiment_root, 
                        n_epoch=50, batchsize=16, rand=32, dis=1, dis_category=5, 
                        ld = 1e-4, lg = 1e-4, lq = 1e-4, save_model_steps=100):

    X_train = np.load(X_train_path)
    X_test = np.load(X_test_path)
    y_train = np.load(y_train_path)
    y_test = np.load(y_test_path)

    cell_train_set = np.concatenate([X_train, X_test])
    cell_test_set = cell_train_set
    cell_test_label = np.concatenate([y_train, y_test])

    print('rand=', rand, 'dis_category=', dis_category, 'batchsize=', batchsize, 'dis=', dis)
    netD, netG, netD_D, netD_Q = create_model(rand=rand, dis_category=dis_category)
    train_representation(cell_train_set, cell_test_set, cell_test_label, netD, netG, netD_D, netD_Q,
                         experiment_root, n_epoch=n_epoch, batchsize=batchsize, rand=rand, dis=dis, 
                         dis_category=dis_category, ld=ld, lg=lg, lq=lq, save_model_steps=save_model_steps)

def cell_representation3(cell_datasets_path, experiment_root,
                        n_epoch=50, batchsize=16, rand=32, dis=1, dis_category=5,
                        ld = 1e-4, lg = 1e-4, lq = 1e-4, save_model_steps=100):

    image = get_image_lists(cell_datasets_path)
    # 获得所有图片的统计信息
    cell = get_images_type(image, 1)
    fov = get_images_type(image, 0)
    cell_type_num =  len(cell.keys())
    fov_type_num = len(fov.keys())
    print(cell_type_num, fov_type_num)

    dis_category = cell_type_num

    # 把cell数据按照train/evaluation分开
    x, y = get_cell_datasets(image)
    X_train, X_test, y_train, y_test = split_datasets_train_test(x, y, test_size=0.2)
    print(len(x), len(y))
    print(len(X_train), len(X_test), len(y_train), len(y_test))

    print(">>> loading datasets ...:")
    X_train, y_train = load_imgs_as_nparray(cell_datasets_path, X_train, y_train, rand)
    X_test, y_test = load_imgs_as_nparray(cell_datasets_path, X_test, y_test, rand)
    print(">>> loading datasets done:")

    cell_train_set = np.concatenate([X_train, X_test])
    cell_test_set = cell_train_set
    cell_test_label = np.concatenate([y_train, y_test])

    print(cell_train_set.shape, cell_test_set.shape, cell_test_label.shape)

    print('rand=', rand, 'dis_category=', dis_category, 'batchsize=', batchsize, 'dis=', dis)
    netD, netG, netD_D, netD_Q = create_model(rand=rand, dis_category=dis_category)
    train_representation2(cell_train_set, cell_test_set, cell_test_label, netD, netG, netD_D, netD_Q,
                         experiment_root, n_epoch=n_epoch, batchsize=batchsize, rand=rand, dis=dis,
                         dis_category=dis_category, ld=ld, lg=lg, lq=lq, save_model_steps=save_model_steps)

def cell_representation2(cell_datasets_path, experiment_root,
                        n_epoch=50, batchsize=16, rand=32, dis=1, dis_category=5,
                        ld = 1e-4, lg = 1e-4, lq = 1e-4, save_model_steps=100):

    x, y = get_all_datasets(cell_datasets_path)
    X_train, X_test, y_train, y_test = split_datasets_train_test(x, y, test_size=0.2)
    print(">>> train with:")
    get_datasets_info(X_train, y_train)
    print(">>> evaluate with:")
    get_datasets_info(X_test, y_test)

    print(">>> loading datasets ...:")
    X_train, y_train = load_imgs_as_nparray(X_train, y_train, rand)
    X_test, y_test = load_imgs_as_nparray(X_test, y_test, rand)
    print(">>> loading datasets done:")

    cell_train_set = np.concatenate([X_train, X_test])
    cell_test_set = cell_train_set
    cell_test_label = np.concatenate([y_train, y_test])

    print(cell_train_set.shape, cell_test_set.shape, cell_test_label.shape)

    print('rand=', rand, 'dis_category=', dis_category, 'batchsize=', batchsize, 'dis=', dis)
    netD, netG, netD_D, netD_Q = create_model(rand=rand, dis_category=dis_category)
    train_representation2(cell_train_set, cell_test_set, cell_test_label, netD, netG, netD_D, netD_Q,
                         experiment_root, n_epoch=n_epoch, batchsize=batchsize, rand=rand, dis=dis,
                         dis_category=dis_category, ld=ld, lg=lg, lq=lq, save_model_steps=save_model_steps)

def generator_fake_cell(experiment_root, batchsize=16, rand=32, dis=1, dis_category=5):
    x, y = get_all_datasets('experiment/data/cell_datasets/')
    print('rand=', rand, 'dis_category=', dis_category, 'batchsize=', batchsize, 'dis=', dis)
    netD, netG, netD_D, netD_Q = create_model(rand=rand, dis_category=dis_category)
    fake_cell(experiment_root, len(y), netD, netG, netD_D, netD_Q, batchsize=batchsize, rand=rand, dis=dis, dis_category=dis_category)

def predict_cell(experiment_root, X_test_path, y_test_path, batchsize=16, rand=32, dis=1, dis_category=5):
    X_test = np.load(X_test_path)
    y_test = np.load(y_test_path)

    cell_test_set = X_test
    cell_test_label = y_test

    netD, netG, netD_D, netD_Q = create_model(rand=rand, dis_category=dis_category)
    predict_cells(experiment_root, cell_test_set, cell_test_label, netD, netG, netD_D, netD_Q, batchsize=batchsize, rand=rand, dis=dis, dis_category=dis_category)

def image_classification(positive_images_root, negative_images_root, positive_npy_root,negative_npy_root, 
                      ref_path, intensity, X_train_path, X_test_path, y_train_path, y_test_path, experiment_root, multi_core = True,
                      fold = 4, random_seed=42, choosing_fold = 1, n_epoch=10000, batchsize=32, rand=64, dis=1, 
                         dis_category=5, ld = 1e-4, lg = 1e-4, lq = 1e-4, save_model_steps = 100):

    cell_segmentation(positive_images_root, negative_images_root, positive_npy_root, 
                      negative_npy_root, ref_path, intensity, multi_core)

    positive_npy_path = [positive_npy_root +str(intensity)+'/' + n[:-3] + 'npy' for n in os.listdir(positive_images_root)]
    negative_npy_path =[negative_npy_root +str(intensity)+'/' + n[:-3] + 'npy' for n in os.listdir(negative_images_root)]

    positive_train_list, positive_test_list = split_dataset(positive_npy_path, fold, random_seed)
    negative_train_list, negative_test_list = split_dataset(negative_npy_path, fold, random_seed)

    positive_train_npy = [np.load(n) for n in positive_train_list[choosing_fold]]
    positive_test_npy = [np.load(n) for n in positive_test_list[choosing_fold]]
    negative_train_npy = [np.load(n) for n in negative_train_list[choosing_fold]]
    negative_test_npy = [np.load(n) for n in negative_test_list[choosing_fold]]

    cell_train_set = np.concatenate([np.concatenate(positive_train_npy), np.concatenate(negative_train_npy)])

    X_train = np.load(X_train_path)
    X_test = np.load(X_test_path)
    y_train = np.load(y_train_path)
    y_test = np.load(y_test_path)
    cell_test_set = np.concatenate([X_train, X_test])
    cell_test_label = np.concatenate([y_train, y_test])
    cell_train_set = np.concatenate([cell_train_set, rotation(cell_test_set)])

    netD, netG, netD_D, netD_Q = create_model(rand=rand, dis_category=dis_category)
    netD, netG, netD_D, netD_Q =  train(cell_train_set, cell_test_set, cell_test_label, 
                   positive_train_npy, positive_test_npy,negative_train_npy, negative_test_npy,
                   netD, netG, netD_D, netD_Q, experiment_root, 
                   n_epoch=n_epoch, batchsize=batchsize, rand=rand, dis=1, dis_category=dis_category, 
                   ld = ld, lg = lg, lq = lq, save_model_steps=save_model_steps)

def image_classification3(cell_datasets_path, experiment_root, fold = 4, random_seed = 42,
                          choosing_fold = 1, n_epoch=10000, batchsize=32, rand=64, dis=1,
                          dis_category=5, ld = 1e-4, lg = 1e-4, lq = 1e-4, save_model_steps = 100):
    print(">>> loading cell and fov datasets ...:")
    image = get_image_lists(cell_datasets_path)
    # 获得细胞有几个类型
    cell = get_images_type(image, 1)
    dis_category =  len(cell.keys())
    # 把cell数据按照train/evaluation分开
    x, y = get_cell_datasets(image)
    X_train, X_test, y_train, y_test = split_datasets_train_test(x, y, test_size=0.2)
    X_train, y_train = load_imgs_as_nparray(cell_datasets_path, X_train, y_train, rand)
    X_test, y_test = load_imgs_as_nparray(cell_datasets_path, X_test, y_test, rand)

    #吧fov加载到内存，按npy的方式组织
    negative_train_npy, negative_test_npy, positive_train_npy, positive_test_npy = \
        load_fov_as_nparray(cell_datasets_path, image)
    print(">>> loading datasets done:")

    cell_train_set = np.concatenate([np.concatenate(positive_train_npy), np.concatenate(negative_train_npy)])

    cell_test_set = np.concatenate([X_train, X_test])
    cell_test_label = np.concatenate([y_train, y_test])
    cell_train_set = np.concatenate([cell_train_set, rotation(cell_test_set)])

    netD, netG, netD_D, netD_Q = create_model(rand=rand, dis_category=dis_category)
    netD, netG, netD_D, netD_Q =  train(cell_train_set, cell_test_set, cell_test_label,
                   positive_train_npy, positive_test_npy,negative_train_npy, negative_test_npy,
                   netD, netG, netD_D, netD_Q, experiment_root,
                   n_epoch=n_epoch, batchsize=batchsize, rand=rand, dis=1, dis_category=dis_category,
                   ld = ld, lg = lg, lq = lq, save_model_steps=save_model_steps)
