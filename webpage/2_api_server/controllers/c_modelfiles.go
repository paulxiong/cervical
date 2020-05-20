package controllers

import (
	"strconv"

	"github.com/gin-gonic/gin"
	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
	f "github.com/paulxiong/cervical/webpage/2_api_server/functions"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	models "github.com/paulxiong/cervical/webpage/2_api_server/models"
	res "github.com/paulxiong/cervical/webpage/2_api_server/responses"
	u "github.com/paulxiong/cervical/webpage/2_api_server/utils"
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

// UploadModelHandler 上传模型文件,并记录到数据集
// @Summary 上传模型文件,并记录到数据集
// @Description 上传模型文件,并记录到数据集，postdata的参数：
// @Description type　0未知 1UNET 2GAN 3SVM 4MASKRCNN 5AUTOKERAS 6MALA
// @Description pid  从那个项目训练的，不知道就给0
// @Description description 模型描述的字符串
// @Description precision1 模型的准确率
// @Description recall 模型的召回率
// @tags API1 模型（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Router /api1/uploadmodel [post]
func UploadModelHandler(c *gin.Context) {
	_typeStr := c.DefaultPostForm("type", "") // 0未知 1UNET 2GAN 3SVM 4MASKRCNN 5AUTOKERAS 6MALA
	_pidStr := c.DefaultPostForm("pid", "0")
	_description := c.DefaultPostForm("description", "")
	_precision1Str := c.DefaultPostForm("precision1", "0")
	_recallStr := c.DefaultPostForm("recall", "0")
	_type, _ := strconv.ParseInt(_typeStr, 10, 64)
	_pid, _ := strconv.ParseInt(_pidStr, 10, 64)
	_precision1, _ := strconv.ParseFloat(_precision1Str, 64)
	_recall, _ := strconv.ParseFloat(_recallStr, 64)

	if len(_description) < 1 {
		res.ResFailedStatus(c, e.Errors["ModelSaveNoDescription"])
		return
	}

	file, err := c.FormFile("file")
	if err != nil {
		res.ResFailedStatus(c, e.Errors["UploadGetFileNameFailed"])
		return
	}

	filename := u.GetUUID() + ".h5"
	modpath := f.NewModulePath(int(_type), filename)
	err2 := c.SaveUploadedFile(file, modpath)
	if err2 != nil {
		logger.Info(err2)
		res.ResFailedStatus(c, e.Errors["UploadSaveFailed"])
		return
	}

	_u, _ := models.GetUserFromContext(c)

	// 保存模型信息到数据库
	md := models.Model{
		ID:        0,
		Type:      int(_type),
		PID:       _pid,
		Path:      modpath,
		Desc:      _description,
		Precision: float32(_precision1),
		Recall:    float32(_recall),
		CreatedBy: _u.ID,
	}
	md.CreateModelInfo()

	res.ResSucceedString(c, "ok")
	return
}
