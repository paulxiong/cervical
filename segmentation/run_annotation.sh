#!/bin/bash
#ORIGIN_DIR='datasets/test_slide/*/'
ORIGIN_DIR=$2
ROOT=`pwd`
SEGMENT_DIR='datasets/segment/test/'
FILE_PATTERN='*.JPG'
CLF_DATASETS='datasets/classify'
MARK_DIR='marked_image'
THRESHOLD=0.5
CLF_INPUT_WIDTH=75
CLF_INPUT_HEIGHT=75
CLF_MODE=MultiClass
SEG_MODEL=all
#SEG_MODEL=c3
CUDA_DEVICE=1
DENOSING=--denoising
#DENOSING=
COLOR_MODE='RGB'
PADDING='Warp'
CROP_METHOD='Mask'
SQUARE_EDGE=50
#COLOR_MODE='LAB_CLAHE_L'
#COLOR_MODE='HIST_BATCH_EQ_LAB'
AREA_THRESH=100
#PVA_THRESH=
echo $3
if [ -n "$3" ];then
    TR_FLAG=--train_test_split
else
    TR_FLAG=
fi
RZM_THRESH=
INTNES_THRESH=
PVA_THRESH="--perimeter_vs_area 18"
#PVA_THRESH=
#RZM_THRESH="--zernike_thresh 3.7"
#INTNES_THRESH="--intensity_thresh 40"
ANNOT_DIR=${CLF_DATASETS}'/annot_out'
TRAINDATA_DIR=${CLF_DATASETS}'/train_datasets'
COPY_DIR=${CLF_DATASETS}'/data'


function run_step1()
{
    ##Step 1. Copy FOVs to segmentation dir
    python3 step1.py \
        --origindir "${ORIGIN_DIR}" \
        --segtestdir ${SEGMENT_DIR} \
        --filepattern ${FILE_PATTERN} \
#	--resize_ratio 1.5 \
#        $DENOSING
    echo "Step1 结束"
}

function run_step2()
{
    ##Step 2. Run Segmentation
    cd src/SEGMENT/kaggle-dsb2018/src/
    
    python3 schwaebische_nuclei_predict.py predict_test \
        --mosaic \
        --loadmodel ${SEG_MODEL}_output/ \
        --predicttestonly \
        --cuda_device $CUDA_DEVICE \
        --colouronly
    
    cd $ROOT
}

function run_step3()
{
    ##Step 3. Crop the FOVs into cells
    python3 step3.py \
        --origindir "${ORIGIN_DIR}" \
        --filepattern ${FILE_PATTERN}\
        --datasets ${CLF_DATASETS}\
        --segtestdir ${SEGMENT_DIR}\
        --crop_method ${CROP_METHOD} \
        --area_thresh ${AREA_THRESH} \
        --square_edge ${SQUARE_EDGE}\
        ${PVA_THRESH} \
        # ${RZM_THRESH} \
        # ${INTNES_THRESH}
}

function run_step4()
{
    ##Step 4. Cervix cell classification
    python3 step4_annot.py \
        --origin_dir "${ORIGIN_DIR}" \
        --pattern ${FILE_PATTERN}\
        --seg_dir ${CLF_DATASETS}\
        --output_dir ${ANNOT_DIR}
}

function run_step5 ()
{
    ##Step 5. Mark the positive cells
    python3 step5_gendata.py \
        --annot_path ${ANNOT_DIR}'/annotation_default.txt' \
        --seg_dir ${CLF_DATASETS}\
        --output_dir ${TRAINDATA_DIR} \
        --train_test_split \
        #--more_norm
}

function run_step6 ()
{
    echo $TR_FLAG
    python3 step6_copy2nugan.py \
        --origin_dir "${ORIGIN_DIR}" \
        --csv_dir ${ANNOT_DIR}'/fov_type.csv' \
        --npy_dir ${CLF_DATASETS}'/npy/'  \
        --output_dir ${COPY_DIR} \
        --pattern ${FILE_PATTERN} \
        ${TR_FLAG}
        #--train_test_split 
}


function run_all()
{
    #clean
    time1=$(date +%s)
    echo $time1
    
    run_step1
    run_step2
    run_step3
    run_step4
    run_step5
    run_step6
    
    #./copy_fov.sh

    time2=$(date +%s)
    echo $time2
    echo "Total time (sec): "
    echo $(($time2 - $time1))
    
}

function clean()
{
    
    echo "Clean the ${SEGMENT_DIR} Dir"
    rm -rf datasets/segment/test/*
    rm -rf datasets/segment/output/predict/test/*/*
    #Clean the previous results
    echo "Clean the ${CLF_DATASETS} Dir"
    rm -rf ${CLF_DATASETS}
    rm -rf ./marked_image
    rm -rf ./cell_result
    
    
}

function check_env()
{
    if [ ! -d "./datasets/segment" ];then
        mkdir -p ./datasets/segment
    fi
    if [ ! -d "./datasets/segment/stage1_train" ];then
        echo "准备U-Net参考训练集"
        ln -s /opt/zhuoyao_workspace/medical_ai/datasets/segment/stage1_train ./datasets/segment/
    fi
    
    if [ ! -d "././src/SEGMENT/kaggle-dsb2018/src/all_output" ];then
        echo "准备U-Net模型Weights参数"
        ln -s /opt/zhuoyao_workspace/medical_ai/src/SEGMENT/kaggle-dsb2018/src/all_output/ ./src/SEGMENT/kaggle-dsb2018/src 
    fi
}

function detect_testdata()
{
    if [ ! -d "$ORIGIN_DIR" ];then
        #echo $2
        folder=`echo "$ORIGIN_DIR" | sed 's#\(.*test_slide\)/\(.*\)/.*/#\2#g'`
        #echo $folder
        dir=`echo "$ORIGIN_DIR" | sed 's#\(.*test_slide/.*\)/.*/#\1#g'`
        #echo $dir
        
        if [ ! -d "$dir" ];then
        
            if [ ! -d ~/Dataset/private_cervical/${folder} ];then
                #echo "~/Dataset/private_cervical/${folder}"
                echo "原始数据目录不存在，请用命令ls -l ~/Dataset/private_cervical/${folder} 检查原始目录"
                exit 0
            fi
            
            if [ ! -d './datasets/test_slide' ];then
                echo "测试数据文件夹不存在，创建..."
                mkdir -p ./datasets/test_slide
            fi
        
            echo "创建数据目录..."
            ln -s ~/Dataset/private_cervical/${folder} ./datasets/test_slide/
            
        fi
        
    fi
}


show_usage='run.sh all/clean/(step5 THRESHOLD)'


# Exit immediately if a command exits with a non-zero status.
set -e



if [ -n "$1" ]; then
    case "$1" in
        all) check_env;detect_testdata;run_all;;
        clean) clean;;
        step1) check_env;detect_testdata;run_step1;;
        step2) check_env;detect_testdata;run_step2;;
        step3) check_env;detect_testdata;run_step3;;
        step4) check_env;detect_testdata;run_step4;;
        step5) check_env;detect_testdata;run_step5;;
        step6) check_env;detect_testdata;run_step6;;
        
        *) echo ${show_usage};;
    esac
    exit 0
fi

echo $show_usage

