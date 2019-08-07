#!/bin/bash
if [ ! -d datasets/segment/ ]; then
    mkdir -p datasets/segment/
fi

if [ ! -d segmentation/src/SEGMENT/kaggle-dsb2018/src/all_output/ ]; then
    echo "not found segmentation/src/SEGMENT/kaggle-dsb2018/src/all_output/*.h5 !!!"
    mkdir -p segmentation/src/SEGMENT/kaggle-dsb2018/src/all_output/
    exit
fi

docker build -f Dockerfile -t cervical:crop_20190807 ..
