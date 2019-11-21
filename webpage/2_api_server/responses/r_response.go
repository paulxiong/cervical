package responses

import (
	"github.com/gin-gonic/gin"
	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
)

//  {
//      code: "200", // 当前请求的状态，比如 RFC 7231, 6.3.1， 200表示StatusOK
//      status: "70", // 我们平台处理请求的状态, 比如70表示：注册的用户名已经存在
//      type: "obj", // data字段的内容的类型，可以是 obj/array/int/string/null里面的5种
//      data: {}/[]/int/string // 我们平台处理请求的结果，可以是对象/数组/整数/字符串
//  }

// ResString 响应一个字符串
func ResString(c *gin.Context, status int, v string) {
	c.JSON(e.StatusReqOK, gin.H{
		"code":   e.StatusSucceed,
		"status": status,
		"type":   "string",
		"data":   v,
	})
}

// ResStruct 响应一个struct
func ResStruct(c *gin.Context, status int, v interface{}) {
	c.JSON(e.StatusReqOK, gin.H{
		"code":   e.StatusSucceed,
		"status": status,
		"type":   "obj",
		"data":   v,
	})
}

// ResInt 响应一个int
func ResInt(c *gin.Context, status int, v int) {
	c.JSON(e.StatusReqOK, gin.H{
		"code":   e.StatusSucceed,
		"status": status,
		"type":   "int",
		"data":   v,
	})
}

// ResFailedStatus 失败只返回status
func ResFailedStatus(c *gin.Context, status int) {
	c.JSON(e.StatusReqOK, gin.H{
		"code":   e.StatusSucceed,
		"status": status,
		"type":   "null",
		"data":   "",
	})
}

// ResSucceedString 响应一个字符串
func ResSucceedString(c *gin.Context, v string) {
	ResString(c, e.Errors["Succeed"], v)
}

// ResSucceedStruct 响应一个struct
func ResSucceedStruct(c *gin.Context, v interface{}) {
	ResStruct(c, e.Errors["Succeed"], v)
}

// ResSucceedInt 响应一个int
func ResSucceedInt(c *gin.Context, v int) {
	ResInt(c, e.Errors["Succeed"], v)
}
