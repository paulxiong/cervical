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
  1: 'const.train',
  2: 'const.predict'
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
  6: 'HOWTOMALA',
  7: 'YOLOV4',
  8: 'YOLOV5'
}

// 细胞分类
export const cellsType = {
  1: 'const.cellsType1',
  2: 'const.cellsType2',
  3: 'const.cellsType3',
  4: 'const.cellsType4',
  6: 'const.cellsType6',
  7: 'const.cellsType7',
  8: 'const.cellsType8',
  9: 'const.cellsType9',
  10: 'const.cellsType10',
  11: 'const.cellsType11',
  12: 'const.cellsType12',
  13: 'const.cellsType13',
  14: 'const.cellsType14',
  15: 'const.cellsType15',
  50: 'const.cellsType50',
  51: 'const.cellsType51',
  100: 'const.cellsType100',
  200: 'const.cellsType200'
}

// 病例分类
export const medicalType = {
  50: 'const.medicalType50',
  51: 'const.medicalType51',
  100: 'const.medicalType100'
}

export const projectType = {
  0: '未知',
  1: '保留',
  2: 'const.train',
  3: 'const.predict'
}

// order 从小到大表示病从轻到重，choicscolor是选项菜单颜色，typecolor是选框颜色
export const cellsOptions = [
  {
    value: 1,
    order: 1,
    choicscolor: '#28c730',
    typecolor: '#28c730',
    label: 'const.cellNorn'
  },
  {
    value: 12,
    order: 2,
    choicscolor: '#51e059',
    typecolor: '#28c730',
    label: 'const.cellT'
  },
  {
    value: 15,
    order: 3,
    choicscolor: '#6ff176',
    typecolor: '#28c730',
    label: 'const.cellX1'
  },
  {
    value: 14,
    order: 4,
    choicscolor: '#91fb96',
    typecolor: '#28c730',
    label: 'const.cellHSV'
  },
  {
    value: 13,
    order: 5,
    choicscolor: '#b6ffba',
    typecolor: '#28c730',
    label: 'const.cellM'
  }
]

export const cellsOptions2 = [
  {
    value: 7,
    order: 101,
    choicscolor: '#f5e6e6',
    typecolor: 'red',
    label: 'const.cellASCUS'
  },
  {
    value: 8,
    order: 102,
    choicscolor: '#fddcdc',
    typecolor: 'red',
    label: 'const.cellASH'
  },
  {
    value: 2,
    order: 103,
    choicscolor: '#ffcece',
    typecolor: 'red',
    label: 'const.cellLSIL'
  },
  {
    value: 3,
    order: 104,
    choicscolor: '#fbbbbc',
    typecolor: 'red',
    label: 'const.cellHSIL'
  },
  {
    value: 4,
    order: 105,
    choicscolor: '#efa5a5',
    typecolor: 'red',
    label: 'const.cellHPV'
  },
  {
    value: 6,
    order: 106,
    choicscolor: '#f98787',
    typecolor: 'red',
    label: 'const.cellSCC'
  },
  {
    value: 9,
    order: 107,
    choicscolor: '#ff6b6b',
    typecolor: 'red',
    label: 'const.cellAGC'
  },
  {
    value: 10,
    order: 108,
    choicscolor: '#f94d4d',
    typecolor: 'red',
    label: 'const.cellAIS'
  },
  {
    value: 11,
    order: 109,
    choicscolor: '#ff2c2c',
    typecolor: 'red',
    label: 'const.cellADC'
  }
]

export const cellsOptions3 = [
  {
    value: 200,
    order: 201,
    choicscolor: '#f9e7b5',
    typecolor: '#ffba00',
    label: 'const.cellNot'
  },
  {
    value: 100,
    order: 202,
    choicscolor: '#ffe08c',
    typecolor: '#ffba00',
    label: 'const.cellUnknown'
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
  { id: 1,   order: 1,   choicscolor: '#00FF00', typecolor: '#009e08', notcelltype: false, shortname: 'Norm',       label: 'const.labelCellNorn' },
  { id: 23,  order: 2,   choicscolor: '#3bf940', typecolor: '#009e08', notcelltype: false, shortname: 'Glandular',  label: 'const.labelCellGlandular' },
  { id: 15,  order: 3,   choicscolor: '#66ff6b', typecolor: '#009e08', notcelltype: false, shortname: 'X1',         label: 'const.labelCellX1' },
  { id: 14,  order: 4,   choicscolor: '#7cf780', typecolor: '#009e08', notcelltype: false, shortname: 'HSV',        label: 'const.labelCellHSV' },
  { id: 13,  order: 5,   choicscolor: '#89f78d', typecolor: '#009e08', notcelltype: false, shortname: 'M',          label: 'const.labelCellM' },
  { id: 20,  order: 6,   choicscolor: '#9bf59e', typecolor: '#009e08', notcelltype: false, shortname: 'PM',         label: 'const.labelCellPM' },
  { id: 21,  order: 7,   choicscolor: '#b8f9bb', typecolor: '#009e08', notcelltype: false, shortname: 'Metaplasia', label: 'const.labelCellMetaplasia' },
  { id: 22,  order: 8,   choicscolor: '#cdfdcf', typecolor: '#009e08', notcelltype: false, shortname: 'B1/T1/M1',   label: 'const.labelCellB' },
  { id: 12,  order: 9,   choicscolor: '#e4ffe5', typecolor: '#009e08', notcelltype: false, shortname: 'T',          label: 'const.labelCellT' },

  // 阳性
  { id: 7,   order: 101, choicscolor: '#fdbdbd', typecolor: '#ff0000', notcelltype: false, shortname: 'ASC-US',     label: 'const.labelCellASCUS' },
  { id: 8,   order: 102, choicscolor: '#fba1a1', typecolor: '#ff0000', notcelltype: false, shortname: 'ASC-H',      label: 'const.labelCellASCH' },
  { id: 9,   order: 107, choicscolor: '#fb8989', typecolor: '#ff0000', notcelltype: false, shortname: 'AGC',        label: 'const.labelCellAGC' },
  { id: 2,   order: 103, choicscolor: '#fd7272', typecolor: '#ff0000', notcelltype: false, shortname: 'LSIL',       label: 'const.labelCellLSIL' },
  { id: 3,   order: 104, choicscolor: '#ff6968', typecolor: '#ff0000', notcelltype: false, shortname: 'HSIL',       label: 'const.labelCellHSIL' },
  { id: 4,   order: 105, choicscolor: '#fb4f4e', typecolor: '#ff0000', notcelltype: false, shortname: 'HPV',        label: 'const.labelCellHPV' },
  { id: 6,   order: 106, choicscolor: '#fd3b3a', typecolor: '#ff0000', notcelltype: false, shortname: 'SCC',        label: 'const.labelCellSCC' },
  { id: 10,  order: 108, choicscolor: '#ff1d1d', typecolor: '#ff0000', notcelltype: false, shortname: 'AIS',        label: 'const.labelCellAIS' },
  { id: 11,  order: 109, choicscolor: '#FF0000', typecolor: '#ff0000', notcelltype: false, shortname: 'ADC',        label: 'const.labelCellADC' },
  // 其他
  { id: 200, order: 201, choicscolor: '#ffdca8', typecolor: '#ff7800', notcelltype: false, shortname: 'NC',         label: 'const.labelCellNC' },
  { id: 100, order: 202, choicscolor: '#ffcd84', typecolor: '#ff7800', notcelltype: false, shortname: 'Unkown',     label: 'const.labelCellUnkown' },
  { id: 50,  order: 202, choicscolor: '#ffba55', typecolor: '#ff7800', notcelltype: true,  shortname: 'N',          label: 'const.labelCellN' },
  { id: 51,  order: 202, choicscolor: '#ff9800', typecolor: '#ff7800', notcelltype: true,  shortname: 'P',          label: 'const.labelCellP' }
]
/* eslint-enable */

// 标注页面把原图的宽缩放到几个像素点（原图太大了一个屏幕显示不过来）
export const page3ImgWidth = 645
