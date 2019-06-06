ROOT_DIR='./'
DATA_ROOT_DIR='../src/CLASSIFY/inceptionV3_final_1/datasets/'
ORIGIN_DIR='../datasets/origin_train/*'
#ORIGIN_DIR='origin_10_1_abnormal_img'
DATA_DIR='classify'
OUTPUT_DIR='mark_pos'
LISTFILE_PATH='listfile5.txt'

python3 ./mark_pos.py \
 --origindir="${ORIGIN_DIR}" \
 --datasets="${DATA_ROOT_DIR}${DATA_DIR}" \
 --outputdir="${ROOT_DIR}${OUTPUT_DIR}" \
 --listfile="${ROOT_DIR}${LISTFILE_PATH}"
