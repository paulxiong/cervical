## 常用脚本整理

### 1 医生标注的CSV转换成 PASCALVOC VOC2007 数据集的格式
安装依赖
```
$ pip3 install xmltodict -i https://pypi.tuna.tsinghua.edu.cn/simple

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
└── redhouse.1817144.IMG053x021.xml
└── redhouse.1817144.IMG053x021.csv
```