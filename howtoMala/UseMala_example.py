#!/usr/bin/env python
# coding: utf-8
import os
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
from sklearn.metrics import classification_report
from keras.utils.vis_utils import plot_model

NUM_EPOCHS = 20
INIT_LR = 1e-1
BS = 32 #BS值必须为被预测图片的数量
predict_root = "./testing_cross_domain"
file_temp = os.listdir(predict_root)
totalTest_cross_domain=0
for i in file_temp:
    totalTest_cross_domain = totalTest_cross_domain + len(os.listdir(os.path.join(predict_root,i)))

#totalTest_cross_domain = len(list(paths.list_images(config.TEST_PATH_CROSS_DOMAIN)))
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
model=load_model("mala.h5")
# 保存模型结构图
plot_model(model, to_file='model1.png',show_shapes=True)
# reset the testGen_cross_domain generator and then use our trained model to
# make predictions on the data
print("[INFO] evaluating network ...(testGen_cross_domain)")
testGen_cross_domain.reset()
predIdxs = model.predict_generator(testGen_cross_domain,
	steps=(totalTest_cross_domain // BS+1),verbose=1)

classes = list(np.argmax(predIdxs, axis=1))
filenames = testGen_cross_domain.filenames
# 根据细胞所在文件夹定义真正标签
labels_trues = []
for file in filenames:
    if file.split('/')[0][-1] == 'P':
        labels_trues.append(0)
    elif file.split('/')[0][-1] == 'N':
        labels_trues.append(1)
for filename,labels_true,classe in zip(filenames, labels_trues, classes):
   print ('图片:{0}-真正标签:{1}-预测标签:{2}'.format(filename,labels_true,classe))

# for each image in the testing set we need to find the index of the
# label with corresponding largest predicted probability
predIdxs = np.argmax(predIdxs, axis=1)

# show a nicely formatted classification report
print('\n',classification_report(labels_trues, predIdxs,
	target_names=testGen_cross_domain.class_indices.keys()))
