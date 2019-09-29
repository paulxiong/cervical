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
  9: '训练完成'
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
  9: 'success'
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

// 标注页面把原图的宽缩放到几个像素点（原图太大了一个屏幕显示不过来）
export const page3ImgWidth = 645
