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

export const cellsOptions = [
  {
    value: 1,
    label: 'Norm正常细胞'
  },
  {
    value: 12,
    label: 'T滴虫'
  },
  {
    value: 15,
    label: 'X1线索细胞'
  },
  // {
  //   value: 5,
  //   label: 'NILM未见上皮内病变'
  // },
  {
    value: 14,
    label: 'HSV疱疹'
  },
  {
    value: 13,
    label: 'M霉菌'
  }
]

export const cellsOptions2 = [
  {
    value: 2,
    label: 'LSIL鳞状上皮细胞低度病变'
  },
  {
    value: 6,
    label: 'SCC鳞状上皮细胞癌'
  },
  {
    value: 3,
    label: 'HSIL鳞状上皮细胞高度病变'
  },
  {
    value: 8,
    label: 'ASCH不典型鳞状细胞高'
  },
  {
    value: 7,
    label: 'ASCUS不典型鳞状细胞低'
  },
  {
    value: 9,
    label: 'AGC不典型腺细胞'
  },
  {
    value: 10,
    label: 'AIS颈管原位腺癌'
  },
  {
    value: 4,
    label: 'HPV感染'
  },
  {
    value: 11,
    label: 'ADC腺癌'
  }
]

export const cellsOptions3 = [
  {
    value: 100,
    label: '未知类型'
  },
  {
    value: 200,
    label: '不是细胞'
  }
]

// 标注页面把原图的宽缩放到几个像素点（原图太大了一个屏幕显示不过来）
export const page3ImgWidth = 645
