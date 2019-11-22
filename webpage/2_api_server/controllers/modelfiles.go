package controllers

import (
	"strconv"

	"github.com/gin-gonic/gin"
	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
	f "github.com/paulxiong/cervical/webpage/2_api_server/functions"
	models "github.com/paulxiong/cervical/webpage/2_api_server/models"
	res "github.com/paulxiong/cervical/webpage/2_api_server/responses"
)

type listMods struct {
	Models []models.Model `json:"models"`
	Total  int64          `json:"total"`
}

// GetModelLists 获得模型的信息列表
// @Summary 获得模型的信息列表
// @Description 获得模型的信息列表
// @tags API1 模型（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param limit query string false "limit, default 10"
// @Param skip query string false "skip, default 0"
// @Param type query string false "type, default 52, 模型类型，0未知 1UNET 2GAN 3SVM 4MASKRCNN 5AUTOKERAS 6MALA 50全部的裁剪模型(没做) 51全部的分类模型 52全部模型"
// @Success 200 {object} controllers.listMods
// @Router /api1/listmodel [get]
func GetModelLists(c *gin.Context) {
	limitStr := c.DefaultQuery("limit", "10")
	skipStr := c.DefaultQuery("skip", "0")
	typeStr := c.DefaultQuery("type", "4")
	limit, _ := strconv.ParseInt(limitStr, 10, 64)
	skip, _ := strconv.ParseInt(skipStr, 10, 64)
	_type, _ := strconv.ParseInt(typeStr, 10, 64)

	lm := listMods{}
	total, mods, _ := models.ListModel(int(limit), int(skip), int(_type))
	lm.Models = mods
	lm.Total = total

	res.ResSucceedStruct(c, lm)
	return
}

type savemod struct {
	ID   int64  `json:"id"   example:"1"`          //项目的ID
	Desc string `json:"desc" example:"某某的训练得到的模型"` //模型的文字描述
}

// SaveModelInfo 把训练任务生成模型信息存数据库
// @Summary 把训练任务生成模型信息存数据库
// @Description 把训练任务生成模型信息存数据库, 模型信息直接从后端取，前端不需要传回去
// @tags API1 模型（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param SaveModel body controllers.savemod true "保存模型的信息"
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/savemodel [post]
func SaveModelInfo(c *gin.Context) {
	w := savemod{}
	err := c.BindJSON(&w)

	p, err := models.GetOneProjectByID(int(w.ID))
	if err != nil || p.Status != 4 {
		res.ResFailedStatus(c, e.Errors["ProjectNotReady"])
		return
	}

	modinfo := f.LoadModJSONFile(p.Dir)
	if modinfo.Path == "" {
		res.ResFailedStatus(c, e.Errors["ModelInfoNotFound"])
		return
	}

	ret := modinfo.ModelInfoSaved()
	if ret == true {
		res.ResFailedStatus(c, e.Errors["ModelAlreadySaved"])
		return
	}

	modinfo.ID = 0
	modinfo.Desc = w.Desc

	err = modinfo.CreateModelInfo()
	if err == nil {
		res.ResSucceedString(c, "ok")
	} else {
		res.ResFailedStatus(c, e.Errors["ModelSaveFailed"])
	}
	return
}
