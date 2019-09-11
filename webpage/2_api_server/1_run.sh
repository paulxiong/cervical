#!/bin/bash
export GIN_MODE='debug'
export SERVER_PORT=9000
export LOG_OUT='enable'
export LOG_GIN='enable'
export LOG_LEVEL='Info'
export MYSQL_HOST='192.168.1.102'
export MYSQL_PORT='3309'
export MYSQL_DB='datasets'
export MYSQL_USR='mysql'
export MYSQL_PASSWD='123456'
export EXPIRE_SECOND=2678400
export QINIU_ACCESSKEY='xxxxx'
export QINIU_SECRETKEY='xxxxx'
export QINIU_BUCKET='mass'
swag init
go run main.go
