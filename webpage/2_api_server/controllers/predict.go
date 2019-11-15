package controllers

import (
	"strconv"

	f "github.com/paulxiong/cervical/webpage/2_api_server/functions"
	models "github.com/paulxiong/cervical/webpage/2_api_server/models"

	"github.com/gin-gonic/gin"
)

type reporterpredicts struct {
	Total    int              `json:"total"  example:"100"` // 总细胞预测数量
	Predicts []models.Predict `json:"cells"`                // 每个细胞
}

// GetPredictResult2 根据传递来的图片ID,返回预测的结果
// @Summary 根据传递来的图片ID,返回预测的结果
// @Description 根据传递来的图片ID,返回当前图片里面细胞的预测的结果，医生报告使用
// @Description status：
// @Description 200 创建
// @tags API1 医疗报告（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param iid query string false "iid, default 659, 图片ID"
// @Param limit query string false "limit, default 1"
// @Param skip query string false "skip, default 0"
// @Success 200 {object} controllers.reporterpredicts
// @Router /api1/predictresult2 [get]
func GetPredictResult2(c *gin.Context) {
	iidStr := c.DefaultQuery("iid", "0")
	iid, _ := strconv.ParseInt(iidStr, 10, 64)
	limitStr := c.DefaultQuery("limit", "1")
	skipStr := c.DefaultQuery("skip", "0")
	limit, _ := strconv.ParseInt(limitStr, 10, 64)
	skip, _ := strconv.ParseInt(skipStr, 10, 64)

	total, predicts, _ := models.ListPredict(int(limit), int(skip), int(iid))
	_predicts := reporterpredicts{
		Total:    int(total),
		Predicts: predicts,
	}

	ResStruct(c, _predicts)
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
// @Param did query string false "did, default 62, 数据集ID"
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