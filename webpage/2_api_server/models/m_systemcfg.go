package models

import (
	"strings"
	"time"

	"github.com/jinzhu/gorm"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	u "github.com/paulxiong/cervical/webpage/2_api_server/utils"
)

// SystemCfg 全局变量！！目的避免每次读取数据库
var SystemCfg *Syscfg

//Syscfg 系统配置的信息
type Syscfg struct {
	ID                   int       `json:"id"                     gorm:"column:id; primary_key"`        //记录ID
	Host                 string    `json:"host"                   gorm:"column:host"`                   //本服务域名+端口
	EmailRegisterContent string    `json:"email_register_content" gorm:"column:email_register_content"` //发送注册邮件的内容
	EmailForgotContent   string    `json:"email_forgot_content"   gorm:"column:email_forgot_content"`   //发送忘记密码邮件的格式
	RefererEn            int64     `json:"referer_en"             gorm:"column:referer_en"`             //开启图片防盗链,0未知1关闭２开启
	Referers             string    `json:"-"                      gorm:"column:referers"`               //防盗链白名单,http开头的字符串数组
	Referers2            []string  `json:"referers"               gorm:"-"`                             //防盗链白名单,http开头的字符串数组,前端
	Referer404URL        string    `json:"referer_404_url"        gorm:"column:referer_404_url"`        //图片不存在,默认图片
	Referer401URL        string    `json:"referer_401_url"        gorm:"column:referer_401_url"`        //非法请求,默认图片
	ImgExpires           int       `json:"imgexpires"             gorm:"column:imgexpires"`             //浏览器上图片缓存过期时间,单位是小时
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
	str, err := u.StrArray2String(&s.Referers2)
	if err == nil {
		s.Referers = str
	}
	return nil
}

// AfterFind 把数据库里面存的字符串转成数组返回
func (s *Syscfg) AfterFind(scope *gorm.Scope) error {
	if s.Referers != "" {
		arr, err := u.String2StrArray(s.Referers)
		if err == nil {
			s.Referers2 = arr
		}
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
	if s.EmailForgotContent != "" {
		updates["email_forgot_content"] = s.EmailForgotContent
	}
	if s.Referer404URL != "" {
		updates["referer_404_url"] = s.Referer404URL
	}
	if s.Referer401URL != "" {
		updates["referer_401_url"] = s.Referer401URL
	}
	if s.RefererEn > 0 {
		updates["referer_en"] = s.RefererEn
	}
	str, err := u.StrArray2String(&s.Referers2)
	if err == nil {
		updates["referers"] = str
	}
	if s.ImgExpires > 0 {
		updates["imgexpires"] = s.ImgExpires
	}

	if len(updates) < 1 {
		return nil
	}

	ret := db.Model(s).Where("id=?", s.ID).Updates(updates)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	SystemCfg, _ = FindSysCfg()
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

// GetEmailBody 根据注册码和邮箱地址生成邮件内容
func GetEmailBody(toaddr string, code string, _type int) string {
	_s, err := FindSysCfg()
	if err != nil || len(_s.EmailRegisterContent) < 1 {
		return ""
	}

	emailbody := strings.Replace(_s.EmailRegisterContent, "email@gmail.com", toaddr, -1)
	if _type == 2 {
		emailbody = strings.Replace(_s.EmailForgotContent, "email@gmail.com", toaddr, -1)
	}
	emailbody = strings.Replace(emailbody, "000000", code, -1)
	return emailbody
}

func init() {
	SystemCfg, _ = FindSysCfg()
}
