#!/bin/bash
ORIGIN_DIR='datasets/origin_test/positive_test_images/'
#ORIGIN_DIR='datasets/origin_test/HPV_1817897/'
#ORIGIN_DIR='datasets/origin_test/1903689_N_39yrs/'
#ORIGIN_DIR='/opt/zhuoyao_workspace/Datasets/private_cervical/2019-05-09/1804615_PNG'

#ORIGIN_DIR='/opt/zhuoyao_workspace/Datasets/private_cervical/2019-05-07/1903552_N_27yrs'

#ORIGIN_DIR='datasets/origin_test/2019-01-04/'

#ORIGIN_DIR = '/GAN/nu_gan/experiment/data/original/negative_test_images/'

ROOT=`pwd`
#ORIGIN_DIR='datasets/origin_train/origin_01_15'
SEGMENT_DIR='datasets/segment/test/'
#FILE_PATTERN='*.BMP'
FILE_PATTERN='*.png'
#FILE_PATTERN='*.JPG'
#CLF_DATASETS='datasets/classify/origin_test'
CLF_DATASETS='datasets/classify/'
ABNORMAL_FOVS='datasets/abnormal_FOVs/'
ABNORMAL_CELLS_FOLDER='datasets/abnormal_cells/'
SLIDE_NAME='1804615_PNG'
CLF_WEIGHTS='./src/CLASSIFY/inceptionV3_final_1/weights_GAN_GRAY/inception.fold_5_Warp_Up_All_CellBased_0.5_MultiClass_RGB_NormalLoss.hdf5'
#CLF_WEIGHTS='./src/CLASSIFY/inceptionV3_final_1/weights/75x75_2nd_batch/inception.fold_5_Warp_Up_All_CellBased_0.5_MultiClass_RGB.hdf5'
#CLF_WEIGHTS='./src/CLASSIFY/inceptionV3_final_1/weights_bak/75x75_2nd3rd_train_0222/inception.fold_5_Warp_Up_All_FovBased_0.5_MultiClass_RGB_NormalLoss.hdf5'
#CLF_WEIGHTS='./src/CLASSIFY/inceptionV3_final_1/weights_bak/75x75_2nd3rd_train_0222/inception.fold_5_Warp_RandomRotate_FovBased_0.5_MultiClass_RGB_NormalLoss.hdf5'
#CLF_WEIGHTS='./src/CLASSIFY/inceptionV3_final_1/weights_bak/75x75_2nd_cleaned/inception.fold_5_Warp_Up_All_CellBased_0.5_MultiClass_RGB_NormalLoss.hdf5'
#CLF_WEIGHTS='/opt/zhuoyao_workspace/medical_ai/classifier/weights_bak/75x75_2nd3rd_train_0222/inception.fold_5_Warp_Up_All_FovBased_0.5_MultiClass_RGB_NormalLoss.hdf5'
#CLF_WEIGHTS='./src/CLASSIFY/inceptionV3_final_1/weights_bak/inception.fold_5_Warp_Majority_Down_Minority_Up_CellBased_0.5_MultiClass_RGB_WeightedLoss.hdf5'
MARK_DIR='marked_image'
THRESHOLD=0.5
CLF_INPUT_WIDTH=75
CLF_INPUT_HEIGHT=75
CLF_MODE=MultiClass
SEG_MODEL=all
#SEG_MODEL=c3
SEG_COLOR=colouronly
#SEG_COLOR=greyonly
CUDA_DEVICE=0
#DENOSING=--denoising
DENOSING=
COLOR_MODE='RGB'
PADDING='Warp'
#CROP_METHOD='Square'
CROP_METHOD='Margin'
#COLOR_MODE='LAB_CLAHE_L'
#COLOR_MODE='HIST_BATCH_EQ_LAB'


function run_step1()
{
    ##Step 1. Copy FOVs to segmentation dir
    python3 step1.py \
        --origindir "${ORIGIN_DIR}" \
        --segtestdir ${SEGMENT_DIR} \
        --filepattern ${FILE_PATTERN} \
        --$SEG_COLOR \
        $DENOSING
}
function run_step2()
{
    ##Step 2. Run Segmentation
    cd src/SEGMENT/kaggle-dsb2018/src/
    ./run.sh $CUDA_DEVICE $SEG_MODEL $SEG_COLOR
    cd $ROOT
}

function run_step3()
{
    ##Step 3. Crop the FOVs into cells
    python3 step3_old.py \
        --origindir "${ORIGIN_DIR}" \
        --filepattern ${FILE_PATTERN}\
        --datasets ${CLF_DATASETS}\
        --segtestdir ${SEGMENT_DIR}\
        --crop_method ${CROP_METHOD} \
        --seg_color ${SEG_COLOR}
}

function run_step4()
{
    ##Step 4. Cervix cell classification
    python3 step4.py \
        --origindir "${ORIGIN_DIR}" \
        --filepattern ${FILE_PATTERN}\
        --datasets ${CLF_DATASETS}\
        --weights  ${CLF_WEIGHTS}\
        --threshold $THRESHOLD \
        --clf_mode $CLF_MODE \
        --color_mode $COLOR_MODE \
        --padding $PADDING \
	--input_shape $CLF_INPUT_HEIGHT $CLF_INPUT_WIDTH \
        --cuda_device $CUDA_DEVICE
}

function run_step5 ()
{
    ##Step 5. Mark the positive cells
    python3 step5_slide.py \
        --origindir "${ORIGIN_DIR}" \
        --filepattern ${FILE_PATTERN}\
        --datasets ${CLF_DATASETS}\
        --outputdir ${MARK_DIR} \
        --abnormalfovs ${ABNORMAL_FOVS} \
        --abnormalcells ${ABNORMAL_CELLS_FOLDER} \
        --slidename ${SLIDE_NAME} \
        --threshold $THRESHOLD \
        --clf_mode $CLF_MODE
}


function run_all()
{
    clean
    time1=$(date +%s)
    echo $time1
    
    run_step1
    run_step2
    run_step3
    #run_step4
    #run_step5

    time2=$(date +%s)
    echo $time2
    echo "Total time (sec): "
    echo $(($time2 - $time1))
    
}

function clean()
{
    #Clean the previous results
    echo "Clean the ${CLF_DATASETS} Dir"
    sudo rm -rf ${CLF_DATASETS}/*_output
    sudo rm -rf ${CLF_DATASETS}/$MARK_DIR
    #echo "Clean the ${SEGMENT_DIR} Dir"
    #sudo rm -rf $SEGMENT_DIR/*
    echo "Clean the ${ABNORMAL_FOVS} Dir"
    sudo rm -rf $ABNORMAL_FOVS/*
}

show_usage='run.sh all/clean/(step5 THRESHOLD)'


# Exit immediately if a command exits with a non-zero status.
set -e

if [ -n "$1" ]; then
    case "$1" in
        all) run_all;;
        clean) clean;;
        step1) run_step1;;
        step2) run_step2;;
        step3) run_step3;;
        step4) run_step4;;
        step5) THRESHOLD=$2; run_step5;;
        *) echo ${show_usage};;
    esac
    exit 0
fi

echo $show_usage

