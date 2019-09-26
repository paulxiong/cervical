// 裁剪图片、训练的状态
export const taskStatus = {
  0: { status: '初始化 ', type: 'info' },
  1: { status: '送去处理', type: 'warning' },
  2: { status: '开始处理', type: 'warning' },
  3: { status: '处理出错', type: 'danger' },
  4: { status: '处理完成', type: 'success' },
  5: { status: '目录不存在', type: 'danger' },
  6: { status: '送去训练', type: 'warning' },
  7: { status: '开始训练', type: 'warning' },
  8: { status: '训练出错', type: 'danger' },
  9: { status: '训练完成', type: 'success' }
}

// 训练类型
export const typeStatus = {
  0: { status: '预测' },
  1: { status: '训练' },
  2: { status: '测试' }
}

// 用户
export const createdBy = {
  0: { name: '普通用户' },
  1: { name: '超级管理员' }
}

// 训练模型类型
export const modelType = {
  0: { name: '未知' },
  1: { name: 'UNET' },
  2: { name: 'GAN' },
  3: { name: 'SVM' },
  4: { name: 'MASKRCNN' },
  5: { name: 'AUTOKERAS' }
}

// 标注页面把原图的宽缩放到几个像素点（原图太大了一个屏幕显示不过来）
export const page3ImgWidth = 645
