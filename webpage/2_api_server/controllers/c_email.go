package controllers

import (
	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
	f "github.com/paulxiong/cervical/webpage/2_api_server/functions"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	m "github.com/paulxiong/cervical/webpage/2_api_server/models"
	res "github.com/paulxiong/cervical/webpage/2_api_server/responses"

	"github.com/gin-gonic/gin"
)

type mailregister struct {
	Email string `form:"email" json:"email" example:"youremail@163.com"` // 用户的邮箱地址
	Type  int    `form:"type"  json:"type"  example:"1"`                 // 验证码类型, 0未知 1注册 2忘记密码
}

// GetEmailCode 用户获取邮箱验证码
// @Description 用户获取邮箱验证码
// @Summary 用户获取邮箱验证码
// @tags API1 用户
// @Accept  multipart/form-data
// @Produce json
// @Param Email body controllers.mailregister true "注册信息表单"
// @Success 200 {string} json "{"status": 200, "data": "ok"}"
// @Router /user/emailcode [POST]
func GetEmailCode(c *gin.Context) {
	var user m.User
	var mcode mailregister
	err := c.ShouldBindJSON(&mcode)
	if err != nil {
		logger.Info(err)
		res.ResFailedStatus(c, e.Errors["EmailCodeInvalidData"])
		return
	}

	user.Email = mcode.Email
	exituser, _ := user.CheckUserExist()
	if mcode.Type == 1 {
		if exituser != nil {
			res.ResFailedStatus(c, e.Errors["RegisterUserExisted"])
			return
		}
	} else if mcode.Type == 2 {
		if exituser == nil || exituser.ID < 1 {
			res.ResFailedStatus(c, e.Errors["PasswdUpdateEmailNotFound"])
			return
		}
	} else {
		res.ResFailedStatus(c, e.Errors["EmailCodeunknown"])
		return
	}

	err = f.SendEmailCode(mcode.Email, mcode.Type)
	if err != nil {
		logger.Info(err)
		res.ResFailedStatus(c, e.Errors["EmailCodeSendFailed"])
		return
	}

	res.ResSucceedString(c, "ok")
	return
}
