package controllers

import (
	"fmt"
	"strconv"

	e "github.com/paulxiong/cervical/webpage/2_api_server/error"

	"github.com/gin-gonic/gin"
)

// GetPredictResult2 根据传递来的项目ID，批次ID， 病例ID， 图片ID,返回预测的结果
// @Summary 根据传递来的项目ID，批次ID， 病例ID， 图片ID,返回预测的结果
// @Description 根据传递来的项目ID，批次ID， 病例ID， 图片ID,返回当前图片里面细胞的预测的结果，医生报告使用
// @Description status：
// @Description 200 创建
// @tags API1 医疗报告（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param pid query string false "pid, default 0, 项目ID"
// @Param bid query string false "bid, default 0, 批次ID"
// @Param mid query string false "mid, default 0, 病例ID"
// @Param iid query string false "iid, default 0, 图片ID"
// @Success 200 {object} function.PredictInfo2
// @Router /api1/predictresult2 [get]
func GetPredictResult2(c *gin.Context) {
	pidStr := c.DefaultQuery("pid", "0")
	bidStr := c.DefaultQuery("bid", "0")
	midStr := c.DefaultQuery("mid", "0")
	iidStr := c.DefaultQuery("iid", "0")
	pid, _ := strconv.ParseInt(pidStr, 10, 64)
	bid, _ := strconv.ParseInt(bidStr, 10, 64)
	mid, _ := strconv.ParseInt(midStr, 10, 64)
	iid, _ := strconv.ParseInt(iidStr, 10, 64)

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   fmt.Sprintf("%d %d %d %d", pid, bid, mid, iid),
	})
	return
}
