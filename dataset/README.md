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
