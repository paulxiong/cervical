package controllers

import (
	e "github.com/paulxiong/cervical/webpage/2_api_server/error"

	"github.com/gin-gonic/gin"
)

// @Pong 检查网络是否正常
// @Description ping检查网络是否正常
// @tags API1
// @Accept  json
// @Produce json
// @Success 200 {string} string	"pong"
// @Router /api1/ping1 [get]
func Pong(c *gin.Context) {
	c.JSON(e.StatusReqOK, gin.H{"status": e.StatusSucceed, "ping": "pong"})
}
