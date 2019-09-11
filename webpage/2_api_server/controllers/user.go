package controllers

import (
	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	m "github.com/paulxiong/cervical/webpage/2_api_server/models"

	"github.com/gin-gonic/gin"
)

type register struct {
	Email           string `form:"email" json:"email"`
	Mobile          string `form:"mobile" json:"mobile" binding:"required,max=11"`
	Username        string `form:"username" json:"username"`
	Password        string `form:"password" json:"password" binding:"required,max=124"`
	ConfirmPassword string `form:"confirmPassword" json:"confirmPassword" binding:"required,eqfield=Password,max=124"`
}

// RegisterUser 注册新用户
// @Description 注册新用户
// @tags API1 用户
// @Accept  json
// @Produce json
// @Param Email formData string false "邮箱"
// @Param Mobile formData string true "手机号码"
// @Param Username formData string false "用户名"
// @Param Password formData string true "密码"
// @Param ConfirmPassword formData string true "确认密码"
// @Success 200 {string} json "{"data": "ok",	"status": 200}"
// @Router /user/register [post]
func RegisterUser(c *gin.Context) {
	var reg register
	var user m.User
	err := c.BindJSON(&reg)
	if err != nil {
		c.JSON(e.StatusReqOK, gin.H{
			"status": e.StatusRegisterError,
			"data":   "RegisterUser failed",
		})
		return
	}
	user.Password = reg.Password
	user.Name = reg.Username
	user.Email = reg.Email
	user.Mobile = reg.Mobile
	user.TypeId = 1000 //普通用户TypeId=1000
	user.Image = "http://workaiossqn.tiegushi.com/xdedu/images/touxiang.jpg"

	if user.Password == "" ||
		user.Mobile == "" {
		logger.Warning.Println("RegisterUser failed ", user)
		c.JSON(e.StatusReqOK, gin.H{
			"status": e.StatusRegisterInvalidData,
			"data":   "RegisterUser failed",
		})
		return
	}

	exituser, errorcode := user.CheckUserExist()
	if exituser != nil {
		c.JSON(e.StatusReqOK, gin.H{
			"status": errorcode,
			"data":   "User already exist",
		})
		return
	}

	err = user.Newuser()
	if err != nil {
		c.JSON(e.StatusReqOK, gin.H{
			"status": e.StatusRegisterNewUserFailed,
			"data":   "User already exist",
		})
		return
	}

	logger.Info.Println("RegisterUser succsess ", user)
	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   "ok",
	})
	return
}

// GetUser 获得当前用户信息
// @Description 获得当前用户信息
// @tags API1 用户
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {string} json "{"data": "ok",	"status": 200}"
// @Router /api1/userinfo [get]
func GetUser(c *gin.Context) {
	u, _ := m.GetUserFromContext(c)

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   u,
	})
	return
}

func OptionUser(c *gin.Context) {
	c.JSON(e.StatusReqOK, gin.H{"status": e.StatusSucceed})
	return
}
