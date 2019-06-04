1.Prepare Data:  
For generate training dataset, we need to prepare the FOV images (JPG or png) with .csv annotation files.  
The folder structure is : "$DATAROOT/$SLIDE_NAME/*.JPG(or .png)" and "$DATAROOT/$SLIDE_NAME/*.csv"   
For generate testing dataset, we only need FOV images.  
The folder structure is : "$DATAROOT/$SLIDE_NAME/*.JPG(or .png)"  
e.g. you can create a soft link of /opt/zhuoyao_workspace/medical_ai/datasets/ to ./dataset,   
reference to the ./dataset/test_slide folder.  

2.Do Segmentation:  
Prepare U-net weights:  
ln -s /opt/zhuoyao_workspace/medical_ai/src/SEGMENT/kaggle-dsb2018/src/all_output/ ./src/SEGMENT/kaggle-dsb2018/src  
  
cmd: ./run_annotation.sh step1 && ./run_annotation.sh step2 && ./run_annotation.sh step3  
In this step, we will segment the FOV into cells.   
  
Output: ./datasets/classify  
1) Previews: ${SLIDE_NAME}_${FOV_NAME}_output/preview/preview.png    
Review the FOV with segmented crops in FOV level.  
  
2) Cells: ${SLIDE_NAME}_${FOV_NAME}_output/crops or npy/${SLIDE_NAME}_${FOV_NAME}_seg.png  
Review the segmented cells.  
  
3) FOV npy file: npy/${SLIDE_NAME}_${FOV_NAME}.npy  
Npy file of FOV for train and test the svm in nu_gan.   
Copy the .npy files to  $NU_GAN/experiment/data/segmented/negative_(test_)npy(or positive_(test_)npy)/160  
  
4) Slide npy file: slide_npy/${SLIDE_NAME}.npy  
Npy file of slide for train and test the svm in nu_gan.  
Copy the .npy files to  $NU_GAN/experiment/data/segmented/negative_(test_)npy(or positive_(test_)npy)/160  

3.Do Annotation:  
cmd: ./run_annotation.sh step4  
In this step, we will map the annotation csv file to the segmented cells.  
  
Output:  
1) Annotation.txt: ./datasets/classify/annot_out, the mapping of cells and annotation.  
2) origin_mark: ./origin_mark. Mark the annotation to the original FOV for debugging.   

4.Generate annotated train dataset.  
cmd: ./run_annotation.sh step5  
In this step, we will generate train dataset with annotation.  
  
Output: ./dataset/classify/train_datasets  
1) dataset: The cell crop images sorted in diagnostic types, and divided into train and test set   
(if step5 set --train_test_split in run_annotation.sh)  
  
2) npy: The npy file of train and test set X, with the label Y. This is for training the gan part in nu_gan.  
Copy the .npy files to $NU_GAN/experiment/data/cell_level_label  
 



