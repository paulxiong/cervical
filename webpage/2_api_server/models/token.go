package models

import (
	// logger "../log"
	"time"

	"github.com/jinzhu/gorm"
)

// Token token信息
type Token struct {
	//Id == UserId
	ID        int64     `json:"id"         gorm:"column:id"`         // ID
	UserID    int64     `json:"uid"        gorm:"column:uid"`        // 用户ID
	Token     string    `json:"token"      gorm:"column:token"`      // token
	Expire    time.Time `json:"expire"     gorm:"column:expire"`     // 过期时间
	CreatedAt time.Time `json:"created_at" gorm:"column:created_at"` // 创建时间
	UpdatedAt time.Time `json:"updated_at" gorm:"column:updated_at"` // 更新时间
}

// BeforeCreate insert token之前的hook
func (u *Token) BeforeCreate(scope *gorm.Scope) error {
	if u.CreatedAt.IsZero() {
		u.CreatedAt = time.Now()
	}
	if u.UpdatedAt.IsZero() {
		u.UpdatedAt = time.Now()
	}
	return nil
}

// UpdateToken token存在更新到数据库，不存在则新建
func (newtoken *Token) UpdateToken(token string, expire time.Time) error {
	newtoken.ID = newtoken.UserID
	newtoken.Expire = expire
	newtoken.Token = token
	t := Token{ID: newtoken.UserID}
	ret := db.Last(&t)
	if ret.Error != nil {
		ret2 := db.Create(newtoken)
		if ret2.Error != nil {
			return ret2.Error
		} else {
			return nil
		}
	} else {
		newtoken.UpdatedAt = time.Now()
		ret3 := db.Model(&t).Updates(newtoken)
		if ret3.Error != nil {
			return ret3.Error
		} else {
			return nil
		}
	}
}
