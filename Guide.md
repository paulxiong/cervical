1. Configuration  
Check the configuration in ./configure.conf, every path's parameter is configed in the file.  
Paramters in 'model' section:  
'path': GAN model and classifier model path  
'purity', 'entorpy', 'itera': identifications for GAN model  
'clf_ts': identification for classifier model  
2. Environment  
cmd:docker run -d -v `pwd`:/nu_gan --name="nu_gan" --runtime=nvidia tensorflow/tensorflow:1.7.0-gpu-nu_gan sleep 100h -v  
Execute the command above in project root, and take care of the --name parameter with an unique name.
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

