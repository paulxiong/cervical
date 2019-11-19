package controllers

import (
	"strconv"

	jwt "github.com/appleboy/gin-jwt/v2"
	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	mid "github.com/paulxiong/cervical/webpage/2_api_server/middlewares"
	m "github.com/paulxiong/cervical/webpage/2_api_server/models"

	"github.com/gin-gonic/gin"
)

// AuthMiddleware jwt的全局变量
var AuthMiddleware *jwt.GinJWTMiddleware

func init() {
	var err error
	AuthMiddleware, err = mid.JwtMiddleware()
	if err != nil {
		logger.Error.Fatal("JWT Error:" + err.Error())
	}
}

type register struct {
	Email           string `form:"email" json:"email" example:"youremail@163.com 正确的邮箱格式" format:"string"`
	EmailCode       string `form:"emailcode" json:"emailcode" example:"123456正确的验证码" format:"string"`
	Mobile          string `form:"mobile" json:"mobile" binding:"max=11" example:"手机号码" format:"string"`
	Username        string `form:"username" json:"username" example:"用户名，英文数字组成" format:"string"`
	Password        string `form:"password" json:"password" binding:"required,max=124" example:"设置密码" format:"string"`
	ConfirmPassword string `form:"confirmPassword" json:"confirmPassword" binding:"required,eqfield=Password,max=124" example:"确认密码" format:"string"`
}

// RegisterUser 注册新用户
// @Description 注册新用户 code: 200 注册请求成功,  406 注册失败
// @Description status：
// @Description 78 验证码无效
// @Description 76 手机号已经注册过
// @Description 75 表单数据错误
// @Description 74 新建用户失败
// @Description 73 表单数据不对（密码或手机号/邮箱/用户名为空）
// @Description 72 两次密码不一致
// @Description 71 邮箱已经注册过
// @Description 70 用户已经存在
// @Description 200 注册成功
// @Summary 注册
// @tags API1 用户
// @Accept  multipart/form-data
// @Produce json
// @Param Register body controllers.register true "注册信息表单"
// @Success 200 {string} json "{"data": "ok",	"status": 200}"
// @Failure 406 {string} json "{"data": "register faild", "status": 错误码}"
// @Router /user/register [post]
func RegisterUser(c *gin.Context) {
	var reg register
	var user m.User
	err := c.ShouldBindJSON(&reg)
	if err != nil {
		c.JSON(e.StatusNotAcceptable, gin.H{
			"status": e.StatusRegisterError75,
			"data":   "register faild",
		})
		return
	}

	user.Password = reg.Password
	user.Name = reg.Username
	user.Email = reg.Email
	user.Mobile = reg.Mobile
	user.TypeID = 1000 //普通用户TypeId=1000
	user.Image = "http://workaiossqn.tiegushi.com/xdedu/images/touxiang.jpg"

	if user.Password == "" || (user.Name == "" && user.Email == "" && user.Mobile == "") {
		logger.Warning.Println("RegisterUser failed ", user)
		c.JSON(e.StatusNotAcceptable, gin.H{
			"status": e.StatusRegisterInvalidData73,
			"data":   "register faild",
		})
		return
	}

	exituser, errorcode := user.CheckUserExist()
	if exituser != nil {
		c.JSON(e.StatusNotAcceptable, gin.H{
			"status": errorcode,
			"data":   "register faild",
		})
		return
	}

	//检查如果是邮箱注册，必须检查验证码的合法
	if user.Email != "" {
		valid, em, codeerr := m.CheckEmailCodeValied(user.Email, reg.EmailCode)
		if codeerr != nil || valid == false {
			c.JSON(e.StatusNotAcceptable, gin.H{
				"status": e.StatusRegisterMailInvalid78,
				"data":   "register faild",
			})
			return
		}
		//校验完之后丢弃这个校验码
		em.UpdateEmailInvalid()
	}

	err = user.Newuser()
	if err != nil {
		c.JSON(e.StatusNotAcceptable, gin.H{
			"status": e.StatusRegisterNewUserFailed74,
			"data":   "register faild",
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
// @Description 获得当前用户信息 code: 200 用户信息获取成功  401 未登录
// @Description status: 200 成功  其他: 未登录
// @Summary 用户信息
// @tags API1 用户（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {string} json "{"data": "ok",	"status": 200}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /user/userinfo [get]
func GetUser(c *gin.Context) {
	u, _ := m.GetUserFromContext(c)

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   u,
	})
	return
}

// OptionUser option请求
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
// @Description 用户通过邮箱/用户名/手机号登录 	status: 60-密码错误  61-用户不存在 63-登录失败 64-表单数据错误
// @Description
// @Summary 登录
// @tags API1 用户
// @Accept  json
// @Produce json
// @Param Login body middlewares.LoginFormData true "登录信息表单"
// @Success 200 {string} json "{"expire": "当前token到期时间", "status": 200, "token": "token的字符串","user": {"id": 3,"mobile": "string","email": "string","name": "string","image": "http://workaiossqn.tiegushi.com/xdedu/images/touxiang.jpg","type_id": 1000,"created_at": "2019-09-12T10:05:39Z","updated_at": "2019-09-12T03:34:17Z"}}"
// @Failure 401 {string} json "{"data": "login faild", "status": 错误码}"
// @Router /user/login [post]
func LoginUser(c *gin.Context) {
	AuthMiddleware.LoginHandler(c)
	return
}

// LogoutUser 用户注销
// @Description 已经登录用户注销
// @Summary 已经登录用户注销
// @tags API1 用户（需要认证）
// @Security ApiKeyAuth
// @Accept json
// @Produce json
// @Success 200 {string} json “{"status": 200, "data": "ok"}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /user/logout [get]
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

type mailregister struct {
	Email string `form:"email" json:"email" example:"youremail@163.com 正确的邮箱格式" format:"string"`
}

// GetEmailCode 用户注册时候获取邮箱验证码
// @Description 注册时候获取邮箱验证码
// @Summary 用户注册时候获取邮箱验证码
// @Description status：
// @Description 71 邮箱已经注册过
// @Description 73 表单数据不对（邮箱为空或格式不对）
// @Description 77 邮件发送出错
// @tags API1 用户
// @Accept  multipart/form-data
// @Produce json
// @Param Register body controllers.mailregister true "注册信息表单"
// @Success 200 {string} json “{"status": 200, "data": "ok"}"
// @Failure 406 {string} json "{"data": "", "status": 错误码}"
// @Router /user/emailcode [POST]
func GetEmailCode(c *gin.Context) {
	var user m.User
	var mregister mailregister
	err := c.ShouldBindJSON(&mregister)
	if err != nil {
		logger.Info.Println(err)
		c.JSON(e.StatusNotAcceptable, gin.H{
			"status": e.StatusRegisterInvalidData73,
			"data":   "send mail faild",
		})
		return
	}

	user.Email = mregister.Email
	exituser, errorcode := user.CheckUserExist()
	if exituser != nil {
		logger.Info.Println(err)
		c.JSON(e.StatusNotAcceptable, gin.H{
			"status": errorcode,
			"data":   "email exist",
		})
		return
	}

	err = m.SendRegisterCode(mregister.Email)
	if err != nil {
		logger.Info.Println(err)
		c.JSON(e.StatusNotAcceptable, gin.H{
			"status": e.StatusRegisterMailFailed77,
			"data":   "sent email failed",
		})
		return

	}

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   "ok",
	})
	return
}

// History 用户信息
func History(c *gin.Context) {
	mid.History()(c)
	return
}

type listOperationlog struct {
	Operationlog []m.Operationlog `json:"accesslog"`
	Total        int64            `json:"total"`
}

// GetAccessLog 按数据库存储顺序依次获得用户访问记录
// @Summary 按数据库存储顺序依次获得用户访问记录
// @Description 按数据库存储顺序依次获得用户访问记录
// @tags API1 用户（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param limit query string false "limit, default 1"
// @Param skip query string false "skip, default 0"
// @Param order query string false "order, default 1, 1倒序，0顺序，顺序是指创建时间"
// @Success 200 {object} models.Operationlog
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /user/accesslog [get]
func GetAccessLog(c *gin.Context) {
	limitStr := c.DefaultQuery("limit", "1")
	skipStr := c.DefaultQuery("skip", "0")
	orderStr := c.DefaultQuery("order", "1")
	limit, _ := strconv.ParseInt(limitStr, 10, 64)
	skip, _ := strconv.ParseInt(skipStr, 10, 64)
	_order, _ := strconv.ParseInt(orderStr, 10, 64)

	total, ds, err := m.ListOperationlog(int(limit), int(skip), int(_order))
	if err != nil {
		logger.Info.Println(err)
	}
	/*
		for idx, v := range ds {
			ds[idx].CreatedAtTs = v.CreatedAt.Unix() * 1000
			ds[idx].StartTimeTs = v.StartTime.Unix() * 1000
		}
	*/

	dts := listOperationlog{}
	dts.Operationlog = ds
	dts.Total = total

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   dts,
	})
	return
}

// GetUserLists 按数据库存储顺序依次获得所有用户信息
// @Summary 按数据库存储顺序依次获得所有用户信息
// @Description 按数据库存储顺序依次获得所有用户信息
// @tags API1 用户（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param limit query string false "limit, default 100"
// @Param skip query string false "skip, default 0"
// @Param order query string false "order, default 1, 1倒序，0顺序，顺序是指创建时间"
// @Success 200 {object} models.User
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /user/lists [get]
func GetUserLists(c *gin.Context) {
	limitStr := c.DefaultQuery("limit", "100")
	skipStr := c.DefaultQuery("skip", "0")
	orderStr := c.DefaultQuery("order", "1")
	limit, _ := strconv.ParseInt(limitStr, 10, 32)
	skip, _ := strconv.ParseInt(skipStr, 10, 32)
	_order, _ := strconv.ParseInt(orderStr, 10, 32)

	users, total, err := m.UserLists(int(limit), int(skip), int(_order))
	if err != nil {
		logger.Info.Println(err)
	}
	ResStructTotal(c, users, total)
	return
}

// updateUser 修改用户信息
type updateUser struct {
	Mobile       string `json:"mobile"       example:"111222222"`                                                 //手机号
	Email        string `json:"email"        example:"mail@163.com"`                                              //邮箱
	Name         string `json:"name"         example:"username"`                                                  //用户名
	Introduction string `json:"introduction" example:"abc"`                                                       //文字介绍
	Image        string `json:"image"        example:"http://workaiossqn.tiegushi.com/xdedu/images/touxiang.jpg"` //用户头像
}

// UpdateUserInfo 修改当前用户信息
// @Summary 修改当前用户信息
// @Description 修改当前用户信息
// @tags API1 用户（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param Register body controllers.updateUser true "修改当前用户信息"
// @Success 200 {string} json “{"status": 200, "data": "ok"}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /user/updateinfo [post]
func UpdateUserInfo(c *gin.Context) {
	uu := updateUser{}
	err := c.ShouldBindJSON(&uu)
	u, _ := m.GetUserFromContext(c)
	if err != nil || u.ID < 1 {
		ResString(c, "invalied user update")
		return
	}

	userinfo := &m.User{
		ID:           u.ID,
		Mobile:       uu.Mobile,
		Email:        uu.Email,
		Name:         uu.Name,
		Image:        uu.Image,
		Introduction: uu.Introduction,
	}

	err2 := userinfo.UpdateUserInfo()
	if err2 != nil {
		ResString(c, "update user info failed")
	}

	ResString(c, "ok")
	return
}
