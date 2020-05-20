package models

import (
	"time"

	"github.com/jinzhu/gorm"
	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
)

// Email 邮件信息
type Email struct {
	ID        int64     `json:"id"         gorm:"column:id"`         // ID
	ToAddr    string    `json:"toaddr"     gorm:"column:toaddr"`     //接收邮箱地址
	FromAddr  string    `json:"fromaddr"   gorm:"column:fromaddr"`   //用哪个邮箱发送的
	MailType  int       `json:"mailtype"   gorm:"column:mailtype"`   //类型 0未知1注册2忘记密码
	Status    int       `json:"status"     gorm:"column:status"`     //发送状态 0未发送1已发送2发送失败
	Exire     time.Time `json:"exire"      gorm:"column:exire"`      //失效时间 超过这个时间邮件失效
	Valid     int       `json:"valid"      gorm:"column:valid"`      //是否有效 0失效1有效2永久有效
	Code      string    `json:"code"       gorm:"column:code"`       //邮件发送的验证码
	Content   string    `json:"content"    gorm:"column:content"`    //邮件文本内容 邮件的正文部分
	CreatedAt time.Time `json:"created_at" gorm:"column:created_at"` //创建时间
	UpdatedAt time.Time `json:"updated_at" gorm:"column:updated_at"` //更新时间
}

// BeforeCreate insert之前的hook
func (em *Email) BeforeCreate(scope *gorm.Scope) error {
	if em.CreatedAt.IsZero() {
		em.CreatedAt = time.Now()
	}
	if em.UpdatedAt.IsZero() {
		em.UpdatedAt = time.Now()
	}
	if em.Exire.IsZero() {
		em.Exire = time.Now()
	}
	return nil
}

// NeEmail 新建邮件
func (em *Email) NeEmail() error {
	ret := db.Create(em)
	if ret.Error != nil {
		return ret.Error
	}
	return nil
}

// UpdateEmail 邮件发送成功或者失败，更新状态到数据库
func (em *Email) UpdateEmail() (e error) {
	ret := db.Model(em).Where("id=?", em.ID).Updates(em)
	if ret.Error != nil {
		logger.Info(ret.Error)
	}
	return ret.Error
}

// UpdateEmailInvalid 邮件验证过了，标记成invalid
func (em *Email) UpdateEmailInvalid() (e error) {
	if em.ID == 0 {
		return nil
	}
	em.Valid = 0
	ret := db.Model(em).Where("id=?", em.ID).Updates(em)
	if ret.Error != nil {
		logger.Info(ret.Error)
	}
	return ret.Error
}

// FindEmailbyToAddr 通过接收方邮箱查找记录
func FindEmailbyToAddr(toaddr string) (*Email, error) {
	em := new(Email)
	ret := db.Where("toaddr = ?", toaddr).Order("created_at DESC").First(&em)
	if ret.Error != nil {
		return em, ret.Error
	}
	return em, nil
}

// CheckEmailCodeValied 检查验证码是否正确，邮件是否有效
func CheckEmailCodeValied(toaddr string, code string) (bool, *Email, int) {
	em, err := FindEmailbyToAddr(toaddr)
	if err != nil {
		return false, em, e.Errors["VerifyEmailNotFound"]
	}
	//过期了
	if time.Now().After(em.Exire) {
		return false, em, e.Errors["VerifyExpired"]
	}
	//失效了，没发送成功, 没找到邮件记录
	if em.Valid == 0 || em.Status != 1 || em.Code != code {
		return false, em, e.Errors["VerifyInvalied"]
	}
	return true, em, e.Errors["Succeed"]
}
