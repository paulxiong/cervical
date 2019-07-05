import os
from step1v2 import step1v2

if __name__ == '__main__':
    origindir='/ai/lambdatest/*/'
    segtestdir='datasets/segment/test/'
    filepattern='*.JPG'

    #python3 step1.py --origindir '/ai/lambdatest/*/' --segtestdir datasets/segment/test/ --filepattern '*.JPG'
    print("step1")
    step1v2(origindir, segtestdir, filepattern)

    #python3 schwaebische_nuclei_predict.py predict_test --mosaic --loadmodel all_output/ --predicttestonly --cuda_device 1 --colouronly
    print("step2")

    #python3 step3.py --origindir '/ai/lambdatest/*/' --filepattern '*.JPG' --datasets datasets/classify
    #                 --segtestdir datasets/segment/test/ --crop_method Mask --area_thresh 100 --square_edge 50 --perimeter_vs_area 18
    print("step3")

    #python3 step4_annot.py --origin_dir '/ai/lambdatest/*/' --pattern '*.JPG' --seg_dir datasets/classify --output_dir datasets/classify/annot_out
    print("step4")

    #python3 step5_gendata.py --annot_path datasets/classify/annot_out/annotation_default.txt --seg_dir datasets/classify
    #                         --output_dir datasets/classify/train_datasets --train_test_split
    print("step5")

    #python3 step6_copy2nugan.py --origin_dir '/ai/lambdatest/*/' --csv_dir datasets/classify/annot_out/fov_type.csv
    #                            --npy_dir datasets/classify/npy/ --output_dir datasets/classify/data --pattern '*.JPG'
    print("step6")
