package controllers

import (
	jwt "github.com/appleboy/gin-jwt/v2"
	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	"github.com/paulxiong/cervical/webpage/2_api_server/middlewares"
	m "github.com/paulxiong/cervical/webpage/2_api_server/models"

	"github.com/gin-gonic/gin"
)

var AuthMiddleware *jwt.GinJWTMiddleware

func init() {
	var err error
	AuthMiddleware, err = middlewares.JwtMiddleware()
	if err != nil {
		logger.Error.Fatal("JWT Error:" + err.Error())
	}
}

type register struct {
	Email           string `form:"email" json:"email" example:"youremail@163.com 正确的邮箱格式" format:"string"`
	Mobile          string `form:"mobile" json:"mobile" binding:"required,max=11" example:"手机号码" format:"string"`
	Username        string `form:"username" json:"username" example:"用户名，英文数字组成" format:"string"`
	Password        string `form:"password" json:"password" binding:"required,max=124" example:"设置密码" format:"string"`
	ConfirmPassword string `form:"confirmPassword" json:"confirmPassword" binding:"required,eqfield=Password,max=124" example:"确认密码" format:"string"`
}

// RegisterUser 注册新用户
// @Description 注册新用户
// @Summary 注册
// @tags API1 用户
// @Accept  multipart/form-data
// @Produce json
// @Param Register body controllers.register true "注册信息表单"
// @Success 200 {string} json "{"data": "ok",	"status": 200}"
// @Success 200 {string} json "{"data": "User already exist",	"status": 70}"
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
// @Summary 用户信息
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

type login struct {
	Email    string `form:"email" json:"email" example:"youremail@163.com 正确的邮箱格式" format:"string"`
	Mobile   string `form:"mobile" json:"mobile" binding:"required,max=11" example:"手机号码" format:"string"`
	Username string `form:"username" json:"username" example:"用户名，英文数字组成" format:"string"`
	Password string `form:"password" json:"password" binding:"required,max=124" example:"用户密码" format:"string"`
}

// LoginUser 用户登录
// @Description 用户通过邮箱/用户名/手机号登录
// @Summary 登录
// @tags API1 用户
// @Accept  multipart/form-data
// @Produce json
// @Param Login body controllers.login true "登录信息表单"
// @Success 200 {string} json “{"expire": "当前token到期时间", "status": 200, "token": "token的字符串","user": {"id": 3,"mobile": "string","email": "string","name": "string","image": "http://workaiossqn.tiegushi.com/xdedu/images/touxiang.jpg","type_id": 1000,"created_at": "2019-09-12T10:05:39Z","updated_at": "2019-09-12T03:34:17Z"}}"
// @Router /user/login [post]
func LoginUser(c *gin.Context) {
	AuthMiddleware.LoginHandler(c)
	return
}

// LogoutUser 用户注销
// @Description 已经登录用户注销
// @Summary 已经登录用户注销
// @tags API1 用户
// @Accept json
// @Produce json
// @Success 200 {string} json “{"status": 200, "data": "ok"}"
// @Router /user/logout [post]
func LogoutUser(c *gin.Context) {
	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   "ok",
	})
	return
}

// CheckAuth 检查当前连接是否已经登录
func CheckAuth(c *gin.Context) {
	AuthMiddleware.MiddlewareFunc()(c)
	return
}
