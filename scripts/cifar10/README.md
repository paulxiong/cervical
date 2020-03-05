## cifar10 数据自定义创建/解压成图片
### CIFAR-10 Matlab version  (fixmatch使用的)
### CIFAR-10 binary version  (auto-GAN使用的, 只是auto-GAN不能直接用自定义的，自定义之后要修改代码里检查文件的md5sum才能用)
### CIFAR-10 python version

## 1 CIFAR-10 Matlab version
### 1-1 用自定义数据创建
拷贝你的数据到当前目录, 病命名为input
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

## 2 CIFAR-10 binary version
### 脚本没整理完
## 3 CIFAR-10 python version
### 脚本没整理完