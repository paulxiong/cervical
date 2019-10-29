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
	DID             int64  `json:"did"              example:"1"`                 //选择的数据集的ID
	Type            int    `json:"type"             example:"1"`                 //项目类型 0 未知 1 训练 2 预测
	Celltypes       []int  `json:"celltypes"        example:"7"`                 //选择哪几个类型做训练或者预测
	ParameterTime   int    `json:"parameter_time"   example:"1800"`              //训练使用的最长时间,单位是秒
	ParameterResize int    `json:"parameter_resize" example:"100"`               //训练之前统一的尺寸,单位是像素
}

// CreateProject 新建项目
// @Summary 新建项目
// @Description 新建项目
// @tags API1 项目（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param CreateProject body controllers.newProject true "创建项目"
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
	}

	logger.Info.Println(np.Desc)
	logger.Info.Println(np.DID)

	p.CreateProject()

	f.NewProjectJSONFile(p, np.Celltypes)

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   "ok",
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
