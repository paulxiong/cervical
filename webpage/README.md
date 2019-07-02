## 1 目录结构
```
├── 1_db                     数据库部署方法
├── 2_api_server             API服务器 
├── 3_thumbor                图片处理（缩略）服务器，图片太大了页面预览速度慢，通过缩放加快加载速度
└── 4_vue-element-admin      前端，数据浏览，数据选择，训练log查看，测试结果查看
``` 

## 2 服务器部署API服务器 
```
$ cd webpage/2_api_server/
$ ./2_build_docker_img.sh

服务器上
$ docker-compose up -d
```

