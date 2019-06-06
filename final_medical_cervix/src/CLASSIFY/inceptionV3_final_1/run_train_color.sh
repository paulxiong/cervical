#!/bin/bash

CLF_MODE=MultiClass
#COLOR_MODE="HSV&CLAHE"
AUGMENT=RandomRotate
#COLOR_MODE="RGB"
CUDA_0=7
CUDA_1=6
CUDA_2=5
CUDA_3=4


Dropout=0.5

if [ -n "$1" ]; then
    CLF_MODE=$1
fi

if [ -n "$2" ]; then
    echo $CUDA_0
    CUDA_0=$2
fi

if [ -n "$3" ]; then
    CUDA_1=$3
fi

if [ -n "$4" ]; then
    CUDA_2=$4
fi

if [ -n "$5" ]; then
    CUDA_3=$5
fi
echo $CUDA_0 $CUDA_1 $CUDA_2 $CUDA_3

nohup python3 final_train.py \
 --resize_method Double_ZoomOut_Padding \
 --augment $AUGMENT \
 --split_method CellBased\
 --dropout $Dropout \
 --clf_mode $CLF_MODE \
 --kfold 5 \
 --color_mode HSV_CLAHE_V \
 --cuda_device "$CUDA_0" \
 1>train${CLF_MODE}_0.log 2>&1 &

nohup python3 final_train.py \
 --resize_method Double_ZoomOut_Padding \
 --augment $AUGMENT \
 --split_method CellBased\
 --dropout $Dropout \
 --clf_mode $CLF_MODE \
 --color_mode HSV_CLAHE_S \
 --kfold 5 \
 --cuda_device "$CUDA_1" \
 1>train${CLF_MODE}_1.log 2>&1 &

nohup python3 final_train.py \
 --resize_method Double_ZoomOut_Padding \
 --augment $AUGMENT \
 --split_method CellBased\
 --dropout $Dropout \
 --clf_mode $CLF_MODE \
 --color_mode HSV_CLAHE_SV \
 --kfold 5 \
 --cuda_device "$CUDA_2" \
1>train${CLF_MODE}_2.log 2>&1 & 


nohup python3 final_train.py \
 --resize_method Double_ZoomOut_Padding \
 --augment $AUGMENT \
 --split_method CellBased\
 --dropout $Dropout \
 --clf_mode $CLF_MODE \
 --color_mode LAB_CLAHE_L \
 --kfold 5 \
 --cuda_device "$CUDA_3" \
 1>train${CLF_MODE}_3.log 2>&1 & 
