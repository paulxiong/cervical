package configs

import (
	"log"
	"os"
	"strconv"
	"strings"

	"github.com/Unknwon/goconfig"
)

// MySqlcfg 数据库配置
type MySqlcfg struct {
	Host     string
	Port     int64
	User     string
	Database string
	Password string
}

// Servercfg 服务信息配置
type Servercfg struct {
	Port int64
}

// Logcfg 日志配置
type Logcfg struct {
	LogOut   string //打开所有log(gin的log和自定义的log)
	LogGin   string //打开gin的log
	LogLevel string
}

// Jwtcfg jwt 配置
type Jwtcfg struct {
	ExpireSecond int64
}

// Qiniucfg 七牛云存储配置
type Qiniucfg struct {
	AccessKey string
	SecretKey string
	Bucket    string
	Enable    bool
}

// Wechatcfg 微信公众号配置
type Wechatcfg struct {
	OriID                string //原始ID
	AppID                string //AppID
	AppSecret            string //AppSecret
	ServerToken          string //服务器配置-令牌
	ServerEncodingAESKey string //服务器配置-消息加解密密钥
	ServerMpVerifyFile   string //服务器配置-域名修改时候的校验文件
	ServerDomain         string //服务器配置-服务器域名
	Enable               bool   //打开/关闭  true/false
}

// Emailcfg 发送邮件的配置
type Emailcfg struct {
	Enable bool   //打开/关闭  true/false
	User   string //发件用户
	Passwd string //发件用户ID
	Host   string //邮件服务器地址
	Port   string //邮件服务器端口
}

var (
	//MySQL 数据库
	MySQL MySqlcfg
	//Server 当前服务
	Server Servercfg
	//Log 服务日志
	Log Logcfg
	//Jwt token
	Jwt Jwtcfg
	//Qiniu 存储
	Qiniu Qiniucfg
	//Wechat 微信公众号
	Wechat Wechatcfg
	//Email 邮箱配置
	Email Emailcfg
)

func getConfigStringValue(cfg *goconfig.ConfigFile, section string, key string, envName string) (val string, err error) {
	env := os.Getenv(envName)
	if strings.Count(env, "") > 1 {
		log.Printf("ENV: %s=%s\n", key, env)
		return env, nil
	}
	value, err := cfg.GetValue(section, key)
	if err != nil {
		log.Printf("section or value not found %s %s\n", section, key)
		return "", err
	}
	log.Printf("CFG: %s=%s\n", key, value)
	return value, nil
}

func getConfigIntValue(cfg *goconfig.ConfigFile, section string, key string, envName string) (val int64, err error) {
	env := os.Getenv(envName)
	if strings.Count(env, "") > 1 {
		envint64, err := strconv.ParseInt(env, 10, 32)
		if err == nil {
			log.Printf("ENV: %s=%d\n", key, envint64)
			return envint64, nil
		}
	}
	value, err2 := cfg.GetValue(section, key)
	if err2 != nil {
		log.Printf("section or value not found %s %s\n", section, key)
		return 0, err2
	}
	valint64, err3 := strconv.ParseInt(value, 10, 32)
	if err3 == nil {
		log.Printf("CFG: %s=%d\n", key, valint64)
		return valint64, nil
	}
	return valint64, nil
}

func getConfigBoolValue(cfg *goconfig.ConfigFile, section string, key string, envName string) (val bool, err error) {
	env := os.Getenv(envName)
	if env == "true" || env == "True" || env == "TRUE" {
		return true, nil
	}

	value, err2 := cfg.GetValue(section, key)
	if err2 != nil {
		log.Printf("section or value not found %s %s\n", section, key)
		return false, err2
	}
	log.Printf("CFG: %s=%s\n", key, value)
	if value == "true" || value == "True" || value == "TRUE" {
		return true, nil
	}
	return false, nil
}

func init() {
	var configfile string = "configs/conf-dev.ini"
	ginmode := os.Getenv("GIN_MODE")
	if ginmode == "release" {
		configfile = "configs/conf.ini"
	}
	cfg, err := goconfig.LoadConfigFile(configfile)
	if err != nil {
		log.Printf("load config failed")
	}

	Jwt.ExpireSecond, _ = getConfigIntValue(cfg, "Token", "expire_second", "EXPIRE_SECOND")
	Server.Port, _ = getConfigIntValue(cfg, "Server", "port", "SERVER_PORT")
	Log.LogOut, _ = getConfigStringValue(cfg, "Log", "log_out", "LOG_OUT")
	Log.LogGin, _ = getConfigStringValue(cfg, "Log", "log_gin", "LOG_GIN")
	Log.LogLevel, _ = getConfigStringValue(cfg, "Log", "log_level", "LOG_LEVEL")
	MySQL.Host, _ = getConfigStringValue(cfg, "Mysql", "host", "MYSQL_HOST")
	MySQL.Port, _ = getConfigIntValue(cfg, "Mysql", "port", "MYSQL_PORT")
	MySQL.Database, _ = getConfigStringValue(cfg, "Mysql", "database", "MYSQL_DB")
	MySQL.User, _ = getConfigStringValue(cfg, "Mysql", "user", "MYSQL_USR")
	MySQL.Password, _ = getConfigStringValue(cfg, "Mysql", "password", "MYSQL_PASSWD")
	Qiniu.AccessKey, _ = getConfigStringValue(cfg, "Qiniu", "accessKey", "QINIU_ACCESSKEY")
	Qiniu.SecretKey, _ = getConfigStringValue(cfg, "Qiniu", "secretKey", "QINIU_SECRETKEY")
	Qiniu.Bucket, _ = getConfigStringValue(cfg, "Qiniu", "bucket", "QINIU_BUCKET")
	Qiniu.Enable, _ = getConfigBoolValue(cfg, "Qiniu", "enable", "QINIU_ENABLE")
	Wechat.OriID, _ = getConfigStringValue(cfg, "Wechat", "ori_id", "WECHAT_ORIID")
	Wechat.AppID, _ = getConfigStringValue(cfg, "Wechat", "appid", "WECHAT_APPID")
	Wechat.AppSecret, _ = getConfigStringValue(cfg, "Wechat", "appsecret", "WECHAT_APPSECRET")
	Wechat.ServerToken, _ = getConfigStringValue(cfg, "Wechat", "server_token", "WECHAT_TOKEN")
	Wechat.ServerEncodingAESKey, _ = getConfigStringValue(cfg, "Wechat", "server_encodingAESKey", "WECHAT_AES")
	Wechat.ServerMpVerifyFile, _ = getConfigStringValue(cfg, "Wechat", "server_mp_verify_file", "WECHAT_MPVERIFY")
	Wechat.ServerDomain, _ = getConfigStringValue(cfg, "Wechat", "server_domain", "WECHAT_DOMAIN")
	Wechat.Enable, _ = getConfigBoolValue(cfg, "Wechat", "enable", "WECHAT_ENABLE")
	Email.Enable, _ = getConfigBoolValue(cfg, "Email", "enable", "EMAIL_ENABLE")
	Email.User, _ = getConfigStringValue(cfg, "Email", "email_user", "EMAIL_USER")
	Email.Passwd, _ = getConfigStringValue(cfg, "Email", "email_passwd", "EMAIL_PASSWD")
	Email.Host, _ = getConfigStringValue(cfg, "Email", "email_host", "EMAIL_HOST")
	Email.Port, _ = getConfigStringValue(cfg, "Email", "email_port", "EMAIL_PORT")

	log.Printf("config inited")
}
