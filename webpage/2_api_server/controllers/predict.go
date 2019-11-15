package controllers

import (
	"fmt"
	"strconv"

	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
	f "github.com/paulxiong/cervical/webpage/2_api_server/functions"
	models "github.com/paulxiong/cervical/webpage/2_api_server/models"

	"github.com/gin-gonic/gin"
)

// GetPredictResult2 根据传递来的图片ID,返回预测的结果
// @Summary 根据传递来的图片ID,返回预测的结果
// @Description 根据传递来的图片ID,返回当前图片里面细胞的预测的结果，医生报告使用
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

type reporterimg struct {
	ID      int64  `json:"id"      example:"100"` // 图片ID
	Imgpath string `json:"imgpath" example:"100"` // 图片URL
	W       int    `json:"w"       example:"100"` // 宽
	H       int    `json:"h"       example:"100"` // 高
}

type reporterimgs struct {
	Total int           `json:"total"  example:"100"` // 总图片数
	Imgs  []reporterimg `json:"images"`               // 每张图片
}

// GetPredictImges 根据传递来的数据集ID，返回当前报告的所有图片列表
// @Summary 据传递来的数据集ID，返回当前报告的所有图片列表
// @Description 据传递来的数据集ID，返回当前报告的所有图片列表(注意预测报告只有一个批次，一个病例，所以这个接口除了医疗报告，其他操作不要用)
// @Description status：
// @Description 200 创建
// @tags API1 医疗报告（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param did query string false "did, default 0, 数据集ID"
// @Success 200 {object} controllers.reporterimgs
// @Router /api1/datasetimgs [get]
func GetPredictImges(c *gin.Context) {
	didStr := c.DefaultQuery("did", "0")
	did, _ := strconv.ParseInt(didStr, 10, 64)

	_d, err := models.GetOneDatasetByID(int(did))
	if err != nil || len(_d.MedicalIDs1) < 1 {
		ResString(c, "datasets not found")
		return
	}

	total, imgs, _ := models.ListImagesByMedicalID2(_d.MedicalIDs1[0])
	rimgs := reporterimgs{}
	rimgs.Total = total
	rimgs.Imgs = make([]reporterimg, 0)
	for _, v := range imgs {
		rimgs.Imgs = append(rimgs.Imgs, reporterimg{
			ID:      v.ID,
			Imgpath: f.Imgpath(v.Batchid, v.Medicalid, v.Imgpath, v.Type),
			W:       v.W,
			H:       v.H,
		})
	}
	ResStruct(c, rimgs)
	return
}
