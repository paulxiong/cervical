package controllers

import (
	e "github.com/paulxiong/cervical/webpage/2_api_server/error"

	"github.com/gin-gonic/gin"
)

// Pong 检查网络是否正常
// @Description ping检查网络是否正常
// @tags API1 连通性（不需要认证）
// @Accept  json
// @Produce json
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Router /api1/ping [get]
func Pong(c *gin.Context) {
	c.JSON(e.StatusReqOK, gin.H{"status": e.StatusSucceed, "ping": "pong"})
}

// AuthPong 检查网络是否正常，需要登录
// @Description ping检查网络是否正常，需要登录
// @tags API1 连通性（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Router /api1/authping [get]
func AuthPong(c *gin.Context) {
	c.JSON(e.StatusReqOK, gin.H{"status": e.StatusSucceed, "ping": "pong"})
}
