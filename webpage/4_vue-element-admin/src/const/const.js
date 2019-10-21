// 裁剪图片、训练的状态
export const taskStatus = {
  0: '初始化',
  1: '送去处理',
  2: '开始处理',
  3: '处理出错',
  4: '处理完成',
  5: '目录不存在',
  6: '送去训练',
  7: '开始训练',
  8: '训练出错',
  9: '训练完成',
  10: '送去预测',
  11: '开始预测',
  12: '预测出错',
  13: '预测完成'
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
  1: '超级管理员'
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
  1: 'Norm 正常细胞',
  2: 'LSIL 鳞状上皮细胞低度病变',
  3: 'HSIL 鳞状上皮细胞高度病变',
  4: 'HPV 感染',
  5: 'NILM 未见上皮内病变',
  6: 'SCC 鳞状上皮细胞癌',
  7: 'ASCUS 不典型鳞状细胞低',
  8: 'ASCH 不典型鳞状细胞高',
  9: 'AGC 不典型腺细胞',
  10: 'AIS 颈管原位腺癌',
  11: 'ADC 腺癌',
  12: 'T 滴虫',
  13: 'M 霉菌',
  14: 'HSV 疱疹',
  15: 'X1 线索细胞'
}

// 标注页面把原图的宽缩放到几个像素点（原图太大了一个屏幕显示不过来）
export const page3ImgWidth = 645
