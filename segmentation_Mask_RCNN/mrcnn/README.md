
1、maskrcnn检测不同尺寸fov速度和精度对比

| fov尺寸   | fov数量 | 检测时间 | 检测到的总细胞数目 | 检测到的真是细胞 | 检测到的错误细胞（细胞浆）、黑色粒子等 |
|-----------|---------|----------|--------------------|------------------|----------------------------------------|
| 1936x1216 | 50      | 1153.91s | 4821               | 4530             | 291                                    |
| 968x608   | 50      | 275.39s  | 3604               | 3559             | 45                                     |

生成的对比图片如下，随机选了两张背景不同的fov图；其中红色框为原图片尺寸检测到的细胞情况，绿色框为缩小一半尺寸后细胞的检测情况。
![image](https://github.com/paulxiong/cervical/blob/master/segmentation_Mask_RCNN/mrcnn/images/IMG002x014.JPG_.png_.png)

![image](https://github.com/paulxiong/cervical/blob/master/segmentation_Mask_RCNN/mrcnn/images/IMG002x017.JPG_.png_.png)

2、无细胞fov和有细胞fov速度对比（有细胞的fov，每张的细胞数目大致在150个细胞左右）

| fov类型   | fov数量 | 总共用时 | 每张fov平均用时 |
|-----------|---------|----------|-----------------|
| 无细胞fov | 40      | 31.36s   | 0.33s           |
| 有细胞fov | 40      | 447.12s  | 10s             |

3、彩色图像和黑白图像检测对比；
  这是彩色图片的检测结果，因为受颜色的影响，部分染色较深的细胞浆被识别成细胞核。
  ![image](https://github.com/paulxiong/cervical/blob/master/segmentation_Mask_RCNN/mrcnn/images/redhouse2019661817144IMG053x021.JPG1_.png)
  
  灰度化后的检测图像如下，混度化后剔除了颜色带来的干扰，检测结果更加好，没得把细胞浆检测为细胞核。
  ![image](https://github.com/paulxiong/cervical/blob/master/segmentation_Mask_RCNN/mrcnn/images/redhouse2019661817144IMG053x021.JPG_.png)
