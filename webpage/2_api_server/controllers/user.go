package controllers

import (
	e "../error"
	logger "../log"
	m "../models"

	"github.com/gin-gonic/gin"
)

type register struct {
	Email           string `form:"email" json:"email"`
	Mobile          string `form:"mobile" json:"mobile" binding:"required,max=11"`
	Username        string `form:"username" json:"username"`
	Password        string `form:"password" json:"password" binding:"required,max=124"`
	ConfirmPassword string `form:"confirmPassword" json:"confirmPassword" binding:"required,eqfield=Password,max=124"`
}

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