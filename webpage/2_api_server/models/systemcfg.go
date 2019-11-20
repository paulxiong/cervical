package models

import (
	"time"

	"github.com/jinzhu/gorm"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
)

//Syscfg 系统配置的信息
type Syscfg struct {
	ID                   int       `json:"id"                     gorm:"column:id; primary_key"`        //记录ID
	Host                 string    `json:"host"                   gorm:"column:host"`                   //本服务域名+端口
	EmailRegisterContent string    `json:"email_register_content" gorm:"column:email_register_content"` //发送注册邮件的内容
	CreatedBy            int64     `json:"created_by"             gorm:"column:created_by"`             //创建者
	CreatedAt            time.Time `json:"created_at"             gorm:"column:created_at"`             //创建时间
	UpdatedAt            time.Time `json:"updated_at"             gorm:"column:updated_at"`             //更新时间
}

// BeforeCreate insert 之前的hook
func (s *Syscfg) BeforeCreate(scope *gorm.Scope) error {
	if s.CreatedAt.IsZero() {
		s.CreatedAt = time.Now()
	}
	if s.UpdatedAt.IsZero() {
		s.UpdatedAt = time.Now()
	}
	return nil
}

// UpdateSysCfg 更新系统配置的信息
func (s *Syscfg) UpdateSysCfg() (err error) {
	var updates map[string]interface{}
	updates = make(map[string]interface{})

	if s.Host != "" {
		updates["host"] = s.Host
	}
	if s.EmailRegisterContent != "" {
		updates["email_register_content"] = s.EmailRegisterContent
	}
	if len(updates) < 1 {
		return nil
	}

	ret := db.Model(s).Where("id=?", s.ID).Updates(updates)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return ret.Error
}

// FindSysCfg 查找系统配置信息
func FindSysCfg() (*Syscfg, error) {
	_s := Syscfg{}
	ret := db.Model(&_s).First(&_s)
	return &_s, ret.Error
}

// NewOrUpdateSysCfg 新建系统配置信息, 如果已经存在就更新
func (s *Syscfg) NewOrUpdateSysCfg() error {
	_s := Syscfg{}
	ret := db.Model(&_s).First(&_s)
	if ret.Error != nil || _s.ID < 1 {
		ret2 := db.Create(s)
		if ret2.Error != nil {
			return ret2.Error
		}
	}

	s.ID = _s.ID
	err := s.UpdateSysCfg()
	return err
}
