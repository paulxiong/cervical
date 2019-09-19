### clone from https://github.com/timsainb/Tensorflow-MultiGPU-VAE-GAN

### ipynb to py

### datasets
```
docker地址&密码:
http://2j592d3300.wicp.vip:8888/terminals/2
223a00e2eb47dc78412c618a55916aefaea195f4f8ac07d7
进入项目目录:
# cd //notebooks/cervical/Tensorflow-MultiGPU-VAE-GAN/
清理h5模型存放的目录:
# rm datasets/*
清理存放原始数据集的目录:
# rm data_org/*
清理存放resize数据的目录:
# rm data_resize/*
清理存放观测数据的目录:
# rm imgs/*
清理存放生成细胞图的目录:
# rm fake/*
上传压缩包至当前目录，并解压：unzip abc***.zip
将目标数据拷贝到data_org :cp abc***/* data_org
检查data_org目录:
# tree ./data_org
- 17P060320197261904165BIMG010x002.JPG_n_1_1168_876_1268_976.png
|-- 17P060320197261904165BIMG010x002.JPG_n_1_1299_559_1399_659.png
|-- 17P060320197261904165BIMG010x002.JPG_n_1_1384_627_1484_727.png
... ...
生成h5文件:
# python celeba_make_dataset.py
检查datasets目录:
# tree ./datasets
- faces_dataset_new.h5
```
### train
```
# python VAE-GAN-multi-gpu-celebA.py
```
### run
```
# python fake.py
```
### save data and models!!!(重要)
```
保存生成细胞：
# zip -r fake_***.zip fake/（如：zip -r fake_17P_type1.zip fake/）
再将压缩好的zip文件下载到本地保存
保存生成模型：
将文件夹models下的三个模型文件rename，追加统一后缀名（如:faces_multiGPU_64_0001.tfmod.meta_17P_type1）
faces_multiGPU_64_0001.tfmod.data-00000-of-00001
faces_multiGPU_64_0001.tfmod.index
faces_multiGPU_64_0001.tfmod.meta
```