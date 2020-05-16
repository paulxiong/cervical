// 裁剪图片、训练的状态
export const taskStatus = {
  0: '初始化',
  1: '送去处理',
  2: '开始',
  3: '出错',
  4: '完成',
  5: '送去审核',
  6: '审核完成'
}

export const taskType = {
  0: 'info',
  1: 'warning',
  2: 'warning',
  3: 'danger',
  4: 'success',
  5: 'warning',
  6: 'success'
}

// 训练类型
export const typeStatus = {
  1: '训练',
  2: '预测'
}

// 用户
export const createdBy = {
  0: '普通用户',
  1: '管理员'
}

// 训练模型类型
export const modelType = {
  0: '未知',
  1: 'UNET',
  2: 'GAN',
  3: 'SVM',
  4: 'MASKRCNN',
  5: 'AUTOKERAS',
  6: 'HOWTOMALA'
}

// 细胞分类
export const cellsType = {
  1: '1 Norm正常细胞 N',
  2: '2 LSIL鳞状上皮细胞低度病变 P',
  3: '3 HSIL鳞状上皮细胞高度病变 P',
  4: '4 HPV感染 P',
  // 5: '5 NILM未见上皮内病变 N',
  6: '6 SCC鳞状上皮细胞癌 P',
  7: '7 ASCUS不典型鳞状细胞低 P',
  8: '8 ASCH不典型鳞状细胞高 P',
  9: '9 AGC不典型腺细胞 P',
  10: '10 AIS颈管原位腺癌 P',
  11: '11 ADC腺癌 P',
  12: '12 T滴虫 N',
  13: '13 M霉菌 N',
  14: '14 HSV疱疹 N',
  15: '15 X1线索细胞 N',
  50: '50 阴性细胞 N',
  51: '51 阳性细胞 P',
  100: '100 未知类型',
  200: '200 不是细胞'
}

export const projectType = {
  0: '未知',
  1: '保留',
  2: '训练',
  3: '预测'
}

// order 从小到大表示病从轻到重，choicscolor是选项菜单颜色，typecolor是选框颜色
export const cellsOptions = [
  {
    value: 1,
    order: 1,
    choicscolor: '#28c730',
    typecolor: '#28c730',
    label: 'Norm正常细胞'
  },
  {
    value: 12,
    order: 2,
    choicscolor: '#51e059',
    typecolor: '#28c730',
    label: 'T滴虫'
  },
  {
    value: 15,
    order: 3,
    choicscolor: '#6ff176',
    typecolor: '#28c730',
    label: 'X1线索细胞'
  },
  {
    value: 14,
    order: 4,
    choicscolor: '#91fb96',
    typecolor: '#28c730',
    label: 'HSV疱疹'
  },
  {
    value: 13,
    order: 5,
    choicscolor: '#b6ffba',
    typecolor: '#28c730',
    label: 'M霉菌'
  }
]

export const cellsOptions2 = [
  {
    value: 7,
    order: 101,
    choicscolor: '#f5e6e6',
    typecolor: 'red',
    label: 'ASC-US不典型鳞状细胞低'
  },
  {
    value: 8,
    order: 102,
    choicscolor: '#fddcdc',
    typecolor: 'red',
    label: 'ASCH不典型鳞状细胞高'
  },
  {
    value: 2,
    order: 103,
    choicscolor: '#ffcece',
    typecolor: 'red',
    label: 'LSIL鳞状上皮细胞低度病变'
  },
  {
    value: 3,
    order: 104,
    choicscolor: '#fbbbbc',
    typecolor: 'red',
    label: 'HSIL鳞状上皮细胞高度病变'
  },
  {
    value: 4,
    order: 105,
    choicscolor: '#efa5a5',
    typecolor: 'red',
    label: 'HPV感染'
  },
  {
    value: 6,
    order: 106,
    choicscolor: '#f98787',
    typecolor: 'red',
    label: 'SCC鳞状上皮细胞癌'
  },
  {
    value: 9,
    order: 107,
    choicscolor: '#ff6b6b',
    typecolor: 'red',
    label: 'AGC不典型腺细胞'
  },
  {
    value: 10,
    order: 108,
    choicscolor: '#f94d4d',
    typecolor: 'red',
    label: 'AIS颈管原位腺癌'
  },
  {
    value: 11,
    order: 109,
    choicscolor: '#ff2c2c',
    typecolor: 'red',
    label: 'ADC腺癌'
  }
]

export const cellsOptions3 = [
  {
    value: 200,
    order: 201,
    choicscolor: '#f9e7b5',
    typecolor: '#ffba00',
    label: '不是细胞'
  },
  {
    value: 100,
    order: 202,
    choicscolor: '#ffe08c',
    typecolor: '#ffba00',
    label: '未知类型'
  }
  // {
  //   value: 50,
  //   choicscolor: '#ffd258',
  //   label: '阴性'
  // },
  // {
  //   value: 51,
  //   choicscolor: '#ffba00',
  //   label: '阳性'
  // }
]

// 标注页面把原图的宽缩放到几个像素点（原图太大了一个屏幕显示不过来）
export const page3ImgWidth = 645
