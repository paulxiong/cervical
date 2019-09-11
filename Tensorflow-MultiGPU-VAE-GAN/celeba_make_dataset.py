# coding: utf-8
from glob import glob
import numpy as np
import scipy.misc
import matplotlib.pyplot as plt
import os
import pandas as pd
import h5py
import tqdm
import cv2

#resize images
def resize_img(input_dir, output_dir, RESIZE):
    img_file = os.listdir(input_dir)
    for img_name in img_file:
        print (os.path.join(input_dir, img_name))
        img = cv2.imread(os.path.join(input_dir, img_name))
        print(img.shape)
        if img.shape[0] != img.shape[1]:
            print("skip this image w != h: %s" % img_name)
            continue
        img = cv2.resize(img,(RESIZE,RESIZE),interpolation=cv2.INTER_LINEAR)
        if os.path.exists(os.path.join(output_dir)):
            cv2.imwrite(os.path.join(output_dir, img_name),img)
        else:
            os.makedirs(os.path.join(output_dir))
            cv2.imwrite(os.path.join(output_dir, img_name), img)

resize_img("17P0603", "resize_17P0603", 64)
data = glob(os.path.join("resize_17P0603", "*.png"))
data = np.sort(data)
print(len(data))

def get_image(image_path, width=64, height=64):
    return scipy.misc.imread(image_path).astype(np.float)

dim = 64
images = np.zeros((len(data),dim*dim*3), dtype = np.uint8)

# make a dataset
for i in tqdm.tqdm(range(len(data))):
    #for i in tqdm.tqdm(range(10)):
    image = get_image(data[i], dim,dim)
    images[i] = image.flatten()
    # get the metadata

with h5py.File(''.join(['datasets/faces_dataset_new.h5']), 'w') as f:
    dset_face = f.create_dataset("images", data = images)