// 裁剪图片、训练的状态
export const taskStatus = {
  0: 'const.init',
  1: 'const.ready',
  2: 'const.start',
  3: 'const.error',
  4: 'const.done',
  5: 'const.tobereview',
  6: 'const.reviewed'
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

/* eslint-disable */
export const cellsOptionsAll = [
  { id: 1,   order: 1,   choicscolor: '#00FF00', typecolor: '#009e08', notcelltype: false, shortname: 'Norm',       label: '正常细胞' },
  { id: 23,  order: 2,   choicscolor: '#3bf940', typecolor: '#009e08', notcelltype: false, shortname: 'Glandular',  label: '腺上皮细胞' },
  { id: 15,  order: 3,   choicscolor: '#66ff6b', typecolor: '#009e08', notcelltype: false, shortname: 'X1',         label: '线索细胞' },
  { id: 14,  order: 4,   choicscolor: '#7cf780', typecolor: '#009e08', notcelltype: false, shortname: 'HSV',        label: '疱疹' },
  { id: 13,  order: 5,   choicscolor: '#89f78d', typecolor: '#009e08', notcelltype: false, shortname: 'M',          label: '霉菌' },
  { id: 20,  order: 6,   choicscolor: '#9bf59e', typecolor: '#009e08', notcelltype: false, shortname: 'PM',         label: '萎缩性改变' },
  { id: 21,  order: 7,   choicscolor: '#b8f9bb', typecolor: '#009e08', notcelltype: false, shortname: 'Metaplasia', label: '鳞状化生细胞' },
  { id: 22,  order: 8,   choicscolor: '#cdfdcf', typecolor: '#009e08', notcelltype: false, shortname: 'B1/T1/M1',   label: '生物性病原体' },
  { id: 12,  order: 9,   choicscolor: '#e4ffe5', typecolor: '#009e08', notcelltype: false, shortname: 'T',          label: '滴虫' },

  // 阳性
  { id: 7,   order: 101, choicscolor: '#fdbdbd', typecolor: '#ff0000', notcelltype: false, shortname: 'ASC-US',     label: '非典型鳞状细胞、意义不明确' },
  { id: 8,   order: 102, choicscolor: '#fba1a1', typecolor: '#ff0000', notcelltype: false, shortname: 'ASC-H',      label: '非典型鳞状细胞不除外高级别鳞状上皮内病变' },
  { id: 9,   order: 107, choicscolor: '#fb8989', typecolor: '#ff0000', notcelltype: false, shortname: 'AGC',        label: '不典型腺细胞' },
  { id: 2,   order: 103, choicscolor: '#fd7272', typecolor: '#ff0000', notcelltype: false, shortname: 'LSIL',       label: '低级别鳞状上皮内病变' },
  { id: 3,   order: 104, choicscolor: '#ff6968', typecolor: '#ff0000', notcelltype: false, shortname: 'HSIL',       label: '高级别鳞状上皮内病变' },
  { id: 4,   order: 105, choicscolor: '#fb4f4e', typecolor: '#ff0000', notcelltype: false, shortname: 'HPV',        label: '人乳头瘤病毒' },
  { id: 6,   order: 106, choicscolor: '#fd3b3a', typecolor: '#ff0000', notcelltype: false, shortname: 'SCC',        label: '鳞状上皮细胞癌' },
  { id: 10,  order: 108, choicscolor: '#ff1d1d', typecolor: '#ff0000', notcelltype: false, shortname: 'AIS',        label: '颈管原位腺癌' },
  { id: 11,  order: 109, choicscolor: '#FF0000', typecolor: '#ff0000', notcelltype: false, shortname: 'ADC',        label: '腺癌' },
  // 其他
  { id: 200, order: 201, choicscolor: '#ffdca8', typecolor: '#ff7800', notcelltype: false, shortname: 'NC',         label: '不是细胞' },
  { id: 100, order: 202, choicscolor: '#ffcd84', typecolor: '#ff7800', notcelltype: false, shortname: 'Unkown',     label: '未知类型' },
  { id: 50,  order: 202, choicscolor: '#ffba55', typecolor: '#ff7800', notcelltype: true,  shortname: 'N',          label: '阴性' },
  { id: 51,  order: 202, choicscolor: '#ff9800', typecolor: '#ff7800', notcelltype: true,  shortname: 'P',          label: '阳性' }
]
/* eslint-enable */

// 标注页面把原图的宽缩放到几个像素点（原图太大了一个屏幕显示不过来）
export const page3ImgWidth = 645
