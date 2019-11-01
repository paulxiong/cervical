#!/usr/bin/env python
# coding: utf-8
import os
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
from sklearn.metrics import classification_report

NUM_EPOCHS = 20
INIT_LR = 1e-1
BS = 32

#totalTest_cross_domain = len(list(paths.list_images(config.TEST_PATH_CROSS_DOMAIN)))
totalTest_cross_domain=2
print("  totalTest_cross_domain="+str(totalTest_cross_domain))

# initialize the testing generator for cross domain
valAug = ImageDataGenerator(rescale=1 / 255.0)
testGen_cross_domain = valAug.flow_from_directory(
        "./testing_cross_domain",
	class_mode="categorical",
	target_size=(64, 64),
	color_mode="rgb",
	shuffle=False,
	batch_size=BS)


model=load_model("mala.h5")


# reset the testGen_cross_domain generator and then use our trained model to
# make predictions on the data
print("[INFO] evaluating network ...(testGen_cross_domain)")
testGen_cross_domain.reset()
predIdxs = model.predict_generator(testGen_cross_domain,
	steps=(totalTest_cross_domain // BS+1),verbose=1)


# for each image in the testing set we need to find the index of the
# label with corresponding largest predicted probability
predIdxs = np.argmax(predIdxs, axis=1)



# show a nicely formatted classification report
print(classification_report(testGen_cross_domain.classes, predIdxs,
	target_names=testGen_cross_domain.class_indices.keys()))

