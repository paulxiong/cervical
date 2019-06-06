#!/bin/bash

CLF_MODE=MultiClass
#CLF_MODE=Binary
#COLOR_MODE="HSV&CLAHE"
COLOR_MODE="RGB"
#COLOR_MODE="LAB_CLAHE_L"
PADDING_METHOD='Warp'
HEIGHT=128
WIDTH=128
#PADDING_METHOD='Double_ZoomOut_Padding'
#HEIGHT=299
#WIDTH=299
#INPUT_FORM='FOLDER'
INPUT_FORM='FOLDER'
LOSS_WEIGHTS="--loss_weight 0.25 3 3 3 3"
SPLIT_METHOD='CellBased'
#SPLIT_METHOD='CellBased'


#PADDING_METHOD=Double_ZoomOut_Padding
#COLOR_MODE="HIST_BATCH_EQ_LAB"
#CUDA_0=7
#CUDA_1=6
#CUDA_2=5
#CUDA_3=4
CUDA_0=1
CUDA_1=2
CUDA_2=4
CUDA_3=5
CUDA_4=6
CUDA_5=7

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
echo $CUDA_0 $CUDA_1

#rm -r ./test_datasets
#rm -r ./train_datasets

nohup python3 final_train_herlev.py \
 --resize_method $PADDING_METHOD \
 --augment Up_All  \
 --split_method $SPLIT_METHOD\
 --dropout $Dropout \
 --clf_mode $CLF_MODE \
 --color_mode $COLOR_MODE \
 --kfold 5 \
 --cuda_device "$CUDA_0" \
 --input_shape $HEIGHT $WIDTH \
 --input_form $INPUT_FORM \
 1>train${CLF_MODE}_$CUDA_0.log 2>&1 & 
 

nohup python3 final_train_herlev.py \
 --resize_method $PADDING_METHOD \
 --augment Up_All  \
 --split_method $SPLIT_METHOD\
 --dropout $Dropout \
 --clf_mode $CLF_MODE \
 --color_mode $COLOR_MODE \
 --kfold 5 \
 --cuda_device "$CUDA_1" \
 --input_shape $HEIGHT $WIDTH \
 --input_form $INPUT_FORM \
 $LOSS_WEIGHTS \
 1>train${CLF_MODE}_$CUDA_1.log 2>&1 & 
