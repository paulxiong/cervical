package platforms

import (
	c "../configs"
	"github.com/chanxuehong/wechat/mp/core"
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
