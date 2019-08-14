## 1 编译docker image
```
$ ./1_build_docker_image.sh
```
## 2 启动docker image
88xx 换成你自己的端口，yourname换成你自己的名字，   --gpus '"device=3"' 的3 换成你自己使用的gpu的id
### ！！！ 注意autokeras自动支持多GPU， 比如--gpus '"device=0,1,2,3"'就是同时使用4个GPU
```
$ docker run -d --name='autokeras-yourname-gpu3' \
    -p 88xx:8888 \
    -v /opt/workspace/yourname:/tf/yourname \
    --gpus '"device=3"' \
    --log-opt max-size=10m \
    cervical_autokeras:20190814
```

## 3 组织训练的目录结构
```
data/
└── task1
    ├── test
    │   ├── 1
    │   │   ├── 17P0603_1903610_IMG026x023.jpg_939_309_50.png
    │   │   ├── ...
    │   │   └── 17P0603_1904746A_IMG025x003.JPG_528_783.png
    │   └── 7
    │       ├── 17P0603_1903610_IMG026x023.jpg_939_309_50.png
    │       ├── ...
    │       └── 17P0603_1904746A_IMG025x003.JPG_528_783.png
    └── train
        ├── 1
        │   ├── 17P0603_1903610_IMG026x023.jpg_939_309_50.png
        │   ├── ...
        │   └── 17P0603_1904746A_IMG025x003.JPG_528_783.png
        └── 7
            ├── 17P0603_1903610_IMG026x023.jpg_939_309_50.png
            ├── ...
            └── 17P0603_1904746A_IMG025x003.JPG_528_783.png
```

## 4 开始训练
在浏览器打开  http://2j592d3300.wicp.vip:88xx/terminals/1， 输入token, 进入终端后，输入
```
# bash
```
data/task1/ 是你准备的训练数据的目录
```
# python main.py --task train --taskdir data/task1/
```

## 5 组织预测的目录结构
```
data/
└── task1
    ├── test
    │   ├── 1
    │   └── 7
    ├── train
    │   ├── 1
    │   └── 7
    └── predict
        ├── 1
        │   ├── 17P0603_1903610_IMG026x023.jpg_939_309_50.png
        │   ├── ...
        │   └── 17P0603_1904746A_IMG025x003.JPG_528_783.png
        └── 7
            ├── 17P0603_1903610_IMG026x023.jpg_939_309_50.png
            ├── ...
            └── 17P0603_1904746A_IMG025x003.JPG_528_783.png
```

## 6 开始预测
```
# python main.py --task predict --taskdir data/task1/
```
