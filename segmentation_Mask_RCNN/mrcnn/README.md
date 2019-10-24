
1、运行环境
```
（1）、单个tesla-v100 gpu。

（2）、环境搭建。
 tensorflow-gpu==1.3.0
 cuda==8.0
 python=3.5.2

 pip install numpy==1.17.0 -i https://pypi.tuna.tsinghua.edu.cn/simple 
 pip install keras==2.0.8 -i https://pypi.tuna.tsinghua.edu.cn/simple
 pip install scikit-image==0.15.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
 pip install imgaug==0.2.9 -i https://pypi.tuna.tsinghua.edu.cn/simple
 pip install utils==0.9.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
 pip install opencv-python==4.1.0.25 -i https://pypi.tuna.tsinghua.edu.cn/simple
 pip install h5py==2.7.0  -i https://pypi.tuna.tsinghua.edu.cn/simple
 pip install matplotlib  -i https://pypi.tuna.tsinghua.edu.cn/simple
 pip install scipy==0.19.1  -i https://pypi.tuna.tsinghua.edu.cn/simple
 pip install Pillow==6.1.0  -i https://pypi.tuna.tsinghua.edu.cn/simple
 pip install sklearn==0.19.0  -i https://pypi.tuna.tsinghua.edu.cn/simple
 pip install ipython==6.1.0   -i https://pypi.tuna.tsinghua.edu.cn/simple
```     

2、运行代码

 (1) 测试代码版本：commit d284e46e33a076308491b8be636dc85ab5d7207a
  

（2）、组织输入目录：
```
     有标记csv的目录结构：
     -- origin_imgs
            |-- IMG002x009.JPG
            |-- IMG002x009.csv
                    .....
                    .....
            |-- IMG003x019.JPG
            |-- IMG003x019.csv

     没有标记csv的目录结构：
     -- origin_imgs
            |-- IMG002x009.JPG
                    .....
                    .....
            |-- IMG003x019.JPG
```        
（4）、查看模型；
```
    -- model
      └── deepretina_final.h5 
```     
   如果没有模型，模型下载地址为： https://drive.google.com/file/d/19kVton20JL9u0CpwGssD7EbBvsWcq1ty/view?usp=sharing   
    
（5）、运行代码；
```
    python my_inference.py

```


3、查看结果

（1）、生成的细胞目录
```
  在cells/crop目录下生成切割好的细胞图：
  --cells
     |--crop
        |--400P_thirteen_1800952_IMG022X023.jpg_P_5_1485_1498_1585_1598.png
                          ...........
                          ...........
        ├--400P_thirteen_1800952_IMG022X023.jpg_P_5_1592_1621_1692_1721.png
```
（2）、针对不同的fov背景复杂度、染色深度、在output_image下生成fov标记图片。
       做如下直观展示，展示地址为：https://github.com/paulxiong/cervical/issues/13


4、maskrcnn检测不同尺寸fov速度和精度对比

(1)、fov缩小两倍之后的精度速度对比。

| fov尺寸   | fov数量 | 检测时间 | 检测到的总细胞数目 | 检测到的真是细胞 | 检测到的错误细胞（细胞浆）、黑色粒子等 |
|-----------|---------|----------|--------------------|------------------|----------------------------------------|
| 1936x1216 | 50      | 1153.91s | 4821               | 4530             | 291                                    |
| 968x608   | 50      | 275.39s  | 3604               | 3559             | 45                                     |
```
```
生成的fov对比图片在https://github.com/paulxiong/cervical/issues/13 中第六点有展示。
```
```
(2)、无细胞fov和有细胞fov速度对比（有细胞的fov，每张的细胞数目大致在150个细胞左右）

| fov类型   | fov数量 | 总共用时 | 每张fov平均用时 |
|-----------|---------|----------|-----------------|
| 无细胞fov | 40      | 31.36s   | 0.33s           |
| 有细胞fov | 40      | 447.12s  | 10s             |
```
```
5、彩色图像和黑白图像检测对比；

  彩色图片的检测结果因为受颜色的影响，部分染色较深的细胞浆被识别成细胞核。 
  
  灰度化后剔除了颜色带来的干扰，检测结果更加好，没有把细胞浆检测为细胞核。
  
  彩色和灰度化后的图像检测结果展示链接为 https://github.com/paulxiong/cervical/issues/13 中的第七点。
