package platforms

import (
	configs "github.com/paulxiong/cervical/webpage/2_api_server/configs"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"

	"github.com/chanxuehong/wechat/mp/core"
	"github.com/chanxuehong/wechat/mp/menu"
	"github.com/chanxuehong/wechat/mp/message/callback/request"
	"github.com/chanxuehong/wechat/mp/message/callback/response"
)

func textMsgHandler(ctx *core.Context) {
	logger.Infof("收到文本消息:\n%s\n", ctx.MsgPlaintext)

	msg := request.GetText(ctx.MixedMsg)
	resp := response.NewText(msg.FromUserName, msg.ToUserName, msg.CreateTime, msg.Content)
	ctx.RawResponse(resp) // 明文回复
	//ctx.AESResponse(resp, 0, "", nil) // aes密文回复
}

func defaultMsgHandler(ctx *core.Context) {
	logger.Infof("收到消息:\n%s\n", ctx.MsgPlaintext)
	ctx.NoneResponse()
}

func menuClickEventHandler(ctx *core.Context) {
	logger.Infof("收到菜单 click 事件:\n%s\n", ctx.MsgPlaintext)

	event := menu.GetClickEvent(ctx.MixedMsg)
	resp := response.NewText(event.FromUserName, event.ToUserName, event.CreateTime, "收到 click 类型的事件")
	ctx.RawResponse(resp) // 明文回复
	//ctx.AESResponse(resp, 0, "", nil) // aes密文回复
}

func defaultEventHandler(ctx *core.Context) {
	logger.Infof("收到事件:\n%s\n", ctx.MsgPlaintext)
	ctx.NoneResponse()
}

// NewWechatServe 注册微信接口
func NewWechatServe() *core.Server {
	mux := core.NewServeMux() // 创建 core.Handler, 也可以用自己实现的 core.Handler

	mux.DefaultMsgHandleFunc(defaultMsgHandler)
	mux.DefaultEventHandleFunc(defaultEventHandler)
	mux.MsgHandleFunc(request.MsgTypeText, textMsgHandler)
	mux.EventHandleFunc(menu.EventTypeClick, menuClickEventHandler)

	/*
		// 注册消息(事件)处理 Handler, 都不是必须的!
		{
			mux.UseFunc(func(ctx *core.Context) { // 注册中间件, 处理所有的消息(事件)
				logger.Info("处理所有的消息(事件)")
				// TODO: 中间件处理逻辑
			})
			mux.UseFuncForMsg(func(ctx *core.Context) { // 注册中间件, 处理所有的消息
				logger.Info("处理所有的消息")
				logger.Info(string(ctx.MsgPlaintext))

				// TODO: 中间件处理逻辑
			})
			mux.UseFuncForEvent(func(ctx *core.Context) { // 注册中间件, 处理所有的事件
				logger.Info("处理所有的事件")
				// TODO: 中间件处理逻辑
			})
		}
	*/

	// 创建 Server, 设置正确的参数.
	// 通常一个 Server 对应一个公众号, 当然一个 Server 也可以对应多个公众号, 这个时候 oriId 和 appId 都应该设置为空值!
	srv := core.NewServer(configs.Wechat.OriID, configs.Wechat.AppID, configs.Wechat.ServerToken, configs.Wechat.ServerEncodingAESKey, mux, nil)
	return srv
}
