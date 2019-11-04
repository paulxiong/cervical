package controllers

import (
	"strconv"

	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
	f "github.com/paulxiong/cervical/webpage/2_api_server/functions"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	models "github.com/paulxiong/cervical/webpage/2_api_server/models"
	u "github.com/paulxiong/cervical/webpage/2_api_server/utils"

	"github.com/gin-gonic/gin"
)

// newProject 新建项目
type newProject struct {
	Desc            string `json:"desc"             example:"this is a project"` //项目的描述
	DID             int64  `json:"did"              example:"1"`                 //选择的数据集的ID, 训练项目表示训练和评估数据集， 预测项目表示预测使用的数据
	Type            int    `json:"type"             example:"1"`                 //项目类型 0 未知 1 保留 2 训练 3 预测
	Celltypes       []int  `json:"celltypes"        example:"7"`                 //选择哪几个类型做训练或者预测
	ParameterTime   int    `json:"parameter_time"   example:"1800"`              //训练使用的最长时间,单位是秒
	ParameterResize int    `json:"parameter_resize" example:"100"`               //训练/预测之前统一的尺寸,单位是像素
	ParameterMID    int    `json:"parameter_mid"    example:"1"`                 //预测使用的模型的id,只有预测时候需要
	ParameterType   int    `json:"parameter_type"   example:"0"`                 //预测方式,0没标注的图 1有标注的图
}

// CreateProject 新建(训练/预测)项目
// @Summary 新建(训练/预测)项目
// @Description 新建(训练/预测)项目
// @tags API1 项目（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param CreateProject body controllers.newProject true "新建(训练/预测)项目"
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/createproject [post]
func CreateProject(c *gin.Context) {
	np := newProject{}
	err := c.BindJSON(&np)
	if err != nil {
		logger.Info.Println(err)
		c.JSON(e.StatusReqOK, gin.H{
			"status": e.StatusSucceed,
			"data":   "invalied data",
		})
		return
	}

	p := models.Project{
		ID:              0,
		DID:             np.DID,
		Desc:            np.Desc,
		Dir:             u.GetRandomSalt(),
		Status:          1, //送去处理
		Type:            np.Type,
		ParameterTime:   np.ParameterTime,
		ParameterResize: np.ParameterResize,
		ParameterMID:    np.ParameterMID,
		ParameterType:   np.ParameterType,
	}

	_mod, _ := models.FindModelInfoByID(p.ParameterMID)
	p.ParameterMType = _mod.Type

	logger.Info.Println(np.Desc)
	logger.Info.Println(np.DID)

	p.CreateProject()

	f.NewProjectJSONFile(p, np.Celltypes, _mod)

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   p.ID,
	})
	return
}

type listProjectsData struct {
	Projects []models.Project `json:"projects"` //项目列表的数组
	Total    int64            `json:"total"`    //项目总个数
}

// ListProjects 按数据库存储顺序依次获得项目信息
// @Summary 按数据库存储顺序依次获得项目信息
// @Description 按数据库存储顺序依次获得项目信息
// @tags API1 项目（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param limit query string false "limit, default 1"
// @Param skip query string false "skip, default 0"
// @Param order query string false "order, default 1, 1倒序，0顺序，顺序是指创建时间"
// @Success 200 {object} controllers.listProjectsData
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/listprojects [get]
func ListProjects(c *gin.Context) {
	limitStr := c.DefaultQuery("limit", "1")
	skipStr := c.DefaultQuery("skip", "0")
	orderStr := c.DefaultQuery("order", "1")
	limit, _ := strconv.ParseInt(limitStr, 10, 64)
	skip, _ := strconv.ParseInt(skipStr, 10, 64)
	_order, _ := strconv.ParseInt(orderStr, 10, 64)

	total, p, err := models.ListProject(int(limit), int(skip), int(_order))
	if err != nil {
		logger.Info.Println(err)
	}

	dts := listProjectsData{}
	dts.Projects = p
	dts.Total = total

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   dts,
	})
	return
}

// GetTrainResult 根据传递来的项目ID，获取训练结果及信息
// @Summary 根据传递来的项目ID，获取训练结果及信息
// @Description 根据传递来的项目ID，获取训练结果及信息
// @Description status：
// @Description 200 成功
// @tags API1 项目（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param id query string false "项目的ID, default 0"
// @Success 200 {object} models.Model
// @Router /api1/trainresult [get]
func GetTrainResult(c *gin.Context) {
	idStr := c.DefaultQuery("id", "1")
	id, _ := strconv.ParseInt(idStr, 10, 64)

	d, err := models.GetOneProjectByID(int(id))
	if err != nil || d.Status != 4 {
		c.JSON(e.StatusReqOK, gin.H{
			"status": e.StatusSucceed,
			"data":   "datasets trainning not finished or not found",
		})
		return
	}

	modinfo := f.LoadModJSONFile(d.Dir)

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   modinfo,
	})
	return
}

// GetPredictResult 根据传递来的项目ID，返回预测的结果
// @Summary 根据传递来的项目ID，返回预测的结果
// @Description 创建预测任务
// @Description status：
// @Description 200 创建
// @tags API1 项目（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param id query string false "id, default 0, 项目ID"
// @Success 200 {object} function.PredictInfo2
// @Router /api1/predictresult [get]
func GetPredictResult(c *gin.Context) {
	idStr := c.DefaultQuery("id", "0")
	id, _ := strconv.ParseInt(idStr, 10, 64)

	dinfo, err := models.GetOneProjectByID(int(id))
	if err != nil {
		c.JSON(e.StatusReqOK, gin.H{
			"status": e.StatusSucceed,
			"data":   "datasets info not found",
		})
		return
	}

	str := f.LoadPredictJSONFile(dinfo.Dir)

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   str,
	})
	return
}
