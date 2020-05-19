package controllers

import (
	"strconv"

	"github.com/gin-gonic/gin"

	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	models "github.com/paulxiong/cervical/webpage/2_api_server/models"
	res "github.com/paulxiong/cervical/webpage/2_api_server/responses"
)

type label2Result struct {
	LabelID string `json:"labelid" example:"2"`   // 标注的ID，删除以及修改时候有用
	PreID   int64  `json:"preid"   example:"2"`   // 预测的ID 人工标注的默认是0
	PID     int64  `json:"pid"     example:"2"`   // 项目ID
	DID     int64  `json:"did"     example:"2"`   // 数据集ID
	Op      int    `json:"op"      example:"1"`   // 操作， 0未知 1增加 2删除 3修改
	TypeID  int    `json:"typeid"  example:"7"`   // 细胞类型的ID
	X1      int    `json:"x1"      example:"0"`   // 左上角X
	Y1      int    `json:"y1"      example:"0"`   // 左上角Y
	X2      int    `json:"x2"      example:"100"` // 右下角X
	Y2      int    `json:"y2"      example:"100"` // 右下角Y
}

type label2sResult struct {
	Label2s []label2Result
	Total   int64 `json:"total" example:"1"`
}

// UpdateLabel2s 标注信息的增删改
// @Summary 标注信息的增删改
// @Description 标注信息的增删改
// @tags API1 标注2（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param CreateProject body controllers.label2sResult true "某张图片的标注增删改查的信息"
// @Success 200 {string} json "{"data": "ok",	"status": 200}"
// @Router /api1/updatelabel2s [POST]
func UpdateLabel2s(c *gin.Context) {
	var lr label2sResult
	err := c.ShouldBindJSON(&lr)
	if err != nil {
		res.ResFailedStatus(c, e.Errors["PostDataInvalied"])
		return
	}

	for _, v := range lr.Label2s {
		if v.Op == 0 || v.Op > 3 || ((v.Op == 2 || v.Op == 3) && v.LabelID == "") {
			res.ResFailedStatus(c, e.Errors["Label2Invalied"])
			return
		}
		newl := &models.Label2{
			ID:     v.LabelID,
			PreID:  v.PreID,
			PID:    v.PID,
			DID:    v.DID,
			TypeID: v.TypeID,
			X1:     v.X1,
			Y1:     v.Y1,
			X2:     v.X2,
			Y2:     v.Y2,
			Status: 0,
		}
		if newl.X1 < 0 || newl.Y1 < 0 || newl.X2 <= newl.X1 || newl.Y2 <= newl.Y1 {
			logger.Info.Println("Label2Invalie 2")
			res.ResFailedStatus(c, e.Errors["LabelInvalied"])
			return
		}

		if v.Op == 1 {
			newl.InsertLabel2()
		} else if v.Op == 2 {
			newl.RemoveLabel2()
		} else if v.Op == 3 {
			newl.UpdateLabel2()
		}
	}

	res.ResSucceedString(c, "ok")
	return
}

// GetLabel2ByPID 通过项目的ID获得对应的所有标注信息
// @Summary 通过项目的ID获得对应的所有标注信息
// @Description 通过项目的ID获得对应的所有标注信息
// @tags API1 标注2（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param limit query string false "limit, default 10"
// @Param skip query string false "skip, default 0"
// @Param status query string false "status, default 10, 0 未审核 1 已审核 2 移除 10 审核+未审核的"
// @Param pid query string false "pid, default 1， 表示项目的ID"
// @Success 200 {object} controllers.label2sResult
// @Router /api1/label2sbypid [get]
func GetLabel2ByPID(c *gin.Context) {
	limitStr := c.DefaultQuery("limit", "10")
	skipStr := c.DefaultQuery("skip", "0")
	pidStr := c.DefaultQuery("pid", "1")
	statusStr := c.DefaultQuery("status", "10")
	pid, _ := strconv.ParseInt(pidStr, 10, 32)
	limit, _ := strconv.ParseInt(limitStr, 10, 32)
	skip, _ := strconv.ParseInt(skipStr, 10, 32)
	_status, _ := strconv.ParseInt(statusStr, 10, 32)

	label2s := label2sResult{}
	label2s.Label2s = make([]label2Result, 0)

	total, _label2s, _ := models.ListLabel2ByPid(int(limit), int(skip), int(pid))
	for _, v := range _label2s {
		if _status == 10 {
			if v.Status != 0 && v.Status != 1 {
				continue
			}
		} else if int(_status) != v.Status {
			continue
		}
		label2s.Label2s = append(label2s.Label2s, label2Result{
			LabelID: v.ID,
			PreID:   v.PreID,
			PID:     v.PID,
			DID:     v.DID,
			TypeID:  v.TypeID,
			X1:      v.X1,
			Y1:      v.Y1,
			X2:      v.X2,
			Y2:      v.Y2,
		})
	}
	label2s.Total = total
	res.ResSucceedStruct(c, label2s)
	return
}
