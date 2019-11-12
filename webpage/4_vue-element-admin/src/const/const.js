// 裁剪图片、训练的状态
export const taskStatus = {
  0: '初始化',
  1: '送去处理',
  2: '开始',
  3: '出错',
  4: '完成',
  5: '目录不存在',
  6: '送去训练',
  7: '开始',
  8: '出错',
  9: '完成',
  10: '送去预测',
  11: '开始',
  12: '出错',
  13: '完成'
}

export const taskType = {
  0: 'info',
  1: 'warning',
  2: 'warning',
  3: 'danger',
  4: 'success',
  5: 'danger',
  6: 'warning',
  7: 'warning',
  8: 'danger',
  9: 'success',
  10: 'warning',
  11: 'warning',
  12: 'danger',
  13: 'success'
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
  5: 'AUTOKERAS'
}

// 细胞分类
export const cellsType = {
  1: '1 Norm正常细胞',
  2: '2 LSIL鳞状上皮细胞低度病变',
  3: '3 HSIL鳞状上皮细胞高度病变',
  4: '4 HPV感染',
  5: '5 NILM未见上皮内病变',
  6: '6 SCC鳞状上皮细胞癌',
  7: '7 ASCUS不典型鳞状细胞低',
  8: '8 ASCH不典型鳞状细胞高',
  9: '9 AGC不典型腺细胞',
  10: '10 AIS颈管原位腺癌',
  11: '11 ADC腺癌',
  12: '12 T滴虫',
  13: '13 M霉菌',
  14: '14 HSV疱疹',
  15: '15 X1线索细胞',
  50: '50 阳性细胞',
  51: '51 阴性细胞',
  100: '100 未知类型'
}

export const projectType = {
  0: '未知',
  1: '保留',
  2: '训练',
  3: '预测'
}

// 标注页面把原图的宽缩放到几个像素点（原图太大了一个屏幕显示不过来）
export const page3ImgWidth = 645
