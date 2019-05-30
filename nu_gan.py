import os
import time
import argparse
from utils.experiment import cell_segmentation, cell_representation, cell_representation_eval, image_classification, image_classification_predict, image_classification_predict_ensemble, image_classification_segment

parser = argparse.ArgumentParser()
parser.add_argument('--task', 
                    choices = ['cell_representation', 'cell_representation_eval', 'image_classification', 'image_classification_predict', 'image_classification_predict_ensemble', 'image_classification_segment', 'cell_segmentation'], 
                    help='cell_representation | cell_representation | image_classification |image_classification_predict | image_classification_segment| cell_segmentation|image_classification_predict_ensemble')
parser.add_argument('--kfold',
                    default=5,
                    help='KFold, default 5',
                    type=int)
parser.add_argument('--kfold_choose',
                    default=0,
                    help='KFold choose, default 0',
                    type=int)
parser.add_argument('--predict_experient_root',
                    default='default',
                    help='.predict_experient_root')
                
parser.add_argument('--predict_purity',
                    default='default',
                    help='predict_purity')

parser.add_argument('--predict_entropy',
                    default='default',
                    help='predict_entropy.')

parser.add_argument('--predict_gen_iterations',
                    default='default',
                    help='predict_gen_iterations.')                        
                    
opt = parser.parse_args()

if not (opt.task):
    parser.error("specific a task such as '--task cell_representation'")

#for image classification and nuclei segmentation
experiment_root = './experiment/'
positive_images_root= experiment_root + 'data/original/positive_images/' 
negative_images_root= experiment_root + 'data/original/negative_images/' 
positive_npy_root = experiment_root + 'data/segmented/positive_npy/'
negative_npy_root = experiment_root + 'data/segmented/negative_npy/'
ref_path = experiment_root + 'data/original/reference/BM_GRAZ_HE_0007_01.png'


positive_test_images_root= experiment_root + 'data/original/positive_test_images/' 
negative_test_images_root= experiment_root + 'data/original/negative_test_images/' 
positive_test_npy_root = experiment_root + 'data/segmented/positive_test_npy/'
negative_test_npy_root = experiment_root + 'data/segmented/negative_test_npy/'


#cell_level_data
X_train_path = experiment_root + 'data/cell_level_label/X_train.npy' 
X_test_path = experiment_root + 'data/cell_level_label/X_test.npy' 
y_train_path = experiment_root + 'data/cell_level_label/y_train.npy' 
y_test_path = experiment_root + 'data/cell_level_label/y_test.npy' 

n_epoch=10
batchsize=36
rand=32
dis=1
dis_category=5
ld = 1e-4
lg = 1e-4
lq = 1e-4
random_seed = 42
save_model_steps=100
intensity = 160 #segmentation intensity
multi_process = True #multi core process for nuclei segmentation

fold = opt.kfold
choosing_fold = opt.kfold_choose #cross-validation for classification

time = str(int(time.time()))
    

if opt.task == 'cell_representation':
    if 1- os.path.exists(experiment_root+time+'_'+str(fold)+'_'+str(choosing_fold)):
        os.makedirs(experiment_root+time+'_'+str(fold)+'_'+str(choosing_fold))
        os.makedirs(experiment_root+time+'_'+str(fold)+'_'+str(choosing_fold)+'/'+'picture')
        os.makedirs(experiment_root+time+'_'+str(fold)+'_'+str(choosing_fold)+'/'+'model')

    experiment_root = experiment_root + time +'_'+str(fold)+'_'+str(choosing_fold) + '/'
    print('folder_name:', experiment_root)
    
    cell_representation(X_train_path, X_test_path, y_train_path, y_test_path, experiment_root, 
                            n_epoch, batchsize, rand, dis, dis_category, 
                            ld, lg, lq, save_model_steps)


if opt.task == 'cell_representation_eval':
    if 1- os.path.exists(experiment_root+time+'_'+str(fold)+'_'+str(choosing_fold)):
        os.makedirs(experiment_root+time+'_'+str(fold)+'_'+str(choosing_fold))
        os.makedirs(experiment_root+time+'_'+str(fold)+'_'+str(choosing_fold)+'/'+'picture')
        os.makedirs(experiment_root+time+'_'+str(fold)+'_'+str(choosing_fold)+'/'+'model')

    experiment_root = experiment_root + time +'_'+str(fold)+'_'+str(choosing_fold) + '/'
    print('folder_name:', experiment_root)
    
    cell_representation_eval(X_train_path, X_test_path, y_train_path, y_test_path, experiment_root, 
                            n_epoch, batchsize, rand, dis, dis_category, 
                            ld, lg, lq, save_model_steps)

if opt.task == 'image_classification':
    if 1- os.path.exists(experiment_root+time+'_'+str(fold)+'_'+str(choosing_fold)):
        os.makedirs(experiment_root+time+'_'+str(fold)+'_'+str(choosing_fold))
        os.makedirs(experiment_root+time+'_'+str(fold)+'_'+str(choosing_fold)+'/'+'picture')
        os.makedirs(experiment_root+time+'_'+str(fold)+'_'+str(choosing_fold)+'/'+'model')

    experiment_root = experiment_root + time +'_'+str(fold)+'_'+str(choosing_fold) + '/'
    print('folder_name:', experiment_root)
    
    image_classification(positive_images_root, negative_images_root, positive_npy_root,negative_npy_root, 
                         ref_path, intensity, X_train_path, X_test_path, y_train_path, y_test_path, 
                         experiment_root, multi_process, fold, random_seed, choosing_fold, n_epoch, 
                         batchsize, rand, dis, dis_category, ld, lg, lq, save_model_steps)
                         
                         
if opt.task == 'image_classification_predict':
    experiment_root = experiment_root + time +'_'+str(fold)+'_'+str(choosing_fold) + '/'
    print('folder_name:', experiment_root)
    
    image_classification_predict(positive_images_root, negative_images_root, positive_npy_root,negative_npy_root, 
                         positive_test_images_root, negative_test_images_root, positive_test_npy_root,negative_test_npy_root,
                         ref_path, intensity, X_train_path, X_test_path, y_train_path, y_test_path, 
                         experiment_root, multi_process, fold, random_seed, choosing_fold, n_epoch, 
                         batchsize, rand, dis, dis_category, ld, lg, lq, save_model_steps, 
                         opt.predict_experient_root, opt.predict_purity, opt.predict_entropy, opt.predict_gen_iterations
                         )


if opt.task == 'image_classification_predict_ensemble':
    experiment_root = experiment_root + time +'_'+str(fold)+'_'+str(choosing_fold) + '/'
    print('folder_name:', experiment_root)
    
    image_classification_predict_ensemble(positive_images_root, negative_images_root, positive_npy_root,negative_npy_root, 
                         positive_test_images_root, negative_test_images_root, positive_test_npy_root,negative_test_npy_root,
                         ref_path, intensity, X_train_path, X_test_path, y_train_path, y_test_path, 
                         experiment_root, multi_process, fold, random_seed, choosing_fold, n_epoch, 
                         batchsize, rand, dis, dis_category, ld, lg, lq, save_model_steps, 
                         opt.predict_experient_root, opt.predict_purity, opt.predict_entropy, opt.predict_gen_iterations
                         )


if opt.task == 'image_classification_segment':
    image_classification_segment(positive_images_root, negative_images_root, positive_npy_root,negative_npy_root, 
                         positive_test_images_root, negative_test_images_root, positive_test_npy_root,negative_test_npy_root,
                         ref_path, intensity, X_train_path, X_test_path, y_train_path, y_test_path, 
                         experiment_root, multi_process, fold, random_seed, choosing_fold, n_epoch, 
                         batchsize, rand, dis, dis_category, ld, lg, lq, save_model_steps,)


if opt.task == 'cell_segmentation':
    cell_segmentation(positive_images_root, negative_images_root, positive_npy_root, 
                          negative_npy_root, ref_path, intensity, multi_process)