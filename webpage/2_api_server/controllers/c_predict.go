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
	Total    int                 `json:"total"  example:"100"` // 总细胞预测数量
	Predicts []models.Predict    `json:"cells"`                // 每个细胞
	Info     returnpredictupdate `json:"info"`                 // 当前图片审核进度，项目审核进度
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
// @Param pid query string false "pid, default 0, 所属项目的ID"
// @Param iid query string false "iid, default 0, 图片ID"
// @Param limit query string false "limit, default 1"
// @Param skip query string false "skip, default 0"
// @Param status query string false "status, default 0, 0 未审核 1 已审核 2 移除 3 管理员已确认 4 未审核+已审核"
// @Success 200 {object} controllers.reporterpredicts
// @Router /api1/predictresult2 [get]
func GetPredictResult2(c *gin.Context) {
	pidStr := c.DefaultQuery("pid", "0")
	iidStr := c.DefaultQuery("iid", "0")
	limitStr := c.DefaultQuery("limit", "1")
	skipStr := c.DefaultQuery("skip", "0")
	statusStr := c.DefaultQuery("status", "0")
	pid, _ := strconv.ParseInt(pidStr, 10, 64)
	iid, _ := strconv.ParseInt(iidStr, 10, 64)
	limit, _ := strconv.ParseInt(limitStr, 10, 64)
	skip, _ := strconv.ParseInt(skipStr, 10, 64)
	status, _ := strconv.ParseInt(statusStr, 10, 64)

	total, predicts, _ := models.ListPredict(int(limit), int(skip), int(pid), int(iid), int(status))
	_predicts := reporterpredicts{
		Total:    int(total),
		Predicts: predicts,
	}
	if len(predicts) > 0 {
		pid := predicts[0].PID
		// 状态0 未审核 1 已审核 2 移除 3 管理员确认
		// 项目所有细胞，　项目已经审核的细胞，　当前图片的所有细胞，当前图片已经审核的细胞，
		cntCellsAll, cntCellsVerified, cntImgCellsAll, cntImgCellsVerified := models.GetPredictPercentByImgID(iid, pid, 1)
		_predicts.Info.CntCellsAll = cntCellsAll
		_predicts.Info.CntCellsVerified = cntCellsVerified
		_predicts.Info.CntImgCellsAll = cntImgCellsAll
		_predicts.Info.CntImgCellsVerified = cntImgCellsVerified
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

	rimgs := reporterimgs{}
	rimgs.Imgs = make([]reporterimg, 0)
	for _, mid := range _d.MedicalIDs1 {
		total, imgs, _ := models.ListImagesByMedicalID2(mid)
		rimgs.Total = rimgs.Total + total

		for _, v := range imgs {
			rimgs.Imgs = append(rimgs.Imgs, reporterimg{
				ID:      v.ID,
				Imgpath: f.Imgpath(v.Batchid, v.Medicalid, v.Imgpath, v.Type),
				W:       v.W,
				H:       v.H,
			})
		}
	}

	res.ResSucceedStruct(c, rimgs)
	return
}

type predictupdate struct {
	ID int64 `json:"id"` // 细胞预测的ID
	// PID      int64 `json:"id"`        // 当前项目的ID
	TrueType int `json:"true_type"` // 审核细胞类型,1到15是细胞类型, 50 阴性 51 阳性 100 未知, 200 不是细胞
}

type returnpredictupdate struct {
	CntCellsAll         int `json:"cellsall"`         // 项目所有细胞
	CntCellsVerified    int `json:"cellsverified"`    // 项目已经审核的细胞
	CntImgCellsAll      int `json:"imgcellsall"`      // 当前图片的所有细胞
	CntImgCellsVerified int `json:"imgcellsverified"` // 前图片已经审核的细胞，
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
// @Success 200 {object} controllers.returnpredictupdate
// @Router /api1/updatepredict [post]
func UpdatePredict(c *gin.Context) {
	pu := predictupdate{}
	err := c.ShouldBindJSON(&pu)
	if err != nil {
		res.ResFailedStatus(c, e.Errors["PostDataInvalied"])
		return
	}

	usr, _ := models.GetUserFromContext(c)

	models.UpdatePredict(pu.ID, pu.TrueType, usr.ID)

	// 状态0 未审核 1 已审核 2 移除 3 管理员确认
	// 项目所有细胞，　项目已经审核的细胞，　当前图片的所有细胞，当前图片已经审核的细胞，
	cntCellsAll, cntCellsVerified, cntImgCellsAll, cntImgCellsVerified := models.GetPredictPercent(pu.ID, 1)
	rpu := returnpredictupdate{
		CntCellsAll:         cntCellsAll,
		CntCellsVerified:    cntCellsVerified,
		CntImgCellsAll:      cntImgCellsAll,
		CntImgCellsVerified: cntImgCellsVerified,
	}

	res.ResSucceedStruct(c, rpu)
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

type predictstatisticscells struct {
	Type  int `json:"type"  example:"100"` // 图片ID
	Total int `json:"total" example:"100"` // 预测细胞类型的统计
}
type predictstatisticsimg struct {
	ID    int64                    `json:"id" example:"100"` // 图片ID
	Cells []predictstatisticscells `json:"cells"`            // 预测细胞类型的统计
}
type predictstatistics struct {
	Total int                    `json:"total"` // 当前项目总的图片个数
	Imgs  []predictstatisticsimg `json:"imgs"`  // 预测图片的统计
}

// GetPredictStatistics 统计当前预测报告的每个图片里面细胞分类的个数
// @Summary 统计当前预测报告的每个图片里面细胞分类的个数
// @Description 统计当前预测报告的每个图片里面细胞分类的个数
// @Description status：
// @tags API1 医疗报告（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param pid query string false "pid, default 0, 所属项目的ID"
// @Success 200 {object} controllers.reporterpredicts
// @Router /api1/predictstatistics [get]
func GetPredictStatistics(c *gin.Context) {
	pidStr := c.DefaultQuery("pid", "0")
	pid, _ := strconv.ParseInt(pidStr, 10, 64)

	project, err := models.GetOneProjectByID(int(pid))
	if err != nil {
		res.ResFailedStatus(c, e.Errors["ProjectNotReady"])
		return
	}

	_d, err := models.GetOneDatasetByID(int(project.DID))
	if err != nil || len(_d.MedicalIDs1) < 1 {
		res.ResFailedStatus(c, e.Errors["DatasetsNotFound"])
		return
	}

	ps := predictstatistics{}
	ps.Imgs = make([]predictstatisticsimg, 0)
	for _, mid := range _d.MedicalIDs1 {
		total, imgs, _ := models.ListImagesByMedicalID2(mid)
		ps.Total = ps.Total + total
		// 遍历病例下面的所有图片
		for _, v := range imgs {
			psi := predictstatisticsimg{
				ID: v.ID,
			}
			psi.Cells = make([]predictstatisticscells, 0)
			predicts, _ := models.GetPredictByImgID(pid, v.ID)
			cells := make(map[int]int, 0)
			// 遍历图片下面的所有细胞
			for _, p := range predicts {
				key := p.PredictType
				if _, ok := cells[key]; ok {
					cells[key] = cells[key] + 1
				} else {
					cells[key] = 1
				}
			}
			for key, value := range cells {
				psi.Cells = append(psi.Cells, predictstatisticscells{
					Type:  key,
					Total: value,
				})
			}
			ps.Imgs = append(ps.Imgs, psi)
		}
	}

	res.ResSucceedStruct(c, ps)
	return
}

// GetPredictCnt 统计医生审核的总次数
// @Summary 统计医生审核的总次数
// @Description 统计医生审核的总次数
// @Description status：
// @tags API1 医疗报告（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {object} models.PredictCount
// @Router /api1/verificationcnt [get]
func GetPredictCnt(c *gin.Context) {
	pcnt := models.GetPredictCount()
	res.ResSucceedStruct(c, pcnt)
	return
}
