## 1 安装依赖
```
$ pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```
## 2 目录结构
```
根目录howtoMala目录下需要存在文件夹：good,bad
testing_cross_domain目录下只允许存在两个文件夹：file_N,file_P
testing_cross_domain
├── file_N
└── file_P
测试模型时将测试数据存放到testing_cross_domain/file_P路径下（每次只能测试一种类型的数据）
默认规定：预测标签1表示阳性，0表示阴性
运行：python test_md.py
运行结果：
预测为阳性细胞数量 30
预测为阴性细胞数量 970
（表示testing_cross_domain/file_P路径下的数据机器预测结果：阳性细胞30个，阴性细胞970个）
```
## 3 Reading Note
*Where is the predict function:
    def _predict(self, result201_200, remove_cnt_201, remove_cnt_200):
    ...
            self.model = load_model(self.projectinfo['modpath'])
    ...
            predIdxs = self.model.predict_generator(testGen_cross_domain,
