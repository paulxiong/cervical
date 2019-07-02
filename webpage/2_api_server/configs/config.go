package configs

import (
	"log"
	"os"
	"strconv"
	"strings"

	"github.com/Unknwon/goconfig"
)

type MySqlcfg struct {
	Host     string
	Port     int64
	User     string
	Database string
	Password string
}

type Servercfg struct {
	Port int64
}

type Logcfg struct {
	Log_out   string //打开所有log(gin的log和自定义的log)
	Log_gin   string //打开gin的log
	Log_level string
}

type Jwtcfg struct {
	Expire_Second int64
}

type Qiniucfg struct {
	AccessKey string
	SecretKey string
	Bucket    string
	Enable    bool
}

type Wechatcfg struct {
	OriId                string //原始ID
	AppId                string //AppID
	AppSecret            string //AppSecret
	ServerToken          string //服务器配置-令牌
	ServerEncodingAESKey string //服务器配置-消息加解密密钥
	ServerMpVerifyFile   string //服务器配置-域名修改时候的校验文件
	ServerDomain         string //服务器配置-服务器域名
	Enable               bool   //打开/关闭  true/false
}

var (
	MySql  MySqlcfg
	Server Servercfg
	Log    Logcfg
	Jwt    Jwtcfg
	Qiniu  Qiniucfg
	Wechat Wechatcfg
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
	} else {
		log.Printf("CFG: %s=%s\n", key, value)
		return value, nil
	}
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

	Jwt.Expire_Second, _ = getConfigIntValue(cfg, "Token", "expire_second", "EXPIRE_SECOND")
	Server.Port, _ = getConfigIntValue(cfg, "Server", "port", "SERVER_PORT")
	Log.Log_out, _ = getConfigStringValue(cfg, "Log", "log_out", "LOG_OUT")
	Log.Log_gin, _ = getConfigStringValue(cfg, "Log", "log_gin", "LOG_GIN")
	Log.Log_level, _ = getConfigStringValue(cfg, "Log", "log_level", "LOG_LEVEL")
	MySql.Host, _ = getConfigStringValue(cfg, "Mysql", "host", "MYSQL_HOST")
	MySql.Port, _ = getConfigIntValue(cfg, "Mysql", "port", "MYSQL_PORT")
	MySql.Database, _ = getConfigStringValue(cfg, "Mysql", "database", "MYSQL_DB")
	MySql.User, _ = getConfigStringValue(cfg, "Mysql", "user", "MYSQL_USR")
	MySql.Password, _ = getConfigStringValue(cfg, "Mysql", "password", "MYSQL_PASSWD")
	Qiniu.AccessKey, _ = getConfigStringValue(cfg, "Qiniu", "accessKey", "QINIU_ACCESSKEY")
	Qiniu.SecretKey, _ = getConfigStringValue(cfg, "Qiniu", "secretKey", "QINIU_SECRETKEY")
	Qiniu.Bucket, _ = getConfigStringValue(cfg, "Qiniu", "bucket", "QINIU_BUCKET")
	Qiniu.Enable, _ = getConfigBoolValue(cfg, "Qiniu", "enable", "QINIU_ENABLE")
	Wechat.OriId, _ = getConfigStringValue(cfg, "Wechat", "ori_id", "WECHAT_ORIID")
	Wechat.AppId, _ = getConfigStringValue(cfg, "Wechat", "appid", "WECHAT_APPID")
	Wechat.AppSecret, _ = getConfigStringValue(cfg, "Wechat", "appsecret", "WECHAT_APPSECRET")
	Wechat.ServerToken, _ = getConfigStringValue(cfg, "Wechat", "server_token", "WECHAT_TOKEN")
	Wechat.ServerEncodingAESKey, _ = getConfigStringValue(cfg, "Wechat", "server_encodingAESKey", "WECHAT_AES")
	Wechat.ServerMpVerifyFile, _ = getConfigStringValue(cfg, "Wechat", "server_mp_verify_file", "WECHAT_MPVERIFY")
	Wechat.ServerDomain, _ = getConfigStringValue(cfg, "Wechat", "server_domain", "WECHAT_DOMAIN")
	Wechat.Enable, _ = getConfigBoolValue(cfg, "Wechat", "enable", "WECHAT_ENABLE")

	log.Printf("config inited")
}
