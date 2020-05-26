#!/usr/bin/env python
# coding: utf-8
import os
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
from sklearn.metrics import classification_report
import time
import shutil
import tensorflow as tf
import keras.backend.tensorflow_backend as KTF


def main1(md90):
    NUM_EPOCHS = 20
    INIT_LR = 1e-1
    predict_root = "./cells_1400"
    file_temp = os.listdir(predict_root)
    BS = 100
    totalTest_cross_domain=0
    for i in file_temp:
        totalTest_cross_domain = totalTest_cross_domain + len(os.listdir(os.path.join(predict_root,i)))

    print("  totalTest_cross_domain="+str(totalTest_cross_domain))
    
    # initialize the testing generator for cross domain
    valAug = ImageDataGenerator(rescale=1 / 255.0)
    testGen_cross_domain = valAug.flow_from_directory(
            predict_root,
    	class_mode="categorical",
    	target_size=(64, 64),
    	color_mode="rgb",
    	shuffle=False,
    	batch_size=BS)
    model = md90
    print("[INFO] evaluating network ...(testGen_cross_domain)")
    testGen_cross_domain.reset()
    t11 = time.time()
    predIdxs = model.predict_generator(testGen_cross_domain,steps=(totalTest_cross_domain // BS+1),verbose=1)
    t22 = time.time() - t11
    classes = list(np.argmax(predIdxs, axis=1))
    classes_scores = []
    for i in range(len(predIdxs)):
        classes_scores.append(max(predIdxs[i]))
    filenames = testGen_cross_domain.filenames

    for filename,classe,classes_score in zip(filenames, classes, classes_scores):
        if classe == 1:
            #new_name = os.path.join('bad', new_name_)
            #shutil.copy(filename, new_name)
            pass
        elif classe == 0:
            new_name = os.path.join('cells_90_P', filename.split('/')[1])
            shutil.copy(os.path.join('cells_82',filename.split('/')[1]), new_name)

    predIdxs = np.argmax(predIdxs, axis=1)