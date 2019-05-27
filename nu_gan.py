import os
import time
import argparse
from utils.experiment import cell_segmentation, cell_representation, cell_representation_eval, image_classification, image_classification_predict, image_classification_segment, image_classification_train
import ConfigParser
import re

from result_archiver import Archiver

def get_input(string):
    reply = raw_input(string)
    reply = reply.lower()
    while reply not in ['yes', 'y', 'no', 'n']:
        reply = raw_input("Please Enter 'yes' or 'no':")
        
    if reply in ['no', 'n']:
        reply=False
    else:
        reply=True
    return reply
    



config = ConfigParser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), "configure.conf")
config.read(config_path)

parser = argparse.ArgumentParser()
parser.add_argument('--task', 
                    choices = ['cell_representation', 'cell_representation_eval', 'image_classification', 'image_classification_predict','image_classification_train','image_classification_segment', 'cell_segmentation'], 
                    help='cell_representation | cell_representation | image_classification |image_classification_predict | image_classification_segment| cell_segmentation')
#parser.add_argument('--image_path',
#                    help='Test images path')
#parser.add_argument('--clf_model_path',
#                    help='Classifier model path')
opt = parser.parse_args()

if not (opt.task):
    parser.error("specific a task such as '--task cell_representation'")
#elif opt.task == 'image_classification_predict':
#    if not (opt.image_path):
#        parser.error("specific a test image path")
#    if not (clf_model_path):
#        parser.error("specific a classifier model path")
        

#for image classification and nuclei segmentation
experiment_root = config.get('data', 'experiment_root')
positive_images_root= experiment_root + config.get('data', 'train_path_p') 
negative_images_root= experiment_root + config.get('data', 'train_path_n') 
positive_npy_root = experiment_root + config.get('data', 'train_npy_path_p') 
negative_npy_root = experiment_root + config.get('data', 'train_npy_path_n')
ref_path = experiment_root + 'data/original/reference/BM_GRAZ_HE_0007_01.png'


positive_test_images_root= experiment_root +  config.get('data', 'test_path_p') 
negative_test_images_root= experiment_root +  config.get('data', 'test_path_n') 
positive_test_npy_root = experiment_root + config.get('data', 'test_npy_path_p')
negative_test_npy_root = experiment_root + config.get('data', 'test_npy_path_n')


#cell_level_data
X_train_path = experiment_root + 'data/cell_level_label/X_train.npy' 
X_test_path = experiment_root + 'data/cell_level_label/X_test.npy' 
y_train_path = experiment_root + 'data/cell_level_label/y_train.npy' 
y_test_path = experiment_root + 'data/cell_level_label/y_test.npy' 

n_epoch=550
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

fold = 4
choosing_fold = 1 #cross-validation for classification

time = str(int(time.time()))
print(experiment_root)
print(time)
if not os.path.exists(experiment_root+time):
    os.makedirs(experiment_root+time)
    os.makedirs(experiment_root+time+'/'+'picture')
    os.makedirs(experiment_root+time+'/'+'model')
    
experiment_root = experiment_root + time + '/'
print('folder_name:'+str(time))

if opt.task == 'cell_representation':
    cell_representation(X_train_path, X_test_path, y_train_path, y_test_path, experiment_root, 
                            n_epoch, batchsize, rand, dis, dis_category, 
                            ld, lg, lq, save_model_steps)


if opt.task == 'cell_representation_eval':
    cell_representation_eval(X_train_path, X_test_path, y_train_path, y_test_path, experiment_root, 
                            n_epoch, batchsize, rand, dis, dis_category, 
                            ld, lg, lq, save_model_steps)

if opt.task == 'image_classification':
    image_classification(positive_images_root, negative_images_root, positive_npy_root,negative_npy_root, 
                         ref_path, intensity, X_train_path, X_test_path, y_train_path, y_test_path, 
                         experiment_root, multi_process, fold, random_seed, choosing_fold, n_epoch, 
                         batchsize, rand, dis, dis_category, ld, lg, lq, save_model_steps)
                         
                         
if opt.task == 'image_classification_train':
    image_classification_train(positive_images_root, negative_images_root, positive_npy_root,negative_npy_root, 
                         positive_test_images_root, negative_test_images_root, positive_test_npy_root,negative_test_npy_root,
                         ref_path, intensity, X_train_path, X_test_path, y_train_path, y_test_path, 
                         experiment_root, multi_process, fold, random_seed, choosing_fold, n_epoch, 
                         batchsize, rand, dis, dis_category, ld, lg, lq, save_model_steps)
                         
    reply = get_input("Do you want archive Test data and model?(Y/N):")
    if not reply:
        exit()
    else:
        #creat result saver
        saver = Archiver()
        saver.init()
        archive_type='Test'
        reply1 = get_input("Do you want to archive train data?(Y/N):")
        if reply1:
            archive_type='Train'
            saver.archive_train()
        saver.archive_test()
        saver.archive_model()
        saver.update_db(archive_type)
    


if opt.task == 'image_classification_segment':
    image_classification_segment(positive_images_root, negative_images_root, positive_npy_root,negative_npy_root, 
                         positive_test_images_root, negative_test_images_root, positive_test_npy_root,negative_test_npy_root,
                         ref_path, intensity, X_train_path, X_test_path, y_train_path, y_test_path, 
                         experiment_root, multi_process, fold, random_seed, choosing_fold, n_epoch, 
                         batchsize, rand, dis, dis_category, ld, lg, lq, save_model_steps)


if opt.task == 'cell_segmentation':
    cell_segmentation(positive_images_root, negative_images_root, positive_npy_root, 
                          negative_npy_root, ref_path, intensity, multi_process)
                          

if opt.task == 'image_classification_predict':
    image_classification_predict(positive_test_images_root, negative_test_images_root, positive_test_npy_root,negative_test_npy_root,
                         ref_path, intensity, experiment_root, dis_category)
                         
    

