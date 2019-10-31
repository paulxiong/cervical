package controllers

import (
	"github.com/gin-gonic/gin"
	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
)

// ResString 响应一个字符串
func ResString(c *gin.Context, v string) {
	c.JSON(e.StatusReqOK, gin.H{"status": e.StatusSucceed, "data": v})
}

// ResStruct 响应一个struct
func ResStruct(c *gin.Context, v interface{}) {
	c.JSON(e.StatusReqOK, gin.H{"status": e.StatusSucceed, "data": v})
}
