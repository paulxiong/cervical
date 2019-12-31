#!/usr/bin/env python
# coding: utf-8
import os
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
from sklearn.metrics import classification_report
import time
import shutil

NUM_EPOCHS = 20
INIT_LR = 1e-1
predict_root = "./testing_cross_domain"
file_temp = os.listdir(predict_root)
BS = 32
totalTest_cross_domain=0
for i in file_temp:
    totalTest_cross_domain = totalTest_cross_domain + len(os.listdir(os.path.join(predict_root,i)))

#totalTest_cross_domain = len(list(paths.list_images(config.TEST_PATH_CROSS_DOMAIN)))
# totalTest_cross_domain=2
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
# model=load_model("yfq_model_classes_3.h5")
model=load_model("mala12-30-2019.h5")
# model=load_model("mala.h5")
# 保存模型结构图
# plot_model(model, to_file='model1.png',show_shapes=True)
# reset the testGen_cross_domain generator and then use our trained model to
# make predictions on the data
print("[INFO] evaluating network ...(testGen_cross_domain)")
testGen_cross_domain.reset()
t11 = time.time()

# model.fit_generator(testGen_cross_domain,steps_per_epoch=10, epochs=100,max_queue_size=1,workers=1)
# model.save('./yfq_model.h5')
predIdxs = model.predict_generator(testGen_cross_domain,
	steps=(totalTest_cross_domain // BS+1),verbose=1)
t22 = time.time() - t11
classes = list(np.argmax(predIdxs, axis=1))
classes_scores = []
for i in range(len(predIdxs)):
    classes_scores.append(max(predIdxs[i]))
filenames = testGen_cross_domain.filenames
# 根据细胞所在文件夹定义真正标签
labels_trues = []
cnt_N = 0
cnt_P = 0
for file in filenames:
    if file.split('/')[0][-1] == 'P':
        labels_trues.append(0)
    elif file.split('/')[0][-1] == 'N':
        labels_trues.append(1)
for filename,labels_true,classe,classes_score in zip(filenames, labels_trues, classes, classes_scores):
    if classe == 1:
        cnt_P = cnt_P + 1
    else:
        cnt_N = cnt_N + 1
    filename = os.path.join(predict_root, filename)
    new_name_ = filename.split('/')[3]

    if classe == 1:
        new_name = os.path.join('bad', new_name_+str(classes_score)[0:5]+'.png')
        shutil.copy(filename, new_name)
    elif classe == 0:
        new_name = os.path.join('good', new_name_+str(classes_score)[0:5]+'.png')
        shutil.copy(filename, new_name)
    print ('图片:{0}-真正标签:{1}-预测标签:{2}-得分:{3:.4}'.format(filename,labels_true,classe,classes_score))

# for each image in the testing set we need to find the index of the
# label with corresponding largest predicted probability
predIdxs = np.argmax(predIdxs, axis=1)

# show a nicely formatted classification report
# print('\n',classification_report(labels_trues, predIdxs,
# 	target_names=testGen_cross_domain.class_indices.keys()))
# print('time cost',t22)
print('规定：阳性标签为‘1’；阴性标签为‘0’')
print('预测为阳性细胞数量',cnt_P)
print('预测为阴性细胞数量',cnt_N)
