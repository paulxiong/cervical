### data_org_0918
```
链接：https://pan.baidu.com/s/1R31QW5fER0s7Bn7FIQDWMw
提取玛：d9vr
说明：尺寸100*100，人工筛选过的原始细胞数据，9月17日以前的测试都基于此数据
目录结构：
data_org_0918/
├── invalid #无效原始细胞图
│   ├── 17P0603
│   │   ├── ...
├── invalid_masked #无效原始细胞掩码图
│       ├── ...
├── valid #有效原始细胞图
│       ├── ...
├── valid_gray #有效原始细胞灰度图
│       ├── ...
├── valid_gray_rotate #有效原始细胞灰度反转图
│       ├── ...
└── valid_masked #有效原始细胞掩码图
        ├── ...
```
### data_seg0918
```
链接：https://pan.baidu.com/s/1jWjkjyoinYN0x6_RiFClZQ
提取玛：zi7j
说明：尺寸100*100，基于data_org_0918数据，将所有批次的细胞1和7类型，按细胞颜色/是否多核/尺寸完成分类
目录结构：
data_seg0918/
├── data_17P_seg
│   ├── org_color
│   │   ├── blue #细胞图背景呈蓝色
│   │   │   ├── ...
│   │   └── unblue #细胞图背景不呈蓝色
│   │       ├── ...
│   ├── org_num
│   │   ├── one #细胞图中只有一个细胞核
│   │   │   ├── ...
│   │   └── unone #细胞图中有多个细胞核
│   │       ├── ...
│   └── org_size
│       ├── max #细胞核偏大
│       │   ├── ...
│       └── min #细胞核偏小
│           ├── ...
├── data_2019_seg
│   ├── ...
└── data_red_seg
    ├── ...
```
### datanew0918
```
链接：https://pan.baidu.com/s/1KfRbJ7-WITqF5CGJP4Dqeg
提取玛：ibs8
说明：尺寸100*100，新批次数据，包含部分17P0603批次新数据和bianping0909批次数据（bianping0909批次没有type1类型细胞）
目录结构：
datanew0918/
├── invalid #无效原始细胞图
│   ├── 17P0603
│   │   ├── ...
│   └── bianping0909
│       ├── ...
└── valid #有效原始细胞图
    ├── 17P0603
    │   ├── ...
    └── bianping0909
        ├── ...
```
### output
```
链接：https://pan.baidu.com/s/17Vv_9Ry_yb0QSeVmzRSLTA 
提取玛：p87e
说明：共两类细胞，cluster为阳性细胞团和细胞，good为阴性细胞团和细胞
目录结构：
output
├── cluster
│   ├── ffa7ce055.png
│   ├── ...
└── good
│   ├── ccb7ce025.png
│   ├── ...
```
### data_all_1010_new(30505)
```
链接：https://pan.baidu.com/s/1XYOGj6BvitlzodN7TmCyQA&shfl=sharepset 
提取码：a4zt
说明：尺寸100*100，截至到2019年10月10日的所有原始细胞数据(除去福建幼园)，包含5个批次的数据，目录crop/valid为人工筛选过的细胞图，csv与img存放原始FOV图像和标注文件
目录结构（括号内为细胞数量）
data_all_1010_new/
├── 17P0603
│   ├── crop
│   │   ├── invalid
│   │   │   ├── ...
│   │   └── valid(6727)
│   │       ├── 1(1392)
│   │       ├── 13(2)
│   │       ├── 2(4)
│   │       ├── 3(528)
│   │       ├── 4(191)
│   │       ├── 5(2960)
│   │       ├── 7(1490)
│   │       ├── 8(46)
│   │       └── 9(114)
│   ├── csv
│   │   └── ...
│   └── img
│       ├── ...
├── 20190523
│   ├── crop
│   │   ├── invalid
│   │   │   ├── ...
│   │   └── valid(9154)
│   │       ├── 1(1173)
│   │       ├── 12(104)
│   │       ├── 13(130)
│   │       ├── 14(1)
│   │       ├── 15(19)
│   │       ├── 2(497)
│   │       ├── 3(1264)
│   │       ├── 4(346)
│   │       ├── 5(3603)
│   │       ├── 7(1512)
│   │       └── 8(505)
│   ├── csv
│   │   ├── ...
│   └── img
│       ├── ...
├── 400P+100hunhe
│   ├── crop
│   │   ├── invalid
│   │   │   ├── ...
│   │   └── valid(6254)
│   │       ├── 13(1)
│   │       ├── 15(21)
│   │       ├── 2(108)
│   │       ├── 3(692)
│   │       ├── 4(121)
│   │       ├── 5(4092)
│   │       ├── 7(1124)
│   │       ├── 8(94)
│   │       └── 9(1)
│   ├── csv
│   │   ├── ...
│   └── img
│       ├── ...
├── bianping
│   ├── crop
│   │   ├── invalid
│   │   │   ├── ...
│   │   └── valid(7082)
│   │       ├── 12(1)
│   │       ├── 13(1)
│   │       ├── 2(47)
│   │       ├── 3(385)
│   │       ├── 4(151)
│   │       ├── 5(5132)
│   │       ├── 7(1192)
│   │       ├── 8(101)
│   │       └── 9(72)
│   ├── csv
│   │   ├── ...
│   └── img
│       ├── ...
└── redhouse
    ├── crop
    │   ├── invalid
    │   │   ├── ...
    │   └── valid(1288)
    │       ├── 1(837)
    │       ├── 2(10)
    │       ├── 4(78)
    │       └── 7(363)
    ├── csv
    │   ├── ...
    └── img
        ├── ...
```
### 400P_thirteen_1(1862)
```
链接：https://pan.baidu.com/s/1_7MCXSnbdVwC-nydBqW6Sw 
提取码：hh5v
说明：尺寸100*100，2019年10月10日至2019年10月21日的原始细胞数据，属于data_all_1010_new数据集中400P+100hunhe批次的数据，目录crop/valid为人工筛选过的细胞图，csv与img存放原始FOV图像和标注文件
目录结构（括号内为细胞数量）
400P_thirteen/
├── crop
│   ├── invalid
│   │   ├── ...
│   └── valid(1862)
│       ├── 14(3)
│       ├── 15(31)
│       ├── 2(61)
│       ├── 4(58)
│       ├── 5(896)
│       ├── 7(580)
│       └── 8(233)
├── csv
│   ├── ...
└── img
    ├── ...
```
### bianping_eleven(1704)
```
链接：https://pan.baidu.com/s/1UrGbOCYlpUWDN4OMi-6zBA 
提取码：tf4k
说明：尺寸100*100，2019年10月21日至2019年10月23日的原始细胞数据，属于data_all_1010_new数据集中bianping批次的数据，目录crop/valid为人工筛选过的细胞图，csv与img存放原始FOV图像和标注文件
目录结构（括号内为细胞数量）
bianping_eleven
├── crop
│   ├── invalid
│   │   ├── ...
│   └── valid(1704)
│       ├── 12(5)
│       ├── 15(2)
│       ├── 2(34)
│       ├── 4(39)
│       ├── 5(1294)
│       ├── 7(313)
│       └── 8(17)
├── csv
│   ├── ...
└── img
    ├── ...
```
### 400P+100hunhe_fifteen(1977)
```
链接：https://pan.baidu.com/s/1fek-rr3OCv3gwaR1FUi-bQ
提取玛：6xd2
说明：尺寸100*100，2019年10月23日到2019年11月6日的原始细胞数据，属于data_all_1010_new数据集中400P+100混合批次的数据
目录结构：(括号内为细胞图数量)
400P+100hunhe_fifteen/
├── crop
│   ├── invalid
│   │   ├── ...
│   └── valid(1977)
│       ├── 2(71)
│       ├── 3(135)
│       ├── 4(48)
│       ├── 5(1038)
│       ├── 7(531)
│       └── 8(154)
├── csv
│   ├── ...
└── img
    ├── ...
```
### bianping_sixteen_seventeen_1127(6184)
```
链接：https://pan.baidu.com/s/1klbG7NKTjDMvf3vFWe2IgQ
提取码：khgk
说明：尺寸100*100，2019年11月6日到2019年11月27日的原始细胞数据，属于data_all_1010_new数据集中bianping合批次的数据，尺寸:100*100，RBG三通道
目录结构：(括号内为细胞图数量)
bianping_sixteen_seventeen_1127
├── crop
│   ├── invalid
│   │   ├── 15
│   │   ├── 7
│   │   └── 8
│   └── valid(6184)
│       ├── 15(103)
│       ├── 2(364)
│       ├── 3(54)
│       ├── 4(142)
│       ├── 5(4284)
│       ├── 7(971)
│       ├── 8(236)
│       └── 9(30)
├── csv
│   ├── 第16批上传
│   │   ├── ...
│   └── 第17批上传
│       ├── ...
└── img
    ├── 第16批上传
    │   ├── ...
    └── 第17批上传
        ├── ...
```
### bianping_eighteen_1128(1018)
```
链接：https://pan.baidu.com/s/1wdK23WzwiNalJVXeiKeysQ
提取码：mtdv
说明：尺寸100*100，2019年11月27日到2019年11月28日的原始细胞数据，属于data_all_1010_new数据集中bianping合批次的数据，尺寸:100*100，RBG三通道
目录结构：
bianping_eighteen_1128/
├── crop
│   ├── invalid
│   └── valid(1018)
│       ├── 15(52)
│       ├── 2(40)
│       ├── 5)(813)
│       └── 7(113)
├── csv
│   └── ...
└── img
    └── ...

```
#### 细胞团数据
### cluster_seg_1105
```
链接：https://pan.baidu.com/s/1INta7eQW6VtRae0nyw6Z7g
提取玛：z9kj
说明：截至到2019年11月5日，基于医生标注过的FOV原图作出的细胞团数据，如目录结构，cluster为阳性数据，
其中cluster_clusters为阳性细胞团数据，expectone中细胞图含有2～4个细胞，one中细胞图含有一个细胞的数据，
good为阴性数据，其中good_cluster为阴性细胞团数据，其他同上。
目录结构：(括号内为细胞图数量)
cluster_seg_1105
├── cluster
│   ├── cluster_clusters(996)
│   ├── expectone(1198)
│   └── one(1461)
└── good
    ├── expectone(2171)
    ├── good_cluster(33)
    └── one(4637)
```
### cluster_seg_1111
```
链接：https://pan.baidu.com/s/1CdqKO2cosWh1mvvMP7r1eA
提取玛：wmwj
说明：2019年11月5日截至到2019年11月11日，基于医生标注过的bianpingFOV原图作出的细胞团数据，如目录结构，cluster为阳性数据，
其中cluster_clusters为阳性细胞团数据，expectone中细胞图含有2～4个细胞，one中细胞图含有一个细胞的数据。
目录结构：(括号内为细胞图数量)
cluster_seg_1111
├── cluster
    ├── cluster_clusters(557)
    ├── expectone(1496)
    └── one(1208)

```
#### C模型测试数据
### temp_data_1021_torun
```
说明：基于数据集data_all_1010_new，并作了一定的删减
链接：https://pan.baidu.com/s/1KpnRmtZl5e19ZwozMcxryQ&shfl=sharepset 
提取码：qgpu
```
| 编号 | 训练                   | 预测     |
|------|------------------------|----------|
| 1    | 17P_2019_400P_bianping | red      |
| 2    | 17P_2019_400P_red      | bianping |
| 3    | 17P_2019_bianping_red  | 400P     |
| 4    | 17P_400P_bianping_red  | 2019     |
| 5    | 2019_400P_bianping_red | 17P      |
```
每个训练集混合了4个批次的所有细胞，对应预测集为额外批次的所有细胞，所有阳性细胞记为7类，阴性细胞记为1类，若测试C模型，训练集必须与预测集一一对应。
所有训练集（train）1，7类细胞数量各5000个；
所有评估集（test）1，7类细胞数量各200个；
所有预测集（predict）1，7类各1000个（red除外，1，7类各440个）；
目录结构：
temp_data_1021_torun
├── 17P
│   └── predict
│       ├── 1
│       └── 7
├── 17P_2019_400P_bianping
│   ├── test
│   │   ├── 1
│   │   └── 7
│   └── train
│       ├── 1
│       └── 7
... ...
```
#### 不同内容的FOV数据（用于对比细胞切割算法）
### Data_FOV_types
```
链接：https://pan.baidu.com/s/1AUeui2f-juKkruImBPOjGw
提取码：uhd6
说明：orgdata_fov_types包含不同内容的FOV原始数据（详情请看解压文件中的readme）；output_MaskRcnn为基于orgdata_fov_types算法MaskRcnn在FOV上标记其检测出的细胞的图像，后面可将其他算法标记的细胞与该数据进行对比，从而选出性能更佳的算法。
目录结构（括号内为细胞数量）
Data_FOV_types/
├── orgdata_fov_types（78）
│   ├── FOV_type_a
│   ├── ...
└── output_MaskRcnn（78）
    ├── a
    ├── ...
```
#### 细胞过滤
### data_cell_seg_1122（训练数据）
```
链接：https://pan.baidu.com/s/1yUUOAi0Q2GeecscdXg2S4A
提取码：hcc2
说明：data_cell_seg_1122数据集用于训练过滤细胞分类器，原始数据来自5个批次随机抽取的500张FOV，其细胞图尺寸:100*100，RGB三通道，valid为质量较好的细胞（希望过滤得到），invalid为质量较差的细胞（希望过滤掉），实际训练时建议将两者比例调成1:1
目录结构（括号内为细胞数量）
data_cell_seg_1122

├── invalid(26479)
│   ├── ...
└── valid(9545)
│   ├── ...
```
### FOV_cells_origin（测试数据）
```
链接：https://pan.baidu.com/s/1NjrdXjreQjBKlQyXydBvvA
提取码：ew8v
说明：2019年11约26日制作的数据，用于验证细胞过滤分类器效果，其中FOV_origin为从17P...、2019...批次数据抽取的两个病例中随机抽出500张FOV，cells_all为FOV_origin数据用MaskRcnn切割出的细胞共41059个细胞。尺寸：100*100，RGB三通道
目录结构：
FOV_cells_origin
├── cells_all（41059）
└── FOV_origin（500）
```
### cell_filter_data_1204（测试数据2）
```
链接：https://pan.baidu.com/s/1waZaKRm_bmdigP9FpcpDag
提取码：wdnn
说明：2019年12月4日，用于测试细胞过滤分类效果，细胞尺寸：100*100，RGB三通道，FOV来自所有医生标记过的FOV
目录结构：
cell_filter_data_1204
├── FOV(1136)
├── invalid_cells(39653)
└── valid_cells(96102)
```
### bingli_N_cells_fit_1213（训练+测试数据——阴性病例）
```
链接：https://pan.baidu.com/s/1S6a5uwD4GhYoVZZRT_DITA 
提取码：5ito
说明：2019年12月13日，基于目前所有阴性病例masrcnn切割结果（尺寸：100*100，RGB三通道），随机选出143000个细胞，按照‘人工筛选细胞的标准’人工筛选细胞
目录结构：
bingli_N_cells_fit_1213
├── test_data
│   ├── invalid_test(1000)
│   └── valid_test(1000)
└── train_data
    ├── invalid(88433)
    └── valid(54567)

```
### bingli_P2_cells_fit_1213（训练+测试数据——阳性病例）
```
链接：https://pan.baidu.com/s/1OfY3XrT6-lUYD52iF3G2Xw
提取码：yrk8
说明：2019年12月13日，基于目前数据cell_filter_data_1204，挑选其中全部valid数据，随机挑选部分invalid数据（保证样本数量均衡），按照‘人工筛选细胞的标准’人工筛选细胞
目录结构：
bingli_P2_cells_fit_1213
├── test_data
│   ├── invalid_test（1000）
│   └── valid_test（1000）
└── train_data
    ├── invalid（42294）
    └── valid（35359）
```
### bingli_N_V2_1220（训练+测试数据2次筛选——阴性病例）
```
链接：https://pan.baidu.com/s/1PhuFwSMV7TZTHzbqsFHBKQ 
提取码：koio
说明：2019年12月25日，基于目前数据bingli_N_cells_fit_1213，按照‘人工筛选细胞的标准V2’人工筛选细胞
目录结构：
bingli_N_V2_1220
├── test_data
│   ├── invalid_test(1000)
│   └── valid_test(1000)
└── train_data
    ├── invalid(91765)
    └── valid(51235)
```
### bingli_P2_V2_1225（训练+测试数据2次筛选——阳性病例）
```
链接：https://pan.baidu.com/s/16_-siABexMsPT2uCJ7NueQ 
提取码：6to2
说明：2019年12月25日，基于目前数据bingli_P2_cells_fit_1213，按照‘人工筛选细胞的标准V2’人工筛选细胞
目录结构：
bingli_P2_V2_1225
├── test_data
│   ├── invalid_test(1000)
│   └── valid_test(1000)
└── train_data
    ├── invalid(46323)
    └── valid(31330)
```
#### 细胞预测
### cells_towclass_1230
```
链接：https://pan.baidu.com/s/1ukzCHX3IUHGzEmCpYlHLRA 
提取码：6f61
说明：2019年12月30日，基于目前所有医生标记过的细胞（RGB，100×100），具体cells_N: 1 5 12 13 15 / cells_P: 2 3 4 7 8 9 14（14分类本是阴性细胞，但由于形态非常接近且数量只有4个，暂归为阳性分类）
目录结构：
cells_towclass_1230
├── data_test
│   ├── cells_N_test(1000)
│   └── cells_P_test(1000)
└── data_train
    ├── cells_N(26986)
    └── cells_P(14364)
```
#### 厦参数据
### cells_xc0216_2class_onecell（第一批20200216）
```
链接：https://pan.baidu.com/s/1TPzWNsD8SZ_NeqPVwYNazQ 
提取码：fum8
厦参导出数据，经整理现为2分类，阳性4181，阴性14w
```
