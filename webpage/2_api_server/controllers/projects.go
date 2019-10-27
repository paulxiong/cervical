package controllers

import (
	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
	f "github.com/paulxiong/cervical/webpage/2_api_server/functions"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	m "github.com/paulxiong/cervical/webpage/2_api_server/models"
	u "github.com/paulxiong/cervical/webpage/2_api_server/utils"

	"github.com/gin-gonic/gin"
)

// newProject 新建项目
type newProject struct {
	Desc      string `json:"desc" example:"this is a project"` //项目的描述
	DID       int64  `json:"did"  example:"1"`                 //选择的数据集的ID
	Type      int    `json:"type" example:"1"`                 //项目类型 0 未知 1 训练 2 预测
	Celltypes []int  `json:"celltypes" example:"7"`            //选择哪几个类型做训练或者预测
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

	p := m.Project{
		ID:     0,
		DID:    np.DID,
		Desc:   np.Desc,
		Dir:    u.GetRandomSalt(),
		Status: 0,
		Type:   np.Type,
	}

	logger.Info.Println(np.Desc)
	logger.Info.Println(np.DID)

	p.CreateProject()

	f.NewProjectJSONFile(p.ID, np.Celltypes, p.Dir, p.Status, p.Type, p.DID)

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   "ok",
	})
	return
}
