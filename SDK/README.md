#### 1 简介
每个后台的数据处理/训练/预测进程是一个worker，SDK提供一个worker实例的基本配置、常用函数、向后端请求任务、统计系统状态的方法。
SDK提供的是框架，改变算法或者处理流程，SDK不需要改变。

#### 2 数据约定
数据目录
```
├── csv    存放医生标注的csv，有数据库的情况这个目录没用，信息都在数据库里面
│   └── 17P0603
│       ├── 2019-7-22
│       │   ├── 1904165A
│       │   │   ├── IMG001x008.csv
│
├── img   存放原图
│   └── 17P0603
│       ├── 1904165A
│       │   ├── Images
│       │   │   ├── IMG001x008.JPG
│
├── scratch
│   ├── 17P0603  #切割的缓存
│   │   ├── 1904165A
│   │   │   ├── cells
│   │   │   │   ├── IMG001x008.JPG
│   │
│   ├── data       这个表示这里存的是数据
│   │   ├── img2   存放用户通过web上传的图片
│   │   │   └── cells
│   │   │       ├── 批次         如果是用户上传的，批次就是时间+用户id
│   │   │       │   ├── 病例_x_y_w_h_color_slid_csv_mod.png
│
├── datasets           这个和数据库的datasets概念一致, 只存放了一个文件列表及说明
│   ├── DkxD9Kjl   workdir
│   │   ├── info.json    数据集的描述文件
│   │   ├── filelist.csv 前端需要用到的datasets的原图列表
│   │   ├── cells
│   │   │   ├── crop
│   │   │   ├── crop_masked
│   │   │   ├── statistics
│
├── projects          每新建一个项目，对应的文件系统产生一个这个目录
│   ├── qXTqpz6P
│   │   ├── info.json    前端传来的参数
│   │   ├── lists.json   前端需要用到的datasets的列表, 包括带缓存的和不带缓存的, 不带缓存的裁剪完之后更新进来
│   │   ├── train.json   训练的参数、状态、结果
│   │   ├── predict.json 预测的参数、状态、结果
```

文件命名约定
```
TODO
```

#### 3 参数
<table class="tg">
  <tr>
    <th class="tg-0pky">任务类型</th>
    <th class="tg-0pky">参数名</th>
    <th class="tg-0pky">参数说明</th>
  </tr>
  <tr>
    <td class="tg-lboi" rowspan="5">数据处理</td>
    <td class="tg-0pky">gray</td>
    <td class="tg-0pky">默认True使用灰色，False使用彩色</td>
  </tr>
  <tr>
    <td class="tg-0pky">size</td>
    <td class="tg-0pky">切割的正方形边长，默认100</td>
  </tr>
  <tr>
    <td class="tg-0pky">type</td>
    <td class="tg-0pky">0--图片直接检测并切割出细胞 1--按照标注csv切割细胞 2--mask-rcnn检测细胞和csv交集的切割</td>
  </tr>
  <tr>
    <td class="tg-0pky">mid</td>
    <td class="tg-0pky">模型文件的id</td>
  </tr>
  <tr>
    <td class="tg-0lax">cache</td>
    <td class="tg-0lax">是否使用裁剪过的cache</td>
  </tr>
  <tr>
    <td class="tg-0pky">训练</td>
    <td class="tg-0pky"></td>
    <td class="tg-0pky"></td>
  </tr>
  <tr>
    <td class="tg-0pky">预测</td>
    <td class="tg-0pky"></td>
    <td class="tg-0pky"></td>
  </tr>
</table>
