package middlewares

import (
	configs "github.com/paulxiong/cervical/webpage/2_api_server/configs"
	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	models "github.com/paulxiong/cervical/webpage/2_api_server/models"
	res "github.com/paulxiong/cervical/webpage/2_api_server/responses"

	"errors"
	"time"

	jwt "github.com/appleboy/gin-jwt/v2"
	"github.com/gin-gonic/gin"
	"golang.org/x/crypto/bcrypt"
)

// IdentityKey 区分用户的key
var IdentityKey = "user.Id"

// LoginFormData 登录的表单数据
type LoginFormData struct {
	Username      string `form:"username"      json:"username"                    example:"username"`        // 用户名
	Password      string `form:"password"      json:"password" binding:"required" example:"password"`        // 密码
	EmailOrMobile string `form:"emailormobile" json:"emailormobile"               example:"email or mobile"` // 邮箱或者手机号
}

// LoginSucceed 登录成功之后返回客户端的内容
type LoginSucceed struct {
	Token  string       `json:"token"  example:"token"`  // token的字符串
	Expire string       `json:"expire" example:"expire"` // 当前token过期的时间戳
	User   *models.User `json:"user"`                    // 当前登录的用户信息
}

// LoginWithPasswd 检查用户名密码是否匹配
func LoginWithPasswd(name string, password string, emailormobile string) (*models.User, string) {
	userFound, _ := models.CheckUserExist2(name, emailormobile, emailormobile)
	if userFound == nil {
		return nil, "LoginUserNotFound"
	}

	hashed := []byte(userFound.Password)
	err := bcrypt.CompareHashAndPassword(hashed, []byte(password))
	if err != nil {
		logger.Info.Println("Authenticator  password not match")
		return nil, "LoginBadPasswd"
	}
	return userFound, ""
}

// JwtMiddleware jwt
func JwtMiddleware() (*jwt.GinJWTMiddleware, error) {
	// the jwt middleware
	authMiddleware, err := jwt.New(&jwt.GinJWTMiddleware{
		Realm:       "xdedu",
		Key:         []byte("xdedu secret key"),
		Timeout:     time.Second * time.Duration(configs.Jwt.ExpireSecond),
		MaxRefresh:  time.Second * time.Duration(configs.Jwt.ExpireSecond*60),
		IdentityKey: IdentityKey,
		PayloadFunc: func(data interface{}) jwt.MapClaims {
			user, ok := data.(*models.User)
			if ok {
				return jwt.MapClaims{
					IdentityKey: user.ID,
				}
			}
			return jwt.MapClaims{}
		},
		IdentityHandler: func(c *gin.Context) interface{} {
			claims := jwt.ExtractClaims(c)
			userID := int64(claims[IdentityKey].(float64))
			user := &models.User{ID: userID}
			models.SaveUsertoContext(c, user)
			return user
		},
		Authenticator: func(c *gin.Context) (interface{}, error) {
			var loginVals LoginFormData
			if err := c.ShouldBind(&loginVals); err != nil {
				logger.Info.Println(err)
				return "", jwt.ErrMissingLoginValues
			}
			userName := loginVals.Username
			EmailMobile := loginVals.EmailOrMobile
			password := loginVals.Password
			userFound, errstring := LoginWithPasswd(userName, password, EmailMobile)
			if userFound == nil {
				return "", errors.New(errstring)
			}
			models.SaveUsertoContext(c, userFound)
			return userFound, nil
		},
		Authorizator: func(data interface{}, c *gin.Context) bool {
			return true
			/*
				if v, ok := data.(*m.User); ok && v.Name == "admin" {
					return true
				}
				return false
			*/
		},
		Unauthorized: func(c *gin.Context, code int, message string) {
			if message == "missing Username or Password" || message == "" {
				res.ResFailedStatus(c, e.Errors["LoginInvalidData"])
			} else if message == "LoginUserNotFound" {
				res.ResFailedStatus(c, e.Errors["LoginUserNotFound"])
			} else if message == "LoginBadPasswd" {
				res.ResFailedStatus(c, e.Errors["LoginBadPasswd"])
			} else {
				res.ResFailedStatus(c, e.Errors["LoginError"])
			}
		},
		LoginResponse: func(c *gin.Context, code int, token string, expire time.Time) {
			user := &models.User{}
			newtoken := &models.Token{}
			userTmp, exists := c.Get("user")
			if exists == true && userTmp != nil {
				userTmp2 := userTmp.(*models.User)
				user.ID = userTmp2.ID
				newtoken.UserID = userTmp2.ID
			}

			newtoken.UpdateToken(token, expire)
			user.UserLogined()

			res.ResSucceedStruct(c, LoginSucceed{
				Token:  token,
				Expire: expire.Format(time.RFC3339),
				User:   user,
			})
		},
		// TokenLookup is a string in the form of "<source>:<name>" that is used
		// to extract token from the request.
		// Optional. Default value "header:Authorization".
		// Possible values:
		// - "header:<name>"
		// - "query:<name>"
		// - "cookie:<name>"
		// - "param:<name>"
		TokenLookup: "header: Authorization, query:token,  cookie:token",
		// TokenLookup: "query:token",
		// TokenLookup: "cookie:token",

		// TokenHeadName is a string in the header. Default value is "Bearer"
		TokenHeadName: "token",

		// TimeFunc provides the current time. You can override it to use another time value. This is useful for testing or if your server uses a different time zone than your tokens.
		TimeFunc: time.Now,
	})

	if err != nil {
		logger.Error.Fatal("JWT Error:" + err.Error())
	}
	return authMiddleware, nil
}

//login(sucessed): Authenticator-->PayloadFunc-->LoginResponse
//login(failed): Authenticator-->Unauthorized
//ping(logined):IdentityHandler-->Authorizator
//ping(not logined):Unauthorized
