### clone from https://github.com/timsainb/Tensorflow-MultiGPU-VAE-GAN

### ipynb to py

### datasets
```
进入项目目录
# cd //notebooks/cervical/Tensorflow-MultiGPU-VAE-GAN/
创建模型存放目录
# mkdir datasets
创建存放原始数据集目录
# mkdir data_org
创建存放resize数据目录
# mkdir data_resize
创建存放生成数据目录
# mkdir imgs
把原始数据拷贝到data_org
# tree ./data_org
- 17P060320197261904165BIMG010x002.JPG_n_1_1168_876_1268_976.png
|-- 17P060320197261904165BIMG010x002.JPG_n_1_1299_559_1399_659.png
|-- 17P060320197261904165BIMG010x002.JPG_n_1_1384_627_1484_727.png
... ...
生成h5文件
# python celeba_make_dataset.py
# tree ./datasets
- faces_dataset_new.h5
```
### train
```
# python VAE-GAN-multi-gpu-celebA.py
```
### run
