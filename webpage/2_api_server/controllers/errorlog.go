package controllers

import (
	"strconv"

	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
	models "github.com/paulxiong/cervical/webpage/2_api_server/models"
	res "github.com/paulxiong/cervical/webpage/2_api_server/responses"

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
// @Router /api1/errorlog [post]
func CreateErrorLog(c *gin.Context) {
	el := errlog{}
	err := c.ShouldBindJSON(&el)
	if err != nil {
		res.ResFailedStatus(c, e.Errors["PostDataInvalied"])
		return
	}
	user, _ := models.GetUserFromContext(c)
	nel := &models.Errorlog{
		ID:        0,
		Errlog:    el.Errlog,
		Opid:      0,
		CreatedBy: user.ID,
	}
	nel.NewErrorLog()

	models.SaveErrorlogIDtoContext(c, nel.ID)

	res.ResSucceedString(c, "ok")
	return
}

type errlogs struct {
	Logs  []models.Errorlog
	Total int `json:"total"  example:"100"` //错误日志的的个数
}

// GetErrorLog 获得前端错误日志
// @Summary 获得前端错误日志
// @Description 获得前端错误日志
// @tags API1 系统（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param limit query string false "limit, default 10"
// @Param skip query string false "skip, default 0"
// @Param order query string false "order, default 1, 1倒序，0顺序，顺序是指创建时间"
// @Success 200 {object} controllers.errlogs
// @Router /api1/errorlog [get]
func GetErrorLog(c *gin.Context) {
	limitStr := c.DefaultQuery("limit", "10")
	skipStr := c.DefaultQuery("skip", "0")
	orderStr := c.DefaultQuery("order", "1")
	limit, _ := strconv.ParseInt(limitStr, 10, 32)
	skip, _ := strconv.ParseInt(skipStr, 10, 32)
	_order, _ := strconv.ParseInt(orderStr, 10, 32)

	els, total, _ := models.ErrorlogLists(int(limit), int(skip), int(_order))

	el := errlogs{
		Logs:  els,
		Total: total,
	}
	res.ResSucceedStruct(c, el)
	return
}
