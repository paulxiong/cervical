package middlewares

import (
	configs "github.com/paulxiong/cervical/webpage/2_api_server/configs"
	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	m "github.com/paulxiong/cervical/webpage/2_api_server/models"

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
	Username      string `form:"username" json:"username" example:"用户名" format:"string"`
	Password      string `form:"password" json:"password" binding:"required" example:"密码" format:"string"`
	EmailOrMobile string `form:"emailormobile" json:"emailormobile" example:"邮箱或者手机号" format:"string"`
}

// LoginWithPasswd 检查用户名密码是否匹配
func LoginWithPasswd(name string, password string, emailormobile string) (*m.User, string) {
	userFound, _ := m.CheckUserExist2(name, emailormobile, emailormobile)
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
			logger.Info.Println("PayloadFunc")
			user, ok := data.(*m.User)
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
			logger.Info.Println("IdentityHandler ")
			user := &m.User{ID: userID}
			m.SaveUsertoContext(c, user)
			return user
		},
		Authenticator: func(c *gin.Context) (interface{}, error) {
			logger.Info.Println("Authenticator ")
			var loginVals LoginFormData
			if err := c.ShouldBind(&loginVals); err != nil {
				logger.Info.Println(err)
				return "", jwt.ErrMissingLoginValues
			}
			userName := loginVals.Username
			EmailMobile := loginVals.EmailOrMobile
			password := loginVals.Password
			userFound, errstring := LoginWithPasswd(userName, password, EmailMobile)
			logger.Info.Println(userName)
			logger.Info.Println(EmailMobile)
			logger.Info.Println(password)
			m.SaveUsertoContext(c, userFound)
			if userFound == nil {
				return "", errors.New(errstring)
			}
			return userFound, nil
		},
		Authorizator: func(data interface{}, c *gin.Context) bool {
			logger.Info.Println("Authorizator ", data)
			return true
			/*
				if v, ok := data.(*m.User); ok && v.Name == "admin" {
					return true
				}
				return false
			*/
		},
		Unauthorized: func(c *gin.Context, code int, message string) {
			logger.Info.Println("Unauthorized ", message, code)
			if message == "missing Username or Password" || message == "" {
				c.JSON(code, gin.H{"status": e.StatusLoginInvalidData64, "data": message})
			} else if message == "LoginUserNotFound" {
				c.JSON(code, gin.H{"status": e.StatusLoginUserNotFound61, "data": message})
			} else if message == "LoginBadPasswd" {
				c.JSON(code, gin.H{"status": e.StatusLoginBadPasswd60, "data": message})
			} else {
				c.JSON(code, gin.H{"status": e.StatusLoginError63, "data": message})
			}
		},
		LoginResponse: func(c *gin.Context, code int, token string, expire time.Time) {
			user := &m.User{}
			newtoken := &m.Token{}
			userTmp, exists := c.Get("user")
			if exists == true && userTmp != nil {
				userTmp2 := userTmp.(*m.User)
				user.ID = userTmp2.ID
				newtoken.UserID = userTmp2.ID
			}
			logger.Info.Println("LoginResponse")

			newtoken.UpdateToken(token, expire)
			user.UserLogined()

			c.JSON(e.StatusReqOK, gin.H{
				"status": e.StatusSucceed,
				"token":  token,
				"expire": expire.Format(time.RFC3339),
				"user":   user,
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
