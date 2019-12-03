package controllers

import (
	"github.com/gin-gonic/gin"
	models "github.com/paulxiong/cervical/webpage/2_api_server/models"
	res "github.com/paulxiong/cervical/webpage/2_api_server/responses"
)

type overview struct {
	UserCnt    int   `json:"usercnt"    example:"100"` // 用户总数
	ImgCnt     int64 `json:"imgcnt"     example:"100"` // 图片总数
	DataSetCnt int64 `json:"datasetcnt" example:"100"` // 数据集总数
	ProjectCnt int64 `json:"projectcnt" example:"100"` // 项目总数
}

// GetOverview 获得概览统计信息
// @Summary 获得概览统计信息
// @Description 获得概览统计信息
// @tags API1 数据（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {object} controllers.overview
// @Router /api1/overview [get]
func GetOverview(c *gin.Context) {
	ov := overview{}
	_, ov.UserCnt, _ = models.UserLists(0, 0, 0)
	ov.ImgCnt, _, _ = models.ListImage(0, 0)
	ov.DataSetCnt, _, _ = models.ListDataset(0, 0, 0)
	ov.ProjectCnt, _, _ = models.ListProject(0, 0, 0, 0)

	res.ResSucceedStruct(c, ov)
	return
}
