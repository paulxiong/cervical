package models

import (
	"time"

	"github.com/jinzhu/gorm"
)

//ErrorLog 错误日志
type ErrorLog struct {
	ID        int64     `json:"id"            gorm:"column:id"          example:"1"`            //ID
	Type      int       `json:"type"          gorm:"column:type"        example:"0"`            //类型, 0前端
	Opid      int64     `json:"opid"          gorm:"column:opid"        example:"12"`           //左上角X
	Errlog    string    `json:"errlog"        gorm:"column:errlog"      example:"error string"` //左上角Y
	CreatedBy int64     `json:"created_by"    gorm:"column:created_by"`                         //创建者
	CreatedAt time.Time `json:"created_time"  gorm:"column:created_at"`
	UpdatedAt time.Time `json:"updated_time"  gorm:"column:updated_at"`
}

// BeforeCreate insert之前的hook
func (err *ErrorLog) BeforeCreate(scope *gorm.Scope) error {
	if err.CreatedAt.IsZero() {
		err.CreatedAt = time.Now()
	}
	if err.UpdatedAt.IsZero() {
		err.UpdatedAt = time.Now()
	}
	return nil
}

// NewErrorLog 新建错误日志
func (err *ErrorLog) NewErrorLog() error {
	ret := db.Model(err).Create(err)
	if ret.Error != nil {
		return ret.Error
	}
	return nil
}
