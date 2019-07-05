import os,sys
from step1v2 import step1v2
sys.path.append(os.path.abspath('step2v2'))
sys.path.append(os.path.abspath('step2v2/modules/'))

if __name__ == '__main__':
    #python3 step1.py --origindir '/ai/lambdatest/*/' --segtestdir datasets/segment/test/ --filepattern '*.JPG'
    print("step1")
    input_origindir='/ai/lambdatest/*/'
    output_segtestdir='datasets/segment/test/'
    filepattern='*.JPG'
    step1v2(input_origindir, output_segtestdir, filepattern)

    #python3 schwaebische_nuclei_predict.py predict_test --mosaic --loadmodel all_output/ --predicttestonly --cuda_device 1 --colouronly
    print("step2")
    from step2v2.schwaebische_nuclei_predict_v2 import step2v2
    action = 'predict_test'
    modpath = './all_output'
    cuda_device = '1'
    datasets_train_path = 'datasets/segment/stage1_train'
    input_datasets_test_path = 'datasets/segment/test'
    step2v2(action, modpath, cuda_device, datasets_train_path, input_datasets_test_path)

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
