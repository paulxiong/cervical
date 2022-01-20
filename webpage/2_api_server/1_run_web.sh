#!/bin/bash
export GIN_MODE='debug'
export SERVER_PORT=9000
export LOG_OUT='enable'
export LOG_GIN='enable'
export LOG_LEVEL='Info'
# export dev.medical.raidcdn.cn='192.168.1.74'
# export MYSQL_HOST='dev.medical.raidcdn.cn'
export MYSQL_HOST='192.168.1.77'
export MYSQL_PORT='3309'
export MYSQL_DB='datasets'
export MYSQL_USR='mysql'
export MYSQL_PASSWD='123456'
export MYSQL_PREFIX='c_'
export EMAIL_ENABLE='enable'
export EMAIL_USER='notify@youzhadahuo.com'
export EMAIL_PASSWD='b14e9665H60855cb'
export EMAIL_HOST='smtp.qiye.aliyun.com'
export EMAIL_PORT='465'
export ZONEINFO='/data/zoneinfo.zip'
export EXPIRE_SECOND=2678400
export QINIU_ACCESSKEY='xxxxx'
export QINIU_SECRETKEY='xxxxx'
export QINIU_BUCKET='mass'

# mkdir -p /data/datadir/thumbor/data/loader/cache
# mkdir -p /data/datadir/thumbor/data/loader/csv
# mkdir -p /data/datadir/thumbor/data/loader/datasets
# mkdir -p /data/datadir/thumbor/data/loader/img
# mkdir -p /data/datadir/thumbor/data/loader/modules/classifier
# mkdir -p /data/datadir/thumbor/data/loader/modules/detector
# mkdir -p /data/datadir/thumbor/data/loader/projects
# mkdir -p /data/datadir/thumbor/data/loader/scratch

ln -s /data_src/datadir/thumbor/data/loader/scratch ./scratch
ln -s /data_src/datadir/thumbor/data/loader/datasets ./datasets
ln -s /data_src/datadir/thumbor/data/loader/projects ./projects
ln -s /data_src/datadir/thumbor/data/loader/csv ./csv
ln -s /data_src/datadir/thumbor/data/loader/img ./img
ln -s /data_src/datadir/thumbor/data/loader/cache ./cache
ln -s /data/km/cervical ./ai
ln -s /data_src/ip2region.db ./ip2region.db
ln -s /data_src/zoneinfo.zip ./zoneinfo.zip


# need to copy files list :  main.exe configs/conf.ini web/dist/ web/src/const/errCode.json
swag init
go build -v -o main.exe -ldflags="-w -s" main.go
tar -czvmf release.tgz main.exe configs/conf.ini web/dist/ web/src/const/errCode.json
cp release.tgz /data
# pushd /data
# tar -xvmf release.tgz
# echo "entered /data and run main.exe"
./main.exe
# popd 

# swag init
# go run main.go
# pushd web
# npm run dev
# popd