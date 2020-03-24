## cifar10 数据自定义创建/解压成图片
-  1 CIFAR-10 Matlab version  (fixmatch使用的)
-  2 CIFAR-10 python version  (auto-GAN不能直接用自定义的，要修改代码里检查文件md5sum才能用)
-  3 CIFAR-10 binary version

## 1 CIFAR-10 Matlab version
### 1-1 用自定义数据创建
拷贝你的数据到当前目录, 命名为input
```
$ cd cervical.git/scripts/cifar10
$ cp /your/path/input . -a
```

准备如下input目录结构
```
├── batches.meta.mat.empty.mat
├── data_batch_1.mat.empty.mat
├── input
│   ├── 1   #这个是批次的index
│   │   ├── airplane   #类别的名字
│   │   ├── bird
│   │   ├── cat
│   │   ├── deer
│   │   ├── dog
│   │   ├── frog
│   │   ├── horse
│   │   ├── ship
│   │   └── truck
│   ├── 2
│   │   ├── airplane
│   │   ├── ...
│   │
│   ├── 3
│   │   ├── airplane
│   │   ├── ...
│   │
│   ├── 4
│   │   ├── airplane
│   │   ├── ...
│   │
│   ├── 5
│   │   ├── airplane
│   │   ├── ...
│   │
```

```
$ python3 create_matlab.py
```
生成如下目录结构
```
output_create/
├── batches.meta.mat
├── data_batch_1.mat
├── data_batch_2.mat
├── data_batch_3.mat
├── data_batch_4.mat
├── data_batch_5.mat
```

打包成cifar10数据
```
$ rm -rf cifar-10-batches-mat
$ mv output_create cifar-10-batches-mat
$ tar -cmf cifar-10-matlab.tar cifar-10-batches-mat
$ gzip cifar-10-matlab.tar
```
------------------
### 1-2 解压
#### !!解压操作能解压自定义数据，也能解压官网数据。不需要做上面的创建操作就能解压

```
$ cd cervical.git/scripts/cifar10
$ cp  /your/path/cifar-10-matlab.tar.gz .

$ gzip -d cifar-10-matlab.tar.gz
$ tar -xmf cifar-10-matlab.tar
```
得到当前如下目录
```
$ ls -lh
总用量 175M
-rw-rw-r-- 1 lambda lambda  912 3月   1 00:28 batches.meta.mat.empty.mat
drwxr-xr-x 2 lambda lambda 4.0K 3月   1 00:28 cifar-10-batches-mat
-rw-rw-r-- 1 lambda lambda 175M 3月   1 00:28 cifar-10-matlab.tar
-rw-rw-r-- 1 lambda lambda 4.3K 3月   1 00:55 create_matlab.py
-rw-rw-r-- 1 lambda lambda  344 3月   1 00:28 data_batch_1.mat.empty.mat
-rw-rw-r-- 1 lambda lambda  344 3月   1 00:48 test_batch.mat.empty.mat
-rw-rw-r-- 1 lambda lambda 2.6K 3月   1 10:51 untar_matlab.py
```

```
$ python3 untar_matlab.py
{0: 'airplane', 1: 'automobile', 2: 'bird', 3: 'cat', 4: 'deer', 5: 'dog', 6: 'frog', 7: 'horse', 8: 'ship', 9: 'truck'}
untar cifar-10-batches-mat/data_batch_1.mat ...
untar cifar-10-batches-mat/data_batch_2.mat ...
untar cifar-10-batches-mat/data_batch_3.mat ...
untar cifar-10-batches-mat/data_batch_4.mat ...
untar cifar-10-batches-mat/data_batch_5.mat ...
untar cifar-10-batches-mat/test_batch.mat ...
```

得到如下目录
```
$ tree cifar10_untar

cifar10_untar/
├── output       #训练数据集目录
│   ├── 1        #训练数据集批次，data_batch_1.mat生成目录1
│   │   ├── airplane      #类别名称，batches.meta.mat里面存储
│   │   ├── automobile
│   │   ├── bird
│   │   ├── cat
│   │   ├── deer
│   │   ├── dog
│   │   ├── frog
│   │   ├── horse
│   │   ├── ship
│   │   └── truck
│   ├── 2
│   │   ├── airplane
│   │   ├── automobile
│   │   ├── bird
│   │   ├── cat
│   │   ├── deer
│   │   ├── dog
│   │   ├── frog
│   │   ├── horse
│   │   ├── ship
│   │   └── truck
└── output_test
    └── 0       #测试数据集批次，test_batch.mat生成
        ├── airplane
        ├── automobile
        ├── bird
        ├── cat
        ├── deer
        ├── dog
        ├── frog
        ├── horse
        ├── ship
        └── truck
```

## 2 CIFAR-10 python version
### 2-1 解压
拷贝你的数据到当前目录, 命名为input
```
$ cd cervical.git/scripts/cifar10
$ cp /your/path/cifar-10-python.tar.gz  .

$ gzip -d cifar-10-python.tar.gz
$ tar -xmf cifar-10-python.tar
```
得到如下文件
```
 ls -lh
总用量 178M
-rw-rw-r-- 1 lambda lambda  912 3月   6 09:27 batches.meta.mat.empty.mat
drwxr-xr-x 2 lambda lambda 4.0K 3月   6 12:16 cifar-10-batches-py
-rw-rw-r-- 1 lambda lambda 178M 3月   6 12:13 cifar-10-python.tar
-rw-rw-r-- 1 lambda lambda 4.3K 3月   6 09:27 create_matlab.py
-rw-rw-r-- 1 lambda lambda 1.5K 3月   6 09:29 create_python.py
-rw-rw-r-- 1 lambda lambda  344 3月   6 09:27 data_batch_1.mat.empty.mat
-rw-rw-r-- 1 lambda lambda 4.5K 3月   6 12:16 README.md
-rw-rw-r-- 1 lambda lambda  344 3月   6 09:27 test_batch.mat.empty.mat
-rw-rw-r-- 1 lambda lambda 2.6K 3月   6 09:27 untar_matlab.py
-rw-rw-r-- 1 lambda lambda  651 3月   6 09:29 untar_python.py



$ ls cifar-10-batches-py/ -l
总用量 181876
-rw-r--r-- 1 lambda lambda      158 3月   6 12:16 batches.meta
-rw-r--r-- 1 lambda lambda 31035704 3月   6 12:16 data_batch_1
-rw-r--r-- 1 lambda lambda 31035320 3月   6 12:16 data_batch_2
-rw-r--r-- 1 lambda lambda 31035999 3月   6 12:16 data_batch_3
-rw-r--r-- 1 lambda lambda 31035696 3月   6 12:16 data_batch_4
-rw-r--r-- 1 lambda lambda 31035623 3月   6 12:16 data_batch_5
-rw-r--r-- 1 lambda lambda       88 3月   6 12:16 readme.html
-rw-r--r-- 1 lambda lambda 31035526 3月   6 12:16 test_batch
```

安装依赖
```
pip3 install Pillow -i https://pypi.tuna.tsinghua.edu.cn/simple
```

执行解压命令
```
$ python3 untar_python.py 
```

得到如下目录
```
$ tree -d python_untar/
python_untar/
├── 1
│   ├── airplane
│   │   ├── xx.png
│   │   ├── ...
│   ├── ...
│
├── 2
│   ├── airplane
│   │   ├── xx.png
│   │   ├── ...
│   ├── ...
│
├── 3
│   ├── airplane
│   │   ├── xx.png
│   │   ├── ...
│   ├── ...
│
├── 4
│   ├── airplane
│   │   ├── xx.png
│   │   ├── ...
│   ├── ...
│
├── 5
│   ├── airplane
│   │   ├── xx.png
│   │   ├── ...
│   ├── ...
│
└── test
    ├── airplane
│   │   ├── xx.png
│   │   ├── ...
    ├── ...

```

### 2-1 自定义数据创建
拷贝自定义数据到当前文件夹
```
$ cd cervical.git/scripts/cifar10
$ cp /your/path/input  .
```

input的目录结构如下
```
$ tree -d input/
input/
├── 1
│   ├── airplane
│   │   ├── xx.png
│   │   ├── ...
│   │
│   └── automobile
│       ├── xx.png
│       ├── ...
├── 2
│   ├── airplane
│   │   ├── xx.png
│   │   ├── ...
│   │
│   └── automobile
│       ├── xx.png
│       ├── ...
├── 3
│   ├── airplane
│   │   ├── xx.png
│   │   ├── ...
│   │
│   └── automobile
│       ├── xx.png
│       ├── ...
├── 4
│   ├── airplane
│   │   ├── xx.png
│   │   ├── ...
│   │
│   └── automobile
│       ├── xx.png
│       ├── ...
├── 5
│   ├── airplane
│   │   ├── xx.png
│   │   ├── ...
│   │
│   └── automobile
│       ├── xx.png
│       ├── ...
└── test
    ├── airplane
    │   ├── xx.png
    │   ├── ...
    │
    └── automobile
        ├── xx.png
        ├── ...
```

开始创建
```
$ python3 create_python.py
```

生成如下目录
```
$ ls python_tar -lh
total 36M
-rw-r--r-- 1 lambda lambda  109 Mar  6 05:38 batches.meta
-rw-r--r-- 1 lambda lambda 5.9M Mar  6 05:38 data_batch_1
-rw-r--r-- 1 lambda lambda 5.9M Mar  6 05:38 data_batch_2
-rw-r--r-- 1 lambda lambda 5.9M Mar  6 05:38 data_batch_3
-rw-r--r-- 1 lambda lambda 5.9M Mar  6 05:38 data_batch_4
-rw-r--r-- 1 lambda lambda 5.9M Mar  6 05:38 data_batch_5
-rw-r--r-- 1 lambda lambda 5.9M Mar  6 05:38 test_batch
```

创建压缩包
```
$ rm -rf cifar-10-batches-py
$ mv python_tar cifar-10-batches-py
$ tar -cmf cifar-10-python.tar cifar-10-batches-py
$ gzip cifar-10-python.tar
```

## 3 CIFAR-10 binary version
### 3-1 解压
拷贝数据到当前目录
```
$ cd cervical.git/scripts/cifar10
$ cp /your/path/cifar-10-binary.tar.gz  .

$ tar -zxmf cifar-10-binary.tar.gz
```
得到如下文件
```
$ ls cifar-10-batches-bin/ -lh
总用量 176M
-rw-r--r-- 1 lambda lambda  61 3月  24 16:18 batches.meta.txt
-rw-r--r-- 1 lambda lambda 30M 3月  24 16:18 data_batch_1.bin
-rw-r--r-- 1 lambda lambda 30M 3月  24 16:18 data_batch_2.bin
-rw-r--r-- 1 lambda lambda 30M 3月  24 16:18 data_batch_3.bin
-rw-r--r-- 1 lambda lambda 30M 3月  24 16:18 data_batch_4.bin
-rw-r--r-- 1 lambda lambda 30M 3月  24 16:18 data_batch_5.bin
-rw-r--r-- 1 lambda lambda  88 3月  24 16:18 readme.html
-rw-r--r-- 1 lambda lambda 30M 3月  24 16:18 test_batch.bin
```

执行解压命令
```
$ python3 untar_binary.py
```

解压之后的目录结构如下
```
$ tree  binary_untar/
binary_untar/
├── 1
│   ├── airplane
│   │   ├── 1.png
│   │   ├── ...
│   ├── automobile
│   ├── bird
│   ├── cat
│   ├── deer
│   ├── dog
│   ├── frog
│   ├── horse
│   ├── ship
│   └── truck
├── 2
│   ...
├── 3
│   ...
├── 4
│   ...
├── 5
│   ...
│
└── test
    ├── airplane
    │   ├── 1.png
    │   ├── ...
    ├── automobile
    ├── bird
    ├── cat
```


### 3-2 自定义数据创建
拷贝自定义数据到当前文件夹
```
$ cd cervical.git/scripts/cifar10
$ cp /your/path/input  .
```

input的目录结构如下
```
$ tree -d input/
input/
├── 1
│   ├── airplane
│   │   ├── xx.png
│   │   ├── ...
│   │
│   └── automobile
│       ├── xx.png
│       ├── ...
├── 2
│   ├── airplane
│   │   ├── xx.png
│   │   ├── ...
│   │
│   └── automobile
│       ├── xx.png
│       ├── ...
├── 3
│   ├── airplane
│   │   ├── xx.png
│   │   ├── ...
│   │
│   └── automobile
│       ├── xx.png
│       ├── ...
├── 4
│   ├── airplane
│   │   ├── xx.png
│   │   ├── ...
│   │
│   └── automobile
│       ├── xx.png
│       ├── ...
├── 5
│   ├── airplane
│   │   ├── xx.png
│   │   ├── ...
│   │
│   └── automobile
│       ├── xx.png
│       ├── ...
└── test
    ├── airplane
    │   ├── xx.png
    │   ├── ...
    │
    └── automobile
        ├── xx.png
        ├── ...
```

开始创建
```
$ python3 create_binary.py
```

生成如下目录
```
$ ls binary_tar/ -lh
总用量 44M
-rw-rw-r-- 1 lambda lambda   60 3月  24 19:01 batches.meta.txt
-rw-rw-r-- 1 lambda lambda 3.0M 3月  24 19:02 data_batch_1.bin
-rw-rw-r-- 1 lambda lambda 3.0M 3月  24 19:02 data_batch_2.bin
-rw-rw-r-- 1 lambda lambda 3.0M 3月  24 19:02 data_batch_3.bin
-rw-rw-r-- 1 lambda lambda 3.0M 3月  24 19:02 data_batch_4.bin
-rw-rw-r-- 1 lambda lambda 3.0M 3月  24 19:02 data_batch_5.bin
-rw-rw-r-- 1 lambda lambda  30M 3月  24 19:03 test_batch.bin
```

创建压缩包
```
$ rm -rf cifar-10-batches-bin
$ mv binary_tar cifar-10-batches-bin
$ tar -cmf cifar-10-binary.tar cifar-10-batches-bin
$ gzip cifar-10-binary.tar
```
