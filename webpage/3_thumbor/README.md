## 启动
```
$ docker-compose up -d
```

## 使用方法
拷贝一个原图到data/loader/目录
```
$ cp x.png data/loader/
```

## 查看
### 查看原图
```
http://127.0.0.1/unsafe/x.png
```
### 查看原图的信息，返回json
```
http://127.0.0.1/unsafe/meta/x.png
```
### 图片按照宽400等比缩放
```
http://127.0.0.1/unsafe/400x0/x.png
```
### 图片按照宽400等比缩放之后，质量按照50%显示
```
http://127.0.0.1/unsafe/400x0/filters:quality(50)/x.png
```

## 对项目的帮助
#### 1 提供图片文件服务，支持部署到内网
#### 2 支持图片操作的方法（比如支持图片缩放，如果图片不做缩放在查看FOV原图的时候非常慢，每张FOV有几MB，网络不好的情况需要很久）

