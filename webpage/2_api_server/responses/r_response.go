package responses

import (
	"github.com/gin-gonic/gin"
	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
)

// ResString 响应一个字符串
func ResString(c *gin.Context, status int, v string) {
	c.JSON(e.StatusReqOK, gin.H{
		"status": status,
		"data":   v,
	})
}

// ResStruct 响应一个struct
func ResStruct(c *gin.Context, status int, v interface{}) {
	c.JSON(e.StatusReqOK, gin.H{
		"status": status,
		"data":   v,
	})
}

// ResInt64 响应一个int64
func ResInt64(c *gin.Context, status int, v int64) {
	c.JSON(e.StatusReqOK, gin.H{
		"status": status,
		"data":   v,
	})
}

// ResFailedStatus 失败只返回status
func ResFailedStatus(c *gin.Context, status int) {
	c.JSON(e.StatusReqOK, gin.H{
		"status": status,
		"data":   nil,
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

// ResSucceedInt64 响应一个int
func ResSucceedInt64(c *gin.Context, v int64) {
	ResInt64(c, e.Errors["Succeed"], v)
}
