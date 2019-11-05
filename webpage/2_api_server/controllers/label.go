package controllers

import (
	"strconv"

	"github.com/gin-gonic/gin"

	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	models "github.com/paulxiong/cervical/webpage/2_api_server/models"
)

// Labelslists 标注信息
type Labelslists struct {
	Labels []models.Label `json:"labels"`
	W      int            `json:"imgw" example:"1024"`
	H      int            `json:"imgh" example:"768"`
}

// GetLabelByImageID 通过图片的ID获得对应的所有标注信息
// @Summary 通过图片的ID获得对应的所有标注信息
// @Description 通过图片的ID获得对应的所有标注信息
// @tags API1 标注（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param limit query string false "limit, default 10"
// @Param skip query string false "skip, default 0"
// @Param imgid query string false "imgid, default 1， 表示图片的ID"
// @Success 200 {object} controllers.Labelslists
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/getLabelbyimageid [get]
func GetLabelByImageID(c *gin.Context) {
	limitStr := c.DefaultQuery("limit", "10")
	skipStr := c.DefaultQuery("skip", "0")
	imgidStr := c.DefaultQuery("imgid", "1")
	imgid, _ := strconv.ParseInt(imgidStr, 10, 32)
	limit, _ := strconv.ParseInt(limitStr, 10, 32)
	skip, _ := strconv.ParseInt(skipStr, 10, 32)

	labels := Labelslists{}
	labels.Labels = make([]models.Label, 0)

	img, err := models.GetImageByID(imgid)
	if err == nil {
		labels.W = img.W
		labels.H = img.H
	}

	total, _labels, _ := models.ListLabelByImageID(int(limit), int(skip), int(imgid))
	for _, v := range _labels {
		_c, _ := models.GetCategoryByID(v.Type)
		v.TypeOut = _c.Name
		labels.Labels = append(labels.Labels, v)
	}

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   labels,
		"total":  total,
	})

	return
}

type labelResult struct {
	ImgID   int64 `json:"imgid"   example:"1"`   // 被标注图片的ID
	LabelID int64 `json:"labelid" example:"2"`   // 标注的ID，删除以及修改时候有用
	Op      int   `json:"op"      example:"1"`   // 操作， 0未知 1增加 2删除 3修改
	TypeID  int   `json:"typeid"  example:"7"`   // 细胞类型的ID
	X1      int   `json:"x1"      example:"0"`   // 左上角X
	Y1      int   `json:"y1"      example:"0"`   // 左上角Y
	X2      int   `json:"x2"      example:"100"` // 右下角X
	Y2      int   `json:"y2"      example:"100"` // 右下角Y
}

type labelsResult struct {
	Labels []labelResult
}

// UpdateLabelsOfImage 标注信息的增删改
// @Summary 标注信息的增删改
// @Description 标注信息的增删改
// @tags API1 标注（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param CreateProject body controllers.labelsResult true "某张图片的标注增删改查的信息"
// @Success 200 {string} json "{"data": "ok",	"status": 200}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/updatelabelsofimage [POST]
func UpdateLabelsOfImage(c *gin.Context) {
	var lr labelsResult
	err := c.ShouldBindJSON(&lr)
	if err != nil {
		ResString(c, "invalied labels")
		return
	}

	for _, v := range lr.Labels {
		logger.Info.Println(v)
		if v.Op == 0 || v.Op > 3 {
			ResString(c, "invalied labels 2")
			return
		} else if v.Op == 1 {
			ladd := &models.Label{
				ID:     0,
				Imgid:  v.ImgID,
				Type:   v.TypeID,
				X:      v.X1,
				Y:      v.Y1,
				W:      v.X2,
				H:      v.Y2,
				Status: 0,
			}
			ladd.InsertLabel()
			logger.Info.Println("add")
		} else if v.Op == 2 {
			logger.Info.Println("remove")
		} else if v.Op == 3 {
			logger.Info.Println("update")
		}
	}

	//ResStructTotal(c, labels, int(total))

	return
}
