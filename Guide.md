1. Configuration  
Check the configuration in ./configure.conf, every path's parameter is configed in the file.  
Paramters in 'model' section:  
'path': GAN model and classifier model path  
'purity', 'entorpy', 'itera': identifications for GAN model when doing prediction  
'clf_ts': identification for classifier model when doing prediction  
2. Environment  
cmd1:docker run -d -v ``pwd``:/nu_gan -v /opt/zhuoyao_workspace/github/cervical/experiment:/nu_gan/experiment  --name="nu_gan" --runtime=nvidia tensorflow/tensorflow:1.7.0-gpu-nu_gan sleep 100h     
Execute the command above in project root, and take care of the --name parameter with an unique name.  
And be ware to link the train and test dataset to the nu_gan folder.  
cmd2:docker exec -it nu_gan bash  
Enter the "nu_gan" docker execute environment.  
run CMD in docker env: pip install tensorboardX
3. Segmentation  
cmd: python nu_gan.py --task 'cell_segmentation'  
This command will segment the images in 'train_path_n' and 'train_path_p', the results are stored in 'train_npy_path_n' and 'train_npy_path_p'  
4. GAN Training and Image Classification  
cmd: python nu_gan.py --task 'image_classification'  
This command will train the nu_gan with the experiment/data/cell_level_label labeled segmented cells,   
and train a svm to do classification the images in 'train_path_p' and 'train_path_n' with the segmentation in 'train_npy_path_n' and 'train_npy_path_p'  
5. Image Classifier Training  
cmd: python nu_gan.py --task 'image image_classification_predict'  
This command will train the svm classifier with the images in in 'train_path_p' and 'train_path_n' with the segmentation in 'train_npy_path_n' and 'train_npy_path_p'  
And evaluate the result with the images in 'test_path_n' and 'test_path_p' with the segmentation in 'test_npy_path_n' and 'test_npy_path_p'.  
After predict, the program will ask for whether to archive the train and test dataset and model, and if yes the script will store 
the data in the 'store_path' and record the informations and the score results in the csv file in 'db_path'.  
6. Image Prediction  
cmd: python nu_gan.py --task 'image image_classification_predict'  
This command will predict the images in 'test_path_n' and 'test_path_p' with the segmentation in 'test_npy_path_n' and 'test_npy_path_p'.  
If the images are less than 100, the result will print in the screen, and greater than 100, the result will store in ./positive_res.csv & ./negative_res.csv  
6. Recheck the previous result  
cat db.csv or open db.csv in python with pandas and do the search  

Training Debug with TensorBoard:  
1. Prepare Data  
Make a dir named 'experiment' in the 'nu_gan' folder, copy the train(positive_images & negative_images) and test (positive_test_images and negative_test_images) datasets to experiment/data/original, copy the segmentation results to the experiment/data/segmented.  
(REFERENCE: https://github.com/paulxiong/cervical/issues/1)  
2. Prepare Environment  
cmd1:docker run -d -v ``pwd``:/nu_gan --name="nu_gan" --runtime=nvidia tensorflow/tensorflow:1.7.0-gpu-nu_gan sleep 100h     
Execute the command above in project root, and take care of the --name parameter with an unique name.  
And be ware to link the train and test dataset to the nu_gan folder.   
cmd2:docker exec -it nu_gan bash   
Enter the "nu_gan" docker execute environment.  
3. Start Training  
Follow 4th steps above.  
4. Start TensorBoard  
NOTICE: DO NOT run tensorboard in docker, run in the original environment.  
The visualization data is stored in ./runs. Start tensorboard with command:  
tensorboard --logdir ./runs --port=xxxx   
Port selection (Method 1): choose 9000-9010, refer to https://github.com/paulxiong/cervical/blob/master/GPU%20%E6%9C%8D%E5%8A%A1%E5%99%A8%E7%AB%AF%E5%8F%A3%E6%98%A0%E5%B0%84%E8%A1%A8  
Port selection (Method 2): choose an unused port, like 6006, and use cmd "ssh -i .ssh/jps-atec.key -t atec@115.236.22.146 -L 127.0.0.1:6006:127.0.0.1:6006 "ssh 172.16.1.99 -L 127.0.0.1:6006:172.16.1.99:6006"" to set a proxy to the localhost:6006. Use http://localhost:6006 to check the result.

