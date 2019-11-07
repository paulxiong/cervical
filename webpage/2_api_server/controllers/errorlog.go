package controllers

import (
	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
	models "github.com/paulxiong/cervical/webpage/2_api_server/models"

	"github.com/gin-gonic/gin"
)

type errlog struct {
	Errlog string `json:"errlog"   example:"error string{}"` // 错误日志的字符串
}

// CreateErrorLog 记录前端错误日志到数据库
// @Summary 记录前端错误日志到数据库
// @Description 记录前端错误日志到数据库
// @tags API1 系统（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param CreateErrorLog body controllers.errlog true "新建(训练/预测)项目"
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/errorlog [post]
func CreateErrorLog(c *gin.Context) {
	el := errlog{}
	err := c.ShouldBindJSON(&el)
	if err != nil {
		ResString(c, "invalied errorlog")
		return
	}
	opid, _ := models.GetOperationlogIDFromContext(c)
	user, _ := models.GetUserFromContext(c)
	nel := &models.ErrorLog{
		Errlog:    el.Errlog,
		Opid:      opid,
		CreatedBy: user.ID,
	}
	nel.NewErrorLog()

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   "ok",
	})
	return
}
