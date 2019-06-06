1.准备模型：   
第一步，进入nu_gan根目录： cd /opt/xxx_workspace/nu_gan  

第二步，拷贝模型：sudo cp -r /opt/zhuoyao_workspace/nu_gan/experiment/1559022992 ./experiment

第三步，更新configure.conf文件：git pull

2.进入docker环境：  
第一步，启动docker： 
run -d -v \`pwd\`:/nu_gan --name="xxxx" --runtime=nvidia tensorflow/tensorflow:1.7.0-gpu-nu_gan sleep 100h     
注意：修改命令中的xxxx为你想要的名称  
  
第二步，进入docker命令环境：  
docker exec -it nu_gan bash    

第三步，安装tensorboardX软件包:  
pip install tensorboardX  

3. 准备数据：  
按照https://github.com/paulxiong/cervical/blob/nu_gan_archive/segmentation/SEG%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E.txt  
准备好训练和测试数据。  
  
4. 训练NU_GAN模型：    
命令:   
python nu_gan.py --task 'image_classification'  
This command will train the nu_gan with the experiment/data/cell_level_label labeled segmented cells,   
and train a svm to do classification the images in 'train_path_p' and 'train_path_n' with the segmentation in 'train_npy_path_n' and 'train_npy_path_p'  
  
5. 训练NU_GAN FOV识别器：    
命令:   
python nu_gan.py --task 'image_classification_train'    
  
6. FOV预测：    
命令:  
python nu_gan.py --task 'image_classification_predict'   

