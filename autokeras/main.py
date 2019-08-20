# -*- coding: utf-8 -*-
import os, csv, cv2, time, argparse, shutil
# 匹配参数放在这里是因为如果参数不对就可以报错退出，否则后面的import会占用很长时间然后再报错退出
parser = argparse.ArgumentParser()
parser.add_argument('--task', choices = ['train', 'predict', 'predict2'], help='train or predict')
parser.add_argument('--taskdir', help='fold path for train/predict')
opt = parser.parse_args()
if not (opt.task) or (opt.task != 'train' and opt.task != 'predict' and opt.task != 'predict2'):
    parser.error("specific a task such as '--task train'")
if opt.taskdir is None or len(opt.taskdir) < 1:
    parser.error("specific path such as '--taskdir your/path/data'")

from autokeras.utils import pickle_from_file
from autokeras.image.image_supervised import load_image_dataset, ImageClassifier
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
from shutil import copyfile

def timestamp():
    return time.strftime("%Y%m%d_%H%M%S", time.localtime())

#write csv
def write_csv(img_dir, csv_dir):
    list = []
    list.append(['File Name','Label'])
    for file_name in os.listdir(img_dir):
    	for img in os.listdir("%s/%s"%(img_dir,file_name)):
            #print (img)
            item = [file_name+"/"+img, file_name]
            list.append(item)
    f = open(csv_dir, 'w')
    writer = csv.writer(f)
    writer.writerows(list)

#resize images
def resize_img(input_dir, output_dir, RESIZE):
    cls_file = os.listdir(input_dir)
    for cls_name in cls_file:
        img_file = os.listdir("%s/%s"%(input_dir,cls_name))
        for img_name in img_file:
            #print (img_name)
            img = cv2.imread("%s/%s/%s"%(input_dir,cls_name,img_name))
            img = cv2.resize(img,(RESIZE,RESIZE),interpolation=cv2.INTER_LINEAR)
            if os.path.exists("%s/%s"%(output_dir,cls_name)):
                cv2.imwrite("%s/%s/%s"%(output_dir,cls_name,img_name),img)
            else:
                os.makedirs("%s/%s"%(output_dir,cls_name))
                cv2.imwrite("%s/%s/%s"%(output_dir,cls_name,img_name),img)

class cervical_autokeras():
    def __init__(self, ROOTPATH):
        #训练、预测任务的顶层目录, 训练是按照时间随机生成的，预测是人为指定的
        self.ROOTPATH = ROOTPATH
        #保存中间过程的目录
        self.TEMP_DIR = os.path.join(self.ROOTPATH, 'autokeras')
        #Folder for storing training images
        self.TRAIN_IMG_DIR = os.path.join(self.ROOTPATH, 'train')
        self.RESIZE_TRAIN_IMG_DIR = os.path.join(self.ROOTPATH,'resize_train')
        #Folder for storing testing images
        self.TEST_IMG_DIR = os.path.join(self.ROOTPATH, 'test')
        self.RESIZE_TEST_IMG_DIR = os.path.join(self.ROOTPATH, 'resize_test')
        #Folder for storing predict images
        self.PREDICT_IMG_DIR = os.path.join(self.ROOTPATH, 'predict')
        self.RESIZE_PREDICT_IMG_DIR = os.path.join(self.ROOTPATH, 'resize_predict')
        #Path to generate csv file
        self.TRAIN_CSV_DIR = os.path.join(self.ROOTPATH, 'train_labels.csv')
        self.TEST_CSV_DIR = os.path.join(self.ROOTPATH, 'test_labels.csv')
        self.PREDICT_CSV_DIR = os.path.join(self.ROOTPATH, 'predict_labels.csv')
        #Path to generate model file
        self.MODEL_DIR = os.path.join(self.ROOTPATH, 'Model.h5')
        #If your memory is not enough, please turn down this value.(my computer memory 16GB)
        self.RESIZE = 128
        #Set the training time, this is half an hour
        self.TIME = 0.5*60*60

        if not os.path.exists(self.ROOTPATH):
             os.makedirs(self.ROOTPATH)

        self.clean_fold()

    def clean_fold(self):
        dirs = [self.RESIZE_TRAIN_IMG_DIR, self.RESIZE_TEST_IMG_DIR, self.RESIZE_PREDICT_IMG_DIR]
        files = [self.TRAIN_CSV_DIR, self.TEST_CSV_DIR, self.PREDICT_CSV_DIR]
        for d in dirs:
            if os.path.exists(d):
                shutil.rmtree(d)
        for f in files:
            if os.path.exists(f):
                os.remove(f)

    def train_autokeras(self):
        #Load images
        train_data, train_labels = load_image_dataset(csv_file_path=self.TRAIN_CSV_DIR, images_path=self.RESIZE_TRAIN_IMG_DIR)
        test_data, test_labels = load_image_dataset(csv_file_path=self.TEST_CSV_DIR, images_path=self.RESIZE_TEST_IMG_DIR)

        train_data = train_data.astype('float32') / 255
        test_data = test_data.astype('float32') / 255
        print("Train data shape:", train_data.shape)

        clf = ImageClassifier(verbose=True, path=self.TEMP_DIR)
        clf.fit(train_data, train_labels, time_limit=self.TIME)
        clf.final_fit(train_data, train_labels, test_data, test_labels, retrain=True)

        y = clf.evaluate(test_data, test_labels)
        print("Evaluate:", y)

        ##Predict the category of the test image
        #img = load_img(PREDICT_IMG_PATH)
        #x = img_to_array(img)
        #x = x.astype('float32') / 255
        #x = np.reshape(x, (1, RESIZE, RESIZE, 3))
        #print("x shape:", x.shape)
        #y = clf.predict(x)
        #print("predict:", y)

        # clf.load_searcher().load_best_model().produce_keras_model().save(MODEL_DIR)
        # clf.export_keras_model(MODEL_DIR)
        clf.export_autokeras_model(self.MODEL_DIR)

    def predict_autokeras(self):
        #Load images
        test_data, test_labels = load_image_dataset(csv_file_path=self.PREDICT_CSV_DIR, images_path=self.RESIZE_PREDICT_IMG_DIR)
        test_data = test_data.astype('float32') / 255
        print("Test data shape:", test_data.shape)

        autokeras_model = pickle_from_file(self.MODEL_DIR)
        autokeras_score = autokeras_model.evaluate(test_data, test_labels)
        print(autokeras_score)
        
    def predict_autokeras2(self):
        #Load images
        test_data, test_labels = load_image_dataset(csv_file_path=self.PREDICT_CSV_DIR, images_path=self.RESIZE_PREDICT_IMG_DIR)
        img_path_1 = self.ROOTPATH + 'predict/'
        predict_error_path = self.ROOTPATH + 'predict_error_data/'
        if os.path.exists(predict_error_path):
            shutil.rmtree(predict_error_path)
        if not os.path.exists(predict_error_path):
            os.mkdir(predict_error_path)
        list_name = os.listdir(img_path_1)
        all_name = []
        all_name_path = []
        for k in list_name:
            path_temp = img_path_1 + k
            list_name_temp = os.listdir(path_temp)
            for k1 in list_name_temp:
                list_name_temp_path = path_temp + '/' + ''.join(k1)
            for kk in list_name_temp:
                all_name.append(kk) #文件名
                all_name_path.append(path_temp + '/' +''.join(kk)) #文件路径
        test_data = test_data.astype('float32') / 255
        print("Test data shape:", test_data.shape)

        autokeras_model = pickle_from_file(self.MODEL_DIR)
        autokeras_score = autokeras_model.evaluate(test_data, test_labels)
        label_predict = autokeras_model.predict(test_data)
        print("============predict============")
        count = 0
        count_ture = 0
        for img_path, i, n,m in zip(all_name_path, all_name,test_labels, label_predict):
            print("文件名：%s     真实标签：%s     预测标签：%s"%(i, n,m))
            count = count + 1
            if n == m:
                count_ture = count_ture + 1
            else:
                copyfile(img_path, predict_error_path + '/' + i)
        print("准确率：",count_ture/count)
        print("评估得分：",autokeras_score)    

if __name__ == "__main__":
    ca = cervical_autokeras(opt.taskdir)

    if opt.task == 'train':
        print ("Resize images...")
        resize_img(ca.TRAIN_IMG_DIR, ca.RESIZE_TRAIN_IMG_DIR, ca.RESIZE)
        resize_img(ca.TEST_IMG_DIR, ca.RESIZE_TEST_IMG_DIR, ca.RESIZE)
        print ("write csv...")
        write_csv(ca.RESIZE_TRAIN_IMG_DIR, ca.TRAIN_CSV_DIR)
        write_csv(ca.RESIZE_TEST_IMG_DIR, ca.TEST_CSV_DIR)
        print ("============Load...=================")
        ca.train_autokeras()
    elif opt.task == 'predict':
        print ("Resize images...")
        resize_img(ca.PREDICT_IMG_DIR, ca.RESIZE_PREDICT_IMG_DIR, ca.RESIZE)
        print ("write csv...")
        write_csv(ca.RESIZE_PREDICT_IMG_DIR, ca.PREDICT_CSV_DIR)
        print ("============Load...=================")
        ca.predict_autokeras()

    elif opt.task == 'predict2':
        print ("Resize images...")
        resize_img(ca.PREDICT_IMG_DIR, ca.RESIZE_PREDICT_IMG_DIR, ca.RESIZE)
        print ("write csv...")
        write_csv(ca.RESIZE_PREDICT_IMG_DIR, ca.PREDICT_CSV_DIR)
        print ("============Load...=================")
        ca.predict_autokeras2()
