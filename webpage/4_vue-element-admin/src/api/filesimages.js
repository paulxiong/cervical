// 文件和图片的URL链接生成的相关函数库
import { APIUrl } from '@/const/config'

export const medicalURL = {
  // 返回某个病例数据的根目录
  rootPath: function(bid, mid) {
    return `${APIUrl}/imgs/scratch/img/${bid}/${mid}`
  },
  // 返回某个病例数据的FOV根目录
  imagesRootPath: function(bid, mid) {
    return `${APIUrl}/imgs/scratch/img/${bid}/${mid}/Images`
  },
  // 返回某个病例数据的FOV的路径
  imagesPath: function(bid, mid, imgname) {
    return `${APIUrl}/imgs/scratch/img/${bid}/${mid}/Images/${imgname}`
  },
  // 返回某个病例数据的Result缩略图
  resultImagePath: function(bid, mid, resultimgname) {
    return `${APIUrl}/imgs/scratch/img/${bid}/${mid}/Thumbs/${resultimgname}`
  },
  // 返回某个病例数据的Preview缩略图
  previewImagePath: function(bid, mid, previewimgname) {
    return `${APIUrl}/imgs/scratch/img/${bid}/${mid}/Thumbs/${previewimgname}`
  }
}
