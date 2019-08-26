package controllers

import (
	e "github.com/paulxiong/cervical/webpage/2_api_server/error"

	"github.com/gin-gonic/gin"
)

func Pong(c *gin.Context) {
	c.JSON(e.StatusReqOK, gin.H{"status": e.StatusSucceed, "ping": "pong"})
}
