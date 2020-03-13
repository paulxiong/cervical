## 常用脚本整理

### 1 医生标注的CSV转换成 PASCALVOC VOC2007 数据集的格式
安装依赖
```
$ pip3 install xmltodict pandas -i https://pypi.tuna.tsinghua.edu.cn/simple

$ sudo apt-get install libsm-dev libxrender-dev libxext-dev
$ pip3 install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple
```

运行
```
$ python3 csv2xml.py
```

目录结构准备
```
all1010
├── 17P0603.1903779.IMG003x023.JPG
├── 17P0603.1903779.IMG003x023.csv
├── 17P0603.1903779.IMG005x016.JPG
├── 17P0603.1903779.IMG005x016.csv
├── redhouse.1817144.IMG053x021.JPG
└── redhouse.1817144.IMG053x021.csv
```

结果
```
all1010
├── 17P0603.1903779.IMG003x023.JPG
├── 17P0603.1903779.IMG003x023.xml
├── 17P0603.1903779.IMG003x023.csv
├── 17P0603.1903779.IMG005x016.JPG
├── 17P0603.1903779.IMG005x016.xml
├── 17P0603.1903779.IMG005x016.csv
├── redhouse.1817144.IMG053x021.JPG
├── redhouse.1817144.IMG053x021.xml
└── redhouse.1817144.IMG053x021.csv
```

### 2 PASCALVOC VOC2007 数据集里面切出正方形的图片来
```
$ python3 cropxml.py
```

### 3 通过细胞核尺寸过滤掉阴性细胞(测试使用)
先从页面上下载阳性细胞的zip文件，解压到当前文件夹，得到目录结果如下：
```
├── kernelsizefilter.py
│
├── cell-4046-51-160242
│   ├── 51
│   │   ├── 1.png
│   └── csv
│
├── cell-4047-51-121862
│   ├── 51
│   │   ├── 1.png
│   └── csv

```

```
$ python3 kernelsizefilter.py > result.csv
```


```
$ cat result.csv
pid,all,valied
4046,36,1
4047,12,4
4048,17,6
4049,2,0
4050,44,33
4051,26,9
4052,21,3
4053,3,0
4054,11,5
4055,4,1
4056,11,4
4057,9,1
4058,4,1
4059,30,8
4060,4,0
4061,2,0
4062,78,22
4063,5,0
4064,78,22
4066,5,1
```

按照丢弃和留下的细胞分类的目录如下
```
└── result
    ├── remove
    │   ├── 4046
    │       ├── 1.png
    │
    └── valied
        ├── 4046
    │       ├── 1.png

```
