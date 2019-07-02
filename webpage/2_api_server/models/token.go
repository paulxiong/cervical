package models

import (
	// logger "../log"
	"github.com/jinzhu/gorm"
	"time"
)

type Token struct {
	//Id == UserId
	Id        int64     `json:"id"         gorm:"column:id"          "ID"`
	UserId    int64     `json:"uid"        gorm:"column:uid"         "用户ID"`
	Token     string    `json:"token"      gorm:"column:token"       "token"`
	Expire    time.Time `json:"expire"     gorm:"column:expire"      "过期时间"`
	CreatedAt time.Time `json:"created_at" gorm:"column:created_at"  "创建时间"`
	UpdatedAt time.Time `json:"created_at" gorm:"column:created_at"  "更新时间"`
}

func (u *Token) BeforeCreate(scope *gorm.Scope) error {
	if u.CreatedAt.IsZero() {
		u.CreatedAt = time.Now()
	}
	if u.UpdatedAt.IsZero() {
		u.UpdatedAt = time.Now()
	}
	return nil
}

func (this *Token) UpdateToken(token string, expire time.Time) error {
	this.Id = this.UserId
	this.Expire = expire
	this.Token = token
	t := Token{Id: this.UserId}
	ret := db.Last(&t)
	if ret.Error != nil {
		ret2 := db.Create(this)
		if ret2.Error != nil {
			return ret2.Error
		} else {
			return nil
		}
	} else {
		this.UpdatedAt = time.Now()
		ret3 := db.Model(&t).Updates(this)
		if ret3.Error != nil {
			return ret3.Error
		} else {
			return nil
		}
	}
	return nil
}
