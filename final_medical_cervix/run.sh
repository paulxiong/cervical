#!/bin/bash
#ORIGIN_DIR='datasets/origin_folder/*/*'
#ORIGIN_DIR='datasets/segment/priv_debug/Original_FOVs/*'
#ORIGIN_DIR='datasets/origin_train/orgin_02052019_cells/LSIL_HPV_1817897'
#ORIGIN_DIR='datasets/origin_train/origin_01_15'
ORIGIN_DIR='datasets/origin_train/orgin_02052019_cells/train/'
#ORIGIN_DIR='/opt/zhuoyao_workspace/medical_ai/datasets/segment/priv_debug/Original_FOVs/*'
#ORIGIN_DIR='datasets/origin_12_06/'
#ORIGIN_DIR='datasets/origin_test/'
#ORIGIN_DIR='datasets/origin_test/slide/HYN_HSIL_T219590/Images'
#ORIGIN_DIR='datasets/origin_test/2018-12-14'
#ORIGIN_DIR='datasets/origin_test/2019-01-04'
#ORIGIN_DIR='/opt/xing_workspace/final_medical_cervix/datasets/origin_test/194308'
#ORIGIN_DIR='/opt/xing_workspace/final_medical_cervix/datasets/origin_test/193413'
#ORIGIN_DIR='datasets/origin_test/2019-01-30'
#ORIGIN_DIR='/opt/zhuoyao_workspace/Datasets/private_cervical/2018-12-14/1804615_FJ/Images'
#ORIGIN_DIR='/opt/zhuoyao_workspace/Datasets/private_cervical/2018-12-14/180130_HD/Images'
ROOT=`pwd`
#ORIGIN_DIR='datasets/origin_train/origin_01_15'
SEGMENT_DIR='datasets/segment/test/'
FILE_PATTERN='*.png'
#FILE_PATTERN='*.JPG'
#CLF_DATASETS='datasets/classify/origin_test'
CLF_DATASETS='datasets/classify'
#CLF_WEIGHTS='./src/CLASSIFY/inceptionV3_final_1/inception.fold_5.hdf5'
#CLF_WEIGHTS='./src/CLASSIFY/inceptionV3_final_1/inception_single_RandomRotate_MultiClass.hdf5'
#CLF_WEIGHTS='./src/CLASSIFY/inceptionV3_final_1/inception.fold_3_RandomRotate_MultiClass.hdf5'
#CLF_WEIGHTS='./src/CLASSIFY/inceptionV3_final_1/weights_bak/inception.fold_3_RandomRotate_MultiClass_2019-01-03.hdf5'
#CLF_WEIGHTS='./src/CLASSIFY/inceptionV3_final_1/weights_bak/inception.fold_3_RandomRotate_MultiClass_2019-01-03.hdf5'
#CLF_WEIGHTS='./src/CLASSIFY/inceptionV3_final_1/weights_bak/2nd_batch/inception.fold_5_Double_ZoomOut_Padding_RandomRotate_CellBased_0.5_MultiClass_RGB.hdf5'
#CLF_WEIGHTS='./src/CLASSIFY/inceptionV3_final_1/weights_bak/2nd_batch_warp/inception.fold_5_Warp_RandomRotate_CellBased_0.5_MultiClass_RGB.hdf5'
CLF_WEIGHTS='./src/CLASSIFY/inceptionV3_final_1/weights_bak/75x75_2nd3rd_train_0222/inception.fold_5_Warp_Up_All_FovBased_0.5_MultiClass_RGB_NormalLoss.hdf5'
#CLF_WEIGHTS='./src/CLASSIFY/inceptionV3_final_1/weights_bak/2nd_batch_hist_eq/inception.fold_5_Double_ZoomOut_Padding_RandomRotate_CellBased_0.5_MultiClass_HIST_BATCH_EQ_LAB.hdf5'
#CLF_WEIGHTS='./src/CLASSIFY/inceptionV3_final_1/weights_bak/2nd_batch_CLAHE_L/inception.fold_5_Double_ZoomOut_Padding_RandomRotate_CellBased_0.5_MultiClass_LAB_CLAHE_L.hdf5'
MARK_DIR='marked_image'
THRESHOLD=0.5
CLF_INPUT_WIDTH=75
CLF_INPUT_HEIGHT=75
CLF_MODE=MultiClass
SEG_MODEL=all
#SEG_MODEL=c3
SEG_COLOR=colouronly
#SEG_COLOR=greyonly
CUDA_DEVICE=1
DENOSING=--denoising
#DENOSING=
COLOR_MODE='RGB'
PADDING='Warp'
CROP_METHOD='Square'
#COLOR_MODE='LAB_CLAHE_L'
#COLOR_MODE='HIST_BATCH_EQ_LAB'
AREA_THRESH=100
#PVA_THRESH=
RZM_THRESH=
INTNES_THRESH=
PVA_THRESH="--perimeter_vs_area 18"
#RZM_THRESH="--zernike_thresh 3.7"
#INTNES_THRESH="--intensity_thresh 40"


function run_step1()
{
    ##Step 1. Copy FOVs to segmentation dir
    python3 step1.py \
        --origindir "${ORIGIN_DIR}" \
        --segtestdir ${SEGMENT_DIR} \
        --filepattern ${FILE_PATTERN} \
	--resize_ratio 0.5 \
        --$SEG_COLOR \
        $DENOSING
}
function run_step2()
{
    ##Step 2. Run Segmentation
    cd src/SEGMENT/kaggle-dsb2018/src/
    
    python3 schwaebische_nuclei.py predict_test \
        --mosaic \
        --loadmodel ${SEG_MODEL}_output/ \
        --predicttestonly \
        --cuda_device $CUDA_DEVICE \
        --$SEG_COLOR
    
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
        --seg_color ${SEG_COLOR} \
        --area_thresh ${AREA_THRESH} \
         ${PVA_THRESH} \
         ${RZM_THRESH} \
         ${INTNES_THRESH}
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
    python3 step5.py \
        --origindir "${ORIGIN_DIR}" \
        --filepattern ${FILE_PATTERN}\
        --datasets ${CLF_DATASETS}\
        --outputdir ${MARK_DIR} \
        --threshold $THRESHOLD \
        --clf_mode $CLF_MODE
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
    rm -rf ${CLF_DATASETS}/*_output
    rm -rf ./marked_image
    rm -rf ./cell_result
    
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

