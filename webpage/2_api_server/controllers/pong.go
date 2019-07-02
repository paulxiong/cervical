package controllers

import (
	e "../error"

	"github.com/gin-gonic/gin"
)

func Pong(c *gin.Context) {
	c.JSON(e.StatusReqOK, gin.H{"status": e.StatusSucceed, "ping": "pong"})
}
