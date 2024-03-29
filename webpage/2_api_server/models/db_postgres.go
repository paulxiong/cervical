package models

/*
参考文档:
http://gorm.book.jasperxu.com/
https://godoc.org/github.com/jinzhu/gorm
*/

import (
	"fmt"
	"time"

	configs "github.com/paulxiong/cervical/webpage/2_api_server/configs"

	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/mysql" //mysql
)

var db *gorm.DB
var userTypes map[int]string

func init() {
	var err error
	connArgs := fmt.Sprintf("%s:%s@(%s:%d)/%s?charset=utf8&parseTime=True&loc=Local",
		configs.MySQL.User, configs.MySQL.Password, configs.MySQL.Host, configs.MySQL.Port, configs.MySQL.Database)
	db, err = gorm.Open("mysql", connArgs)
	if err != nil {
		panic(err)
	}

	//设置默认表名前缀
	gorm.DefaultTableNameHandler = func(db *gorm.DB, defaultTableName string) string {
		return configs.MySQL.Prefix + defaultTableName
	}
	db.LogMode(false)
	db.SingularTable(true)
	db.DB().SetMaxIdleConns(10)
	db.DB().SetConnMaxLifetime(time.Second)
	db.DB().SetMaxOpenConns(100)

	// db.AutoMigrate(&Token{}, &UserType{}, &User{})

	userTypes, _ = UserTypeInit()
}
