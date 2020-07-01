package controllers

import (
	"strconv"

	jwt "github.com/appleboy/gin-jwt/v2"
	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	mid "github.com/paulxiong/cervical/webpage/2_api_server/middlewares"
	m "github.com/paulxiong/cervical/webpage/2_api_server/models"
	res "github.com/paulxiong/cervical/webpage/2_api_server/responses"

	"github.com/gin-gonic/gin"
)

// AuthMiddleware jwt的全局变量
var AuthMiddleware *jwt.GinJWTMiddleware

func init() {
	var err error
	AuthMiddleware, err = mid.JwtMiddleware()
	if err != nil {
		logger.Fatal("JWT Error:" + err.Error())
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
// @Summary 注册
// @tags API1 用户
// @Accept  multipart/form-data
// @Produce json
// @Param Register body controllers.register true "注册信息表单"
// @Success 200 {string} json "{"data": "ok",	"status": 200}"
// @Router /user/register [post]
func RegisterUser(c *gin.Context) {
	var reg register
	var user m.User
	err := c.ShouldBindJSON(&reg)
	if err != nil {
		res.ResFailedStatus(c, e.Errors["RegisterInvalidData"])
		return
	}

	user.Password = reg.Password
	user.Name = reg.Username
	user.Email = reg.Email
	user.Mobile = reg.Mobile
	user.TypeID = 1000 //普通用户TypeId=1000
	user.Image = "/img/avatar.jpg"

	if user.Password == "" || (user.Name == "" && user.Email == "" && user.Mobile == "") {
		logger.Warn("RegisterUser failed ", user)
		res.ResFailedStatus(c, e.Errors["RegisterInvalidData"])
		return
	}

	exituser, _ := user.CheckUserExist()
	if exituser != nil {
		res.ResFailedStatus(c, e.Errors["RegisterUserExisted"])
		return
	}

	//检查如果是邮箱注册，必须检查验证码的合法
	if user.Email != "" {
		valid, em, codeerr := m.CheckEmailCodeValied(user.Email, reg.EmailCode)
		if valid == false {
			res.ResFailedStatus(c, codeerr)
			return
		}
		//校验完之后丢弃这个校验码
		em.UpdateEmailInvalid()
	}

	err = user.Newuser()
	if err != nil {
		res.ResFailedStatus(c, e.Errors["RegisterNewUserFailed"])
		return
	}

	logger.Info("RegisterUser succsess ", user)
	res.ResSucceedString(c, "ok")
	return
}

// GetUser 获得当前用户信息
// @Description 获得当前用户信息
// @Summary 用户信息
// @tags API1 用户（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {object} models.User
// @Router /user/userinfo [get]
func GetUser(c *gin.Context) {
	u, _ := m.GetUserFromContext(c)
	res.ResSucceedStruct(c, u)
	return
}

// OptionUser option请求
func OptionUser(c *gin.Context) {
	res.ResSucceedString(c, "ok")
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
// @Description
// @Summary 登录
// @tags API1 用户
// @Accept  json
// @Produce json
// @Param Login body middlewares.LoginFormData true "登录信息表单"
// @Success 200 {object} middlewares.LoginSucceed
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
// @Success 200 {string} json "{"status": 200, "data": "ok"}"
// @Router /user/logout [get]
func LogoutUser(c *gin.Context) {
	res.ResSucceedString(c, "ok")
	return
}

// CheckAuth 检查当前连接是否已经登录
func CheckAuth(c *gin.Context) {
	AuthMiddleware.MiddlewareFunc()(c)
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
		logger.Info(err)
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

	res.ResSucceedStruct(c, dts)
	return
}

type listusers struct {
	Users []m.User `json:"users"`
	Total int      `json:"total"`
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
		logger.Info(err)
	}
	lu := listusers{
		Users: users,
		Total: total,
	}
	res.ResSucceedStruct(c, lu)
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
// @Success 200 {string} json "{"status": 200, "data": "ok"}"
// @Router /user/updateinfo [post]
func UpdateUserInfo(c *gin.Context) {
	uu := updateUser{}
	err := c.ShouldBindJSON(&uu)
	u, _ := m.GetUserFromContext(c)
	if err != nil || u.ID < 1 {
		res.ResFailedStatus(c, e.Errors["PostDataInvalied"])
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
		res.ResFailedStatus(c, e.Errors["UserUpdateFailed"])
	}

	res.ResSucceedString(c, "ok")
	return
}

// updatepasswd 通过验证码修改密码
type updatepasswd struct {
	Email           string `json:"email"     example:"mail@163.com"`                                          // 邮箱
	EmailCode       string `json:"emailcode" example:"654321"`                                                // 验证码
	Password        string `json:"password" binding:"required,max=124" example:"123"`                         // 新密码
	ConfirmPassword string `json:"confirmPassword" binding:"required,eqfield=Password,max=124" example:"123"` // 新密码确认
}

// UpdatePassWD 通过验证码修改密码
// @Summary 通过验证码修改密码
// @Description 通过验证码修改密码
// @tags API1 用户
// @Accept  json
// @Produce json
// @Param updatepasswd body controllers.updatepasswd true "通过验证码修改密码"
// @Success 200 {string} json "{"status": 200, "data": "ok"}"
// @Router /user/updatepasswd [post]
func UpdatePassWD(c *gin.Context) {
	up := updatepasswd{}
	err := c.ShouldBindJSON(&up)
	if err != nil {
		res.ResFailedStatus(c, e.Errors["PostDataInvalied"])
		return
	}

	if len(up.Email) < 5 || len(up.EmailCode) < 6 || len(up.Password) < 3 || up.Password != up.ConfirmPassword {
		res.ResFailedStatus(c, e.Errors["PostDataInvalied"])
		return
	}

	//必须检查验证码的合法
	valid, em, codeerr := m.CheckEmailCodeValied(up.Email, up.EmailCode)
	if valid == false {
		res.ResFailedStatus(c, codeerr)
		return
	}
	//校验完之后丢弃这个校验码
	em.UpdateEmailInvalid()

	userinfo := &m.User{
		ID:    0,
		Email: up.Email,
	}
	_user, err2 := userinfo.Finduserbyemail()
	if err2 != nil || _user.ID < 1 {
		res.ResFailedStatus(c, e.Errors["PasswdUpdateEmailNotFound"])
		return
	}

	err3 := m.UpdateUserPassWD(_user.ID, up.Password)
	if err3 != nil {
		res.ResFailedStatus(c, e.Errors["PasswdUpdateFailed"])
		return
	}

	res.ResSucceedString(c, "ok")
	return
}
