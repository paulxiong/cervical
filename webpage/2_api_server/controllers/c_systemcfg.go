package controllers

import (
	"github.com/gin-gonic/gin"

	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
	models "github.com/paulxiong/cervical/webpage/2_api_server/models"
	res "github.com/paulxiong/cervical/webpage/2_api_server/responses"
)

// emailContent 邮件的格式
type emailContent struct {
	Content string `json:"content"` //邮件的html内容,字符串
}

// RegisterEmailCfg 设置发送验证码的邮件的样式
// @Summary 设置发送验证码的邮件的样式
// @Description 设置发送验证码的邮件的样式，验证用000000代替，用户的邮箱用email@gmail.com代替。后台发送的时候通过字符串替换换成对应用户的邮箱和验证码
// @tags API1 系统（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param emailContent body controllers.emailContent true "邮件的html内容"
// @Success 200 {string} json "{"data": "ok",	"status": 200}"
// @Router /api1/registeremailcfg [POST]
func RegisterEmailCfg(c *gin.Context) {
	var ec emailContent
	err := c.ShouldBindJSON(&ec)
	if err != nil {
		res.ResFailedStatus(c, e.Errors["PostDataInvalied"])
		return
	}

	s := models.Syscfg{
		EmailRegisterContent: ec.Content,
	}

	err = s.NewOrUpdateSysCfg()
	if err != nil {
		res.ResFailedStatus(c, e.Errors["SystemSaveFailed"])
		return
	}
	res.ResSucceedString(c, "ok")
	return
}

// GetRegisterEmailCfg 获得当前发送验证码的邮件的样式
// @Summary 获得当前发送验证码的邮件的样式
// @Description 获得当前发送验证码的邮件的样式
// @tags API1 系统（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {object} models.Syscfg
// @Router /api1/registeremailcfg [GET]
func GetRegisterEmailCfg(c *gin.Context) {
	s, err := models.FindSysCfg()
	if err != nil {
		res.ResFailedStatus(c, e.Errors["SystemNotFound"])
		return
	}

	res.ResSucceedStruct(c, s)
	return
}
