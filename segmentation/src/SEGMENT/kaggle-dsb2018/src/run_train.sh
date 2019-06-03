#!/bin/bash
CUDA=3


function train()
{
    #public: train on Science bowl dataset
    #here we trin for 20 epochs for the colour model 
    #according to the README, they train the colour model 
    #twice, each 10 epochs
    #private: train on private data set for 10 epochs

    if [ -n "$1" ]; then
        case "$1" in
            c1) C_FLAG=--noise; C_VALUE=0.1;;
            c2) C_FLAG=--transform; C_VALUE=0.175;;
            c3) C_FLAG=;C_VALUE=;;
            *) echo ${show_usage}; exit 0;;
        esac
    fi
    
    
    if [ -n "$2" ]; then
        case "$2" in
            pub_1st) TRAIN_PATH_FLAG=;\
                    TRAIN_PATH=; \
                    COLOR_MODE=--colouronly; \
                    EPOCH=10; \
                    OUTPUT=./${1}_output; \
                    MODEL_FLAG=; \
                    MODEL=;;
            pub_2nd) TRAIN_PATH_FLAG=; \
                    TRAIN_PATH=; \
                    COLOR_MODE=; \
                    EPOCH=10; \
                    OUTPUT=./${1}_output; \
                    MODEL_FLAG=--loadmodel; \
                    MODEL=./${1}_output;;
            private) TRAIN_PATH_FLAG=--trainpath; \
                     TRAIN_PATH=../../../../datasets/segment/private_train; \
                     COLOR_MODE=--colouronly; \
                     EPOCH=10; \
                     OUTPUT=./${1}_output; \
                     MODEL_FLAG=--loadmodel; \
                     MODEL=./${1}_output ;;
        esac
    fi
    echo $1
    echo $2
    
    echo "train path flag:" "$TRAIN_PATH_FLAG"
    echo "train path:" "$TRAIN_PATH"
    echo "epcho:" "$EPOCH"
    echo "model path:" "$MODEL"
    echo "model flag:" "$MODEL_FLAG"
    echo "c flag:" "$C_FLAG"
    echo "c value:" "$C_VALUE"
    echo "output path:" "$OUTPUT"
    
    python3 schwaebische_nuclei.py train \
       	--maxtrainsize 300000 \
       	--testpath ../../../../datasets/segment/stage1_test \
       	--mosaic \
       	--rotate \
       	--epoch "$EPOCH" \
       	--valsplit 0 \
	    --output $OUTPUT \
	    --cuda_device $CUDA \
	    $TRAIN_PATH_FLAG $TRAIN_PATH $MODEL_FLAG $MODEL $C_FLAG $C_VALUE $COLOR_MODE
}

set -e
show_usage='Usage: ./run_train {c1/c2/c3} [private/public]'


echo "$1"
echo "$2"
if [ -n $1 ]; then
    if [ -n "$2" ]; then
        train ${1} $2
    else
        train ${1} pub_1st
        train ${1} pub_2nd
        train ${1} private
    fi
else
    echo $show_usage
fi


