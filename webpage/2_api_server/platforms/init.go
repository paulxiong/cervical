package platforms

import (
	"github.com/chanxuehong/wechat/mp/core"
	c "github.com/paulxiong/cervical/webpage/2_api_server/configs"
)

// Srv 全局变量
var Srv *core.Server

func init() {
	if c.Qiniu.Enable {
		QiniuInit()
	}
	if c.Wechat.Enable {
		Srv = NewWechatServe()
	}
}
