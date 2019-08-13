#!/bin/bash
if [ ! -d datasets/segment/ ]; then
    mkdir -p datasets/segment/
fi

if [ ! -d src/SEGMENT/kaggle-dsb2018/src/all_output/ ]; then
    echo "not found segmentation/src/SEGMENT/kaggle-dsb2018/src/all_output/*.h5 !!!"
    mkdir -p src/SEGMENT/kaggle-dsb2018/src/all_output/
    exit
fi

if [ -d datasets/segment/stage1_train/ ] || [ -d datasets/segment/stage1_test/ ]; then
    echo "please remove datasets/segment/stage1_train/ and datasets/segment/stage1_test/ !!!"
    exit
fi

timestamp=$(date "+%Y%m%d%-H%-M%-S")

docker build -f Dockerfile -t cervical:crop_${timestamp} ..
