### data_org_0918
```
链接：https://pan.baidu.com/s/1R31QW5fER0s7Bn7FIQDWMw
提取玛：d9vr
说明：尺寸100*100，人工筛选过的原始细胞数据，9月17日以前的测试都基于此数据
目录结构：
data_org_0918/
├── invalid
│   ├── 17P0603
│   │   ├── 1
│   │   ├── 3
│   │   ├── ...
│   ├── 20190523
│   │   ├── 1
│   │   ├── 12
│   │   ├── ...
│   └── redhouse
│       ├── 1
│       ├── 2
│       ├── ...
├── invalid_masked
│   ├── 17P0603
│   │   ├── 1
│   │   ├── 3
│   │   ├── ...
│   ├── 20190523
│   │   ├── 1
│   │   ├── 12
│   │   ├── ...
│   └── redhouse
│       ├── 1
│       ├── 2
│       ├── ...
├── valid
│   ├── 17P0603
│   │   ├── 1
│   │   ├── 2
│   │   ├── ...
│   ├── 20190523
│   │   ├── 1
│   │   ├── ...
│   └── redhouse
│       ├── 1
│       ├── ...
├── valid_gray
│   ├── 17P0603
│   │   ├── 1
│   │   ├── ...
│   ├── 20190523
│   │   ├── 1
│   │   ├── ...
│   └── redhouse
│       ├── 1
│       ├── ...
├── valid_gray_rotate
│   ├── 17P0603
│   │   ├── 1
│   │   ├── ...
│   ├── 20190523
│   │   ├── 1
│   │   ├── ...
│   └── redhouse
│       ├── 1
│       ├── ...
└── valid_masked
    ├── 17P0603_masked
    │   ├── 1
    │   ├── ...
    ├── 20190523_masked
    │   ├── 1
    │   ├── ...
    └── redhouse_masked
        ├── 1
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
│   │   ├── blue
│   │   │   ├── 1
│   │   │   └── 7
│   │   └── unblue
│   │       ├── 1
│   │       └── 7
│   ├── org_num
│   │   ├── one
│   │   │   ├── 1
│   │   │   └── 7
│   │   └── unone
│   │       ├── 1
│   │       └── 7
│   └── org_size
│       ├── max
│       │   ├── 1
│       │   └── 7
│       └── min
│           ├── 1
│           └── 7
├── data_2019_seg
│   ├── org_color
│   │   ├── blue
│   │   │   ├── 1
│   │   │   └── 7
│   │   └── unblue
│   │       ├── 1
│   │       └── 7
│   ├── org_num
│   │   ├── one
│   │   │   ├── 1
│   │   │   └── 7
│   │   └── unone
│   │       ├── 1
│   │       └── 7
│   └── org_size
│       ├── max
│       │   ├── 1
│       │   └── 7
│       └── min
│           ├── 1
│           └── 7
└── data_red_seg
    ├── org_color
    │   ├── blue
    │   │   ├── 1
    │   │   └── 7
    │   └── unblue
    │       ├── 1
    │       └── 7
    ├── org_num
    │   ├── one
    │   │   ├── 1
    │   │   └── 7
    │   └── unone
    │       ├── 1
    │       └── 7
    └── org_size
        ├── max
        │   ├── 1
        │   └── 7
        └── min
            ├── 1
            └── 7
```
### datanew0918
```
链接：https://pan.baidu.com/s/1KfRbJ7-WITqF5CGJP4Dqeg
提取玛：ibs8
说明：尺寸100*100，新批次数据，包含部分17P0603批次新数据和bianping0909批次数据（bianping0909批次没有type1类型细胞）
目录结构：
datanew0918/
├── invalid
│   ├── 17P0603
│   │   ├── crop
│   │   │   ├── 1
│   │   │   ├── ...
│   │   └── crop_masked
│   │       ├── 1
│   │       ├── ...
│   └── bianping0909
│       ├── crop
│       │   ├── 12
│       │   ├── ...
│       └── crop_masked
│           ├── 12
│           ├── ...
└── valid
    ├── 17P0603
    │   ├── crop
    │   │   ├── 1
    │   │   ├── ...
    │   └── crop_masked
    │       ├── 1
    │       ├── ...
    └── bianping0909
        ├── crop
        │   ├── 13
        │   ├── ...
        └── crop_masked
            ├── 13
            ├── ...
```
