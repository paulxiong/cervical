# final_medical_cervix
final_medical_cervix AI project

1) Please do not update .png test/train img files to this project.
2) Please download the models files from our cloud server.

## Pipeline Predict
* Root Dir: ./  
* Predict:  
./run.sh {all/step1.../step5} [Threshold]  
**Comments:**  
  * {all/step1.../step5}:  
 all: run all steps(from step1 to step5}  
 step1: run step1--Copy FOVs to Segmentation Dir  
 step2: run step2--Segmentation  
 step3: run step3--Crop FOVs into cells  
 step4: run step4--Classification  
 step5: run step5--Mark result on FOVs  
 clean: clean all the tmp files  
  * Parameters(can be changed in run.sh):  
 ORIGIN_DIR: path to original fovs  
 CLF_WEIGHTS: path to classification weights  
 CLF_MODE: Classifier's mode, Binary/MultiClass  
 THRESHOLD: Positive's threshold. When Classifier's mode is MultiClass mode, THRESHOLD is ignored for the class is determined by the biggest possibility in all classes. Default 0.5.  
 SEG_MODEL: Reference to 'Segmentation' Part, which Segmentation model to use, default: all (a backup model of c3).  
 SEG_COLOR: Use GRAY/COLOR to do segmentation.  
 CUDA_DEVICE: which GPU to use, support only one GPU each time, 0 ~ 7.  
 DENOISING: Do mean filtering to reduce gaussian noise when copy the FOVs to segment.  
 * **Steps:**  
   * Copy data to ORIGIN_DIR, the script will find all *.png in the ORIGIN_DIR.  
   * ./run.sh all   
   * Check the predictions in ./datasets/classify/marked_images  
 

Segmentation
-

* Root Dir: src/SEGMENT/kaggle-dsb2018

* Train:  
src/SEGMENT/kaggle-dsb2018/run_train.sh {c1/c2/c3} [private/pub_1st/pub_2nd]  
  * **Comments:**   
    * {c1/c2/c3}:  
  c1:model 1c mosaic with Gaussian noise and speckle noise data augmentation;  
  c2:model 2c mosaic with perspective transform data augmentation  
  c3:model 3c mosaic only  
    * [private/pub_1st/pub_2nd]:  
  private: train on our private labeled data which are labeled with Label Me   
  pub_1st: Train Color model on Science Bowl public stage1 train data.  
  pub_2nd: Train Gray model and Retrain Color model Science Bowl public training dataset stage1 train data(according to README.md in dsb2018, we need to train color model twice in pub_1st and pub_2nd).
  * **Step:**  
    * Prepare train dataset:   
    Private Dataset: PipelineRootDir/datasets/segment/private_train  
    Train Dataset: PipelineRootDir/datasets/segment/stage1_train  
    Test Dataset: PipelineRootDir/datasets/segment/stage1_test
    * Train model:  
    Train c1 model: ./run_train.sh c1  
    Train model without private dataset: ./run_train.sh c1 pub_1st & ./run_train.sh c1 pub_2nd
    * Check result:
    In ./c1_ouput/result

* Predict:  
src/SEGMENT/kaggle-dsb2018/run.sh {CUDA_DIVICE} {MODEL} {COLOURONLY/GRAYONLY}  
**Comments:**  
This script is a part of prediction pipeline. If you want to run segmentation prediction, you need to change to the RootDir of Pipeline and do as follows:  
  * **Step:**  
    * Copy data to ORIGIN_DIR, the script will find all *.png in the ORIGIN_DIR. 
    * ./run.sh step1
    * ./run.sh step2
    * ./run.sh step3
    * Check segmentation result in PipelineRootDir/datasets/Classify/${FOV_basenaem}_output/previews/previews.png & mask.png  
  * **Parameters**
    * CUDA_DIVICE: select a GPU to run the prediction, 0 ~ 7
    * MODEL: same as training {c1/c2/c3} which model weights to use.   
    Note: During prediction, the script will try to load 3 models as c1 & c2 & c3 to do prediction for competetion. For our project, we only need one model, so do remove the dummy models in c1/c2/c3_output/models_colour and keep the newest one.
    * COLOURONLY/GRAYONLY: Use color model or gray model to do the segmentation


Classification
-

* CLFRootDir: src/CLASSIFY/inceptionV3_final_1/

* Prepare Training data(Refer to 'Pipeline Prediction'):  
  * **Step:**  
    * Copy original FOVs to ORIGIN_DIR
    * Do segmentation first, confirm Pipeline Step3 results are ready in PipelineRootDir/datasets/classify/*_output  
    * Generate listfile.txt. Refer to gen_listfile in 'Tools' part. 
    * Copy classifier training data and generate .csv as training input. Refer to clf_preproc.py in 'Tools' part.  
    * Run classifier training scripts. Refer to 'Train' part of 'Classifier'

* Train:  
At first, dataset is splited into 2 parts: TrainSet and TestSet. In training part, a k-fold cv training is implemented to seperate TrainSet into 2 parts for Train and Valid for k times. Testset is used to evaluate the model's robustness and the dataset's distribution consistency.
  * **run_train_augment.sh**  
  Start a parellel training with 4 different augment method for result comparation.  
  Augment method: RandomRotate, Minority, Majority_Down_Minority_Up, Majority_Down.  
  Parameters:   
  CLF_MODE: MultiClass/Binary;  
  COLOR_MODE: RGB, LAB_CLAHE_L/HIST_BATCH_EQ_LAB; default RGB.  
  * **run_train_color.sh**  
  Start a parellel training with 4 different color mode for results comparation.  
  Color mode: RGB, HSV_CLAHE_V, HSV_CLAHE_S, HSV_CLAHE_SV, LAB_CLAHE_L; default RGB (Need to optimize)    
  Parameters:   
  CLF_MODE: MultiClass/Binary;  
  AUGMENT: RandomRotate/Minority/Majority_Down_Minority_Up/Majority_Down.  
  * **run_train_single.sh**  
  Start a training without k-fold validation, dataset is splited into train-test only(here testset is used to validate ). 
  Use this script to generate final models when all the parameters are optimized.  
  Parameters:  
  CLF_MODE: MultiClass/Binary
  
* Analyze Training Result:  
1.在服务器上启动 jupyter notebook:  
  cd /opt/xxx_workspace  
  nohup python3 /usr/local/bin/jupyter-notebook --port 8988 1>./jup.log 2>&1 &  
2.在本地主机上设置 ssh proxy 到jupyter notebook  
  ssh -i .ssh/jps-atec.key -t atec@115.236.22.146 -L 127.0.0.1:8988:127.0.0.1:8988 "ssh 172.16.1.99  -L 127.0.0.1:8988:127.0.0.1:8988"  
3.在服务器上查找jupyter notebook token  
  jupyter notebook list  
  http://localhost:8988/?token=xxxxxx :: /opt/xxx_workspace  
4.在本地主机上登入 http://localhost:8988， 输入第3步查找到的token，进入jupyter notebook web界面  
5.在jupyter notebook web页面中打开：final_medical_cervix/src/CLASSIFY/inceptionV3_final_1/result_analysis.ipynb  
6.重新运行result_analysis.ipynb所有模块后，可以在3.MultiClass Result analysis中看到模型在Train, valid, test三个数据集合上的分数  
 
* Predict: 
Reference to Pipeline Predict


## Tools
* Source Code Dir: PipelineRootDir/tools  

* **annot_img_to_file.py**  
Generate input files and train data for classifer.  
  * Parameters(Modified in script):   
annot_path: path contains the annotated fov images(point annotate) .  
seg_path: Segmetation Result path in which are *_output dirs. And in *_output/preview, there should be label.png for annotation.   

* **clf_preproc.py**  
Generate annotation file for clf_preproc.py.  
  * Parameters(Modified in script):   
LABELFILE_PATH: A list of the path to listfile.txt(annotation).  
SRC_DATAROOT: Segmetation Result path.  
DST_DATAROOT: A list of the path where copy the segmetation result to. Must be a one-to-one match with LABELFILE_PATH  
FORCE_COPY: If DST_DATAROOT exists, force to replace it.   
**Warning:** Before force copy, do confirm the segmentation results are matching with the annotations. Because we are not sure about every segmetation result is the same, FORCE_COPY may destroy the annotation‘s correctness.

* **Herlev_EDA.ipynb**  
EDA jupyter notebook for Herlev dataset  
* **Sample1_EDA.ipynb**  
EDA jupyter notebook for 2018_10_1 and 2018_12_06 training dataset.  
* **mark_pos.py**  
Read a listfile.txt(annotation), and generate FOVs marked with all the labeled abnormal cells.  
* **json2mask.py**  
Transfer segmentation annotations in json format to mask.png format(like a numpy matrix).  
* **listfile_.txt**  
Annotations with format[['{Image_basename}_output', [abnormal_indexes], [normal_indexes]],...]  
* **gen_listfile**  
Scripts for generate listfile.txt  

* **PipelineRootDir/datasets/gen_test_fov.ipynb**  
Jupyter notebook for select train and test fovs from slides.

* **CLFRootDir/datasets/Tuning_Dataset.ipynb**  
Jupyter notebook for tuning training dataset, for we cann't resegment the fovs and use the result as training data. Use this notebook can keep the consistency between annotations and data.

## Build Training Dataset
* Step0: 如何获得彩点标注的FOV Image：https://pan.baidu.com/play/video#/video?path=%2FCervical_Cells%2F%E6%A0%87%E6%B3%A8%E7%BB%86%E8%83%9E.mp4&t=-1
    color_map = {1: (0, 255, 255), #yellow
             2: (0, 255, 0), #Green
             3: (0, 0, 255), #Red
             5: (255, 255, 0) #cyan
            }
    class_map ={1: 'LSIL', 
                2: 'HSIL',
                3: 'LSIL_HPV',
                5: 'SCC'
            }
* Step1: 准备好用彩色点标注好的FOV image， 将其放到dataset/origin_annotation/batch_of_trainset/下  
* Step2: 将对应的原始FOV image, 放到dataset/origin_train/batch_of_trainset/下  
* Step3: 参考下面Example中'Step2: Run Segmentation Prediction with pipeline'，运行./run.sh step1/step2/step3，生成dataset/classify/*_output/preview/label.png  
* Step4: 修改tools/annot_img_to_file.py中的参数，annot_path='dataset/origin_annotation/batch_of_trainset/', seg_path='dataset/classify'，运行脚本，得到annotation_batch_of_trainset.txt的annotation文件  
* Step5: 修改clf_preproc.py中的LABELFILE_PATH='annotation_batch_of_trainset.txt', SRC_DATAROOT='dataset/classify',  DST_DATAROOT='src/CLASSIFY/inceptionv3_final_1/dataset/classify_batch_of_trainset'，运行clf_preproc.py，生成training需要的csv文件以及数据    

Example:
-

* Build Project from Begining:  
Here is an example of how to build a prediction pipeline from the beginning.  
  * Step1: Train Segmentation Model  
  Refer to 'Run Segmentation Training' part below.  
  * Step2: Run Segmentation Prediction with pipeline
    * Copy data: cp -r /opt/zhuoyao_workspace/github/final_medical_cervix/datasets/original_train/*    \  
            PipelineRootDir/datasets/original_train  
    * vi ./run.sh 
    * modify the ORIGIN_PATH to PipelineDir/datasets/original_train/origin_1* (for batch 1)  
    * ./run.sh step1  
    * ./run.sh step2  
    * ./run.sh step3  
    * Check segmentation result in PipelineRootDir/datasets/Classify/${FOV_basenaem}_output/previews/previews.png & mask.png   
  * Step3: Annotate Segmentation Results  
  Note: Skip this step when use the exist listfile.txt in the project, the corresponding data is in:  
  /opt/zhuoyao_workspace/github/final_medical_cervix/src/CLASSIFY/inceptionV3_final_1/datasets  
    * cd PipelineRootDir/tools/gen_listfile & vi write_listfile.py  
    * modified the annotation of the train data according to Doctor's Label(In Watone Cloud)  
    * python3 write_listfile.py & mv listfile.txt ../  
  * Step4: Generate Input And Data For Classifier  
  Note: In this step, if listfile is not corresponding to segment result, it would be assert Error.  
  If use listfile5.txt, copy  
  '/opt/zhuoyao_workspace/github/final_medical_cervix/src/CLASSIFY/inceptionV3_final_1/datasets/classify_nodenoise_2018' to PipelineRootDir/src/CLASSIFY/inceptionV3_final_1/datasets and DST_DATAROOT must be 'classify_nodenoise_2018'.  
  If use listfile_2019.txt, copy  
  /opt/zhuoyao_workspace/github/final_medical_cervix/src/CLASSIFY/inceptionV3_final_1/datasets/classify_nodenoise_2019  
    * cd ../ & vi clf_preproc.py  
    * modify LABELFILE_PATH and DST_DATAROOT  
    * python3 clf_preproc.py  
  * Step5: Train Classifier  
    * cd PipelineRootDir/src/CLASSIFY/inceptionV3_final_1/  
    * ./run_train_augmenta.sh  
    * Wait until training finished  
    * mkdir weights_bak & mkdir ./weights_bak/1st_batch & cp ./weights/*.hdf5 ./weights_bak/1st_batch  
    * Use result_analysis.ipynb to see the training result  
  * Step6: Do prediction for test FOVs  
    * cd PipelineRootDir 
    * cp -r /opt/zhuoyao_workspace/github/final_medical_cervix/datasets/original_test/*    \  
            PipelineRootDir/datasets/original_test
    * Refer to 'Pipeline Prediction'
  


* Run Segmentation Training:  
Here is an example for running Segmentation training.  
  * cp -r /opt/zhuoyao_workspace/github/final_medical_cervix/datasets/segment/stage1* PipelineRootDir/datasets/segment
  * cd src/SEGMENT/kaggle-dsb2018/src
  * ./run_train.sh c3 pub_1st & ./run_train.sh c3 pub_2st
  * cp ./c3_output/models_colour/{latest_one}.h5 ./all_output/models_colour


Data
-
## Segmentation Cells Test
* Abnormal Cells which cannot be segmented (use it to test your segmentation method and see if it can be segmented):  

It includes 3 fovs (LSIL, HPV, HSIL) which the abnormal cells are not able to be segmented as a cell either because its nuclei is too large (daily in LSIL and HSIL) or other unknown reasons.

The Original_FOVs folder has the original fovs, while the Labeled_by_Pathologist folder has the same fovs which abnormal cells are labeled by pathologist. You can test with Original_FOVs folder and use Labeled_by_Pathologist as a reference.

Please download it from:
https://okcloud.watone.com.cn/index.php/s/XyAL27tsspCRN6T

## Doctor labled 2nd batch slides (As a refernce)

  * LSIL, HSIL, LSIL_HPV, SCC: https://okcloud.watone.com.cn/index.php/s/goeaWgp7pYRA9C6

## Doctor labled 3rd batch slides (As a refernce)
  * LSIL, HSIL, LSIL_HPV: https://okcloud.watone.com.cn/index.php/s/ato72xSQy7F5YFk
  
## Original 2nd batch slides
HSIL：
下载数据：（https://pan.baidu.com/s/1WfsmPeeqen75_oWm2OHqDA）

SCC:
下载数据：（https://pan.baidu.com/s/1kNNvrmO5nyyA5s6i_Q4Wdg）

LSIL:
下载数据：（https://pan.baidu.com/s/1jmWUMdtHWZzKfPjadII9oA）

LSIL+HPV:
下载数据：（https://pan.baidu.com/s/1yhVopfRS5aryTeq-tRsvmQ）

## Original 3rd batch slides
链接: https://pan.baidu.com/s/1wZe-NHUl5gKmrFOZCuT9FQ 提取码: b9nt 

## Original 4th batch slides
1）HSIL：这张片子标注约200个异常细胞
https://pan.baidu.com/s/17t9PbF29lMaHD7GA8qAyew 提取码: s41e 

2）LSIL：这张片子标注约200个异常细胞

https://pan.baidu.com/s/1VQ5B4wfDOrORotd4sujuYw 提取码: egnh 

3）找2张SCC，1张HPV的片子，每张片子标注约200个异常细胞
https://pan.baidu.com/s/1wpeYsEfu2awNbZuh0kB6pQ 提取码: acue

其中3）这个文件夹，因为里面只分了阳性/阴性，没有定标为哪类。所以得从阳性片子里找一下我们需要的片子。

## 50 Test slides from Mr.Hu
Most of them are Negtive. Use them to verify the robustness of our model
链接: https://pan.baidu.com/s/1uvdWNtjftBWP2JBnRGL4Qw 提取码: 3w8z

