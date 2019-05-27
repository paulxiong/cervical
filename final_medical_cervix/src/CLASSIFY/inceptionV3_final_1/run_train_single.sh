#!/bin/bash
CLF_MODE=MultiClass
#CLF_MODE=Binary
#COLOR_MODE="HSV&CLAHE"
COLOR_MODE="RGB"
#COLOR_MODE="LAB_CLAHE_L"
PADDING_METHOD='Warp'
HEIGHT=75
WEIGHT=75
INPUT_FORM='FOLDER'


#PADDING_METHOD=Double_ZoomOut_Padding
#COLOR_MODE="HIST_BATCH_EQ_LAB"
#CUDA_0=7
#CUDA_1=6
#CUDA_2=5
#CUDA_3=4
CUDA_0=0

Dropout=0.5

if [ -n "$1" ]; then
    CLF_MODE=$1
fi

if [ -n "$2" ]; then
    echo $CUDA_0
    CUDA_0=$2
fi
echo $CUDA_0

nohup python3 final_train.py \
 --resize_method $PADDING_METHOD \
 --augment RandomRotate \
 --split_method CellBased\
 --dropout $Dropout \
 --clf_mode $CLF_MODE \
 --kfold 0 \
 --color_mode $COLOR_MODE \
 --cuda_device "$CUDA_0" \
 --input_shape $HEIGHT $WEIGHT \
 --input_form $INPUT_FORM \
 1>trainSingle${CLF_MODE}_$CUDA_0.log 2>&1 &
