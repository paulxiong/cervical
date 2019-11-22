package controllers

import (
	"strconv"

	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
	f "github.com/paulxiong/cervical/webpage/2_api_server/functions"
	models "github.com/paulxiong/cervical/webpage/2_api_server/models"
	res "github.com/paulxiong/cervical/webpage/2_api_server/responses"

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
// @Param status query string false "status, default 0, 0 未审核 1 已审核 2 移除 3 管理员已确认 4 未审核+已审核"
// @Success 200 {object} controllers.reporterpredicts
// @Router /api1/predictresult2 [get]
func GetPredictResult2(c *gin.Context) {
	iidStr := c.DefaultQuery("iid", "0")
	limitStr := c.DefaultQuery("limit", "1")
	skipStr := c.DefaultQuery("skip", "0")
	statusStr := c.DefaultQuery("status", "0")
	iid, _ := strconv.ParseInt(iidStr, 10, 64)
	limit, _ := strconv.ParseInt(limitStr, 10, 64)
	skip, _ := strconv.ParseInt(skipStr, 10, 64)
	status, _ := strconv.ParseInt(statusStr, 10, 64)

	total, predicts, _ := models.ListPredict(int(limit), int(skip), int(iid), int(status))
	_predicts := reporterpredicts{
		Total:    int(total),
		Predicts: predicts,
	}

	res.ResSucceedStruct(c, _predicts)
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
		res.ResFailedStatus(c, e.Errors["DatasetsNotFound"])
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
	res.ResSucceedStruct(c, rimgs)
	return
}

type predictupdate struct {
	ID       int64 `json:"id"`        // 细胞预测的ID
	TrueType int   `json:"true_type"` // 审核细胞类型,1到15是细胞类型, 50 阴性 51 阳性 100 未知, 200 不是细胞
}

// UpdatePredict 医生审核信息写回数据库
// @Summary 医生审核信息写回数据库
// @Description 医生审核信息写回数据库
// @Description status：
// @Description 200 创建
// @tags API1 医疗报告（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param predictupdate body controllers.predictupdate true "医生审核信息"
// @Success 200 {string} json "{"ping": "ok",	"status": 200}"
// @Router /api1/updatepredict [post]
func UpdatePredict(c *gin.Context) {
	pu := predictupdate{}
	err := c.ShouldBindJSON(&pu)
	if err != nil {
		res.ResFailedStatus(c, e.Errors["PostDataInvalied"])
		return
	}

	models.UpdatePredict(pu.ID, pu.TrueType)

	res.ResSucceedString(c, "ok")
	return
}

type predictreview struct {
	ID     int64 `json:"id"`     // 细胞预测的（医生审核的信息）ID
	Status int   `json:"status"` // 管理员检查结果，2 错误 3 正确(对应于预测的状态 0 未审核 1 已审核 2 移除 3 管理员确认)
}

// ReviewPredict 管理员检查医生审核过后的信息
// @Summary 管理员检查医生审核过后的信息
// @Description 管理员检查医生审核过后的信息
// @Description status：
// @Description 200 创建
// @tags API1 医疗报告（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param predictreview body controllers.predictreview true "管理员检查结果"
// @Success 200 {string} json "{"ping": "ok",	"status": 200}"
// @Router /api1/reviewpredict [post]
func ReviewPredict(c *gin.Context) {
	pr := predictreview{}
	err := c.ShouldBindJSON(&pr)
	if err != nil {
		res.ResFailedStatus(c, e.Errors["PostDataInvalied"])
		return
	}

	models.ReviewPredict(pr.ID, pr.Status)

	res.ResSucceedString(c, "ok")
	return
}
