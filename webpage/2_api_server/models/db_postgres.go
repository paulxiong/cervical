/*
参考文档:
http://gorm.book.jasperxu.com/
https://godoc.org/github.com/jinzhu/gorm
*/
package models

import (
	"time"

	configs "../configs"
	// logger "../log"

	"fmt"

	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/mysql"
)

var db *gorm.DB

func init() {
	var err error
	connArgs := fmt.Sprintf("%s:%s@(%s:%d)/%s?charset=utf8&parseTime=True&loc=Local",
		configs.MySql.User, configs.MySql.Password, configs.MySql.Host, configs.MySql.Port, configs.MySql.Database)
	db, err = gorm.Open("mysql", connArgs)
	if err != nil {
		panic(err)
	}
	db.LogMode(false)
	db.SingularTable(true)
	db.DB().SetMaxIdleConns(10)
	db.DB().SetConnMaxLifetime(time.Second)
	db.DB().SetMaxOpenConns(100)

	// db.AutoMigrate(&Token{}, &UserType{}, &User{})

	// UserTypeInit()
}
