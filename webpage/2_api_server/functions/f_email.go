package function

import (
	"strconv"
	"time"

	"gopkg.in/gomail.v2"

	configs "github.com/paulxiong/cervical/webpage/2_api_server/configs"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	m "github.com/paulxiong/cervical/webpage/2_api_server/models"
	util "github.com/paulxiong/cervical/webpage/2_api_server/utils"
)

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
	m.SetHeader("From", m.FormatAddress(mailConn["user"], "讯动医疗")) //这种方式可以添加别名
	m.SetHeader("To", mailTo...)                                   //发送给多个用户
	m.SetHeader("Subject", subject)                                //设置邮件主题
	m.SetBody("text/html", body)                                   //设置邮件正文

	d := gomail.NewDialer(mailConn["host"], port, mailConn["user"], mailConn["pass"])

	err := d.DialAndSend(m)
	return err
}

// SendEmailCode 发送注册/忘记密码时候的邮箱验证码
func SendEmailCode(toaddr string, _type int) error {
	code := util.GetRandomStringNum(6)
	newemail := m.Email{
		ID:       0,
		ToAddr:   toaddr,
		FromAddr: configs.Email.User,
		MailType: _type,
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
	subject := "验证码"           //邮件主题
	body := code               // 邮件正文

	// 查找系统配置里面的邮件样式
	emailbody := m.GetEmailBody(toaddr, code, _type)
	if len(emailbody) > 0 {
		body = emailbody
	}
	//0未知1注册2忘记密码
	if _type == 1 {
		subject = "注册码"
	}

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
