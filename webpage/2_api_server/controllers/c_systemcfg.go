package controllers

import (
	"strconv"

	"github.com/gin-gonic/gin"

	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
	models "github.com/paulxiong/cervical/webpage/2_api_server/models"
	res "github.com/paulxiong/cervical/webpage/2_api_server/responses"
)

// emailContent 邮件的格式
type emailContent struct {
	Content string `json:"content"` //邮件的html内容,字符串
	Type    int    `json:"type"`    //邮件的类型,0未知 1注册 2忘记密码
}

// EmailCfg 设置发送验证码的邮件的样式
// @Summary 设置发送验证码的邮件的样式
// @Description 设置发送验证码的邮件的样式，验证用000000代替，用户的邮箱用email@gmail.com代替。后台发送的时候通过字符串替换换成对应用户的邮箱和验证码
// @tags API1 系统（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param emailContent body controllers.emailContent true "邮件的html内容"
// @Success 200 {string} json "{"data": "ok",	"status": 200}"
// @Router /api1/emailcfg [POST]
func EmailCfg(c *gin.Context) {
	var ec emailContent
	err := c.ShouldBindJSON(&ec)
	if err != nil || ec.Type == 0 {
		res.ResFailedStatus(c, e.Errors["PostDataInvalied"])
		return
	}

	s := models.Syscfg{
		EmailRegisterContent: ec.Content,
	}
	if ec.Type == 2 {
		s.EmailRegisterContent = ""
		s.EmailForgotContent = ec.Content
	}

	err = s.NewOrUpdateSysCfg()
	if err != nil {
		res.ResFailedStatus(c, e.Errors["SystemSaveFailed"])
		return
	}
	res.ResSucceedString(c, "ok")
	return
}

// GetEmailCfg 获得当前发送验证码的邮件的样式
// @Summary 获得当前发送验证码的邮件的样式
// @Description 获得当前发送验证码的邮件的样式
// @tags API1 系统（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param type query string false "type, default 1, 0未知 1注册 2忘记密码"
// @Success 200 {object} models.Syscfg
// @Router /api1/emailcfg [GET]
func GetEmailCfg(c *gin.Context) {
	typeStr := c.DefaultQuery("type", "1")
	_type, _ := strconv.ParseInt(typeStr, 10, 32)

	s, err := models.FindSysCfg()
	if err != nil {
		res.ResFailedStatus(c, e.Errors["SystemNotFound"])
		return
	}
	if _type == 1 {
		s.EmailForgotContent = ""
	} else if _type == 2 {
		s.EmailRegisterContent = ""
	}

	res.ResSucceedStruct(c, s)
	return
}

// refererContent Referer配置
type refererContent struct {
	RefererEn     int64    `json:"referer_en"      example:"1"`                  //开启图片防盗链,0未知1关闭２开启
	Referers      []string `json:"referers"        example:"http://baidu.com"`   //防盗链白名单,http开头的字符串数组
	Referer404URL string   `json:"referer_404_url" example:"http://a.com/1.png"` //图片不存在,默认图片
	Referer401URL string   `json:"referer_401_url" example:"http://a.com/2.png"` //非法请求,默认图片
	ImgExpires    int      `json:"imgexpires"      example:"1"`                  //浏览器上图片缓存过期时间,单位是小时，最少一小时
}

// GetRefererCfg 获取图片服务的Referer配置
// @Summary 获取图片服务的Referer配置
// @Description　获取图片服务的Referer配置
// @tags API1 系统（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {object} controllers.refererContent
// @Router /api1/referercfg [GET]
func GetRefererCfg(c *gin.Context) {
	syscfg, _ := models.FindSysCfg()
	rc := refererContent{
		RefererEn:     syscfg.RefererEn,
		Referers:      syscfg.Referers2,
		Referer404URL: syscfg.Referer404URL,
		Referer401URL: syscfg.Referer401URL,
		ImgExpires:    syscfg.ImgExpires,
	}

	res.ResSucceedStruct(c, rc)
	return
}

// UpdateRefererCfg 配置图片服务的Referer
// @Summary 配置图片服务的Referer
// @Description　配置图片服务的Referer
// @tags API1 系统（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param refererContent body controllers.refererContent true "Referer配置"
// @Success 200 {string} json "{"data": "ok",	"status": 200}"
// @Router /api1/referercfg [POST]
func UpdateRefererCfg(c *gin.Context) {
	var rc refererContent
	err := c.ShouldBindJSON(&rc)
	if err != nil {
		res.ResFailedStatus(c, e.Errors["PostDataInvalied"])
		return
	}

	s := models.Syscfg{
		RefererEn:     rc.RefererEn,
		Referers2:     rc.Referers,
		Referer404URL: rc.Referer404URL,
		Referer401URL: rc.Referer401URL,
		ImgExpires:    rc.ImgExpires,
	}

	err = s.NewOrUpdateSysCfg()
	if err != nil {
		res.ResFailedStatus(c, e.Errors["SystemSaveFailed"])
		return
	}
	res.ResSucceedString(c, "ok")
	return
}
