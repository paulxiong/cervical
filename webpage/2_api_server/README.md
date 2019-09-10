#### 1 安装 golang

#### 2 安装golang的模块
```
$ go get -u github.com/swaggo/swag/cmd/swag
```

#### 3 本地运行源码
```
$ ./1_run.sh
```

#### 4 使用docker部署服务
```
$ ./2_build_docker_img.sh
$ docker build -t lambdazhang/xdedu:0.0.1 .
$ docker run -d --name=xdedu_server \
    -e VIRTUAL_HOST=testwechat.tiegushi.com \
    -e GIN_MODE=release \
    -e SERVER_PORT=80 \
    -e LOG_OUT='enable' \
    -e LOG_GIN='enable' \
    -e LOG_LEVEL='Info' \
    -e PG_HOST='10.27.176.133' \
    -e PG_PORT=65432 \
    -e PG_DB='postgres' \
    -e PG_USR='postgres' \
    -e PG_PASSWD='postgres' \
    -e EXPIRE_SECOND=600 \
    lambdazhang/xdedu:70ad187 ./main.exe
```

#### 5 代码目录结构说明
##### 打包和部署相关

```
├── 1_run.sh                    执行这个脚本启动本地源码
├── 2_build_docker_img.sh       执行这个脚本打包网页代码以及服务器代码，并最终生成docker image
├── adminpage -> ../6_admin/
├── webpage -> ../4_vue/
├── 
```

##### 压力测试脚本及本地数据库

```
├── benchmark
│   ├── log.txt
│   ├── main_test.sh
│   ├── scripts
│   │   ├── ping.lua
│   │   └── token.lua
│   └── token.txt
├── docker
│   ├── docker-compose.yml
│   └── README.md
├── README.md
```

##### 基于gin做的API服务端
```
│
├── main.go                入口函数，启动router，打印服务信息
├── middlewares            JWT的中间件，登陆认证使用
│   └── jwt.go
│
├── routes                 路由代码，配置路由接口、跨域、压缩、鉴权
│   └── routes.go
│
├── controllers            被路由调用的模块，连接路由和数据库
│   ├── course.go
│   ├── pong.go
│   ├── tiku.go
│   └── user.go
│
├── models                 数据库增删改查
│   ├── course.go
│   ├── db_postgres.go
│   ├── tiku.go
│   ├── token.go
│   └── user.go
│
├── configs                所有服务的配置文件
│   ├── conf-dev.ini
│   ├── config.go
│   └── conf.ini
│
├── error                  状态码常量
│   └── errorcode.go
│
├── log                    可以控制级别的日志输出
│   └── log.go
```

---
