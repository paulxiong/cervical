package models

import (
	"strconv"
	"time"

	"gopkg.in/gomail.v2"

	"github.com/jinzhu/gorm"
	configs "github.com/paulxiong/cervical/webpage/2_api_server/configs"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	util "github.com/paulxiong/cervical/webpage/2_api_server/utils"
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
		logger.Info.Println(ret.Error)
	}
	return ret.Error
}

// UpdateEmailInvalid 邮件验证过了，标记成invalid
func (em *Email) UpdateEmailInvalid() (e error) {
	em.Valid = 0
	ret := db.Model(em).Where("id=?", em.ID).Updates(em)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
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
func CheckEmailCodeValied(toaddr string) (bool, *Email, error) {
	em, err := FindEmailbyToAddr(toaddr)
	if err != nil {
		return false, em, err
	}
	//过期了,失效了，没发送成功, 没找到邮件记录
	if time.Now().Before(em.Exire) || em.Valid == 0 || em.Status != 1 || em.ID < 1 {
		return false, em, err
	}
	return true, em, err
}

// sendMail 发送电子邮件
func sendMail(mailTo []string, subject string, body string) error {
	//定义邮箱服务器连接信息，如果是阿里邮箱 pass填密码，qq邮箱填授权码
	mailConn := map[string]string{
		"user": configs.Email.User,
		"pass": configs.Email.Passwd,
		"host": configs.Email.Host,
		"port": configs.Email.Port,
	}

	//转换端口类型为int
	port, _ := strconv.Atoi(mailConn["port"])

	m := gomail.NewMessage()
	m.SetHeader("From", "Register"+"<"+mailConn["user"]+">") //这种方式可以添加别名，即"Register"， 也可以直接用<code>m.SetHeader("From",mailConn["user"])</code> 读者可以自行实验下效果
	m.SetHeader("To", mailTo...)                             //发送给多个用户
	m.SetHeader("Subject", subject)                          //设置邮件主题
	m.SetBody("text/html", body)                             //设置邮件正文

	d := gomail.NewDialer(mailConn["host"], port, mailConn["user"], mailConn["pass"])

	err := d.DialAndSend(m)
	return err
}

// SendRegisterCode 发送注册时候的邮箱验证码
func SendRegisterCode(toaddr string) error {
	code := util.GetRandomStringNum(6)
	newemail := Email{
		ID:       0,
		ToAddr:   toaddr,
		FromAddr: configs.Email.User,
		MailType: 1,
		Status:   0,
		Valid:    1,
		Code:     code,
		Content:  code,
	}

	err := newemail.NeEmail()
	if err != nil {
		logger.Info.Println(err)
		return err
	}

	// 邮件十分钟之内有效
	m10, _ := time.ParseDuration("10m")
	newemail.Exire = newemail.CreatedAt.Add(m10)
	newemail.Valid = 1
	newemail.Status = 1

	mailTo := []string{toaddr} //定义收件人
	subject := "注册码"           //邮件主题
	body := code               // 邮件正文
	err = sendMail(mailTo, subject, body)
	if err != nil {
		logger.Info.Println(err)
		newemail.Status = 2
		newemail.Valid = 0
	}

	err2 := newemail.UpdateEmail()
	if err2 != nil {
		logger.Info.Println(err2)
	}
	return err
}
