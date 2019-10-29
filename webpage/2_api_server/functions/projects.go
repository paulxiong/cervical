package function

import (
	"encoding/json"
	"log"

	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	"github.com/paulxiong/cervical/webpage/2_api_server/models"
	m "github.com/paulxiong/cervical/webpage/2_api_server/models"
)

// ProjectInfo 项目的描述信息, 存到工作目录的info.json
type ProjectInfo struct {
	ID              int64  `json:"id"      example:"1"`             //任务ID
	DID             int64  `json:"did"     example:"1"`             //数据集的id
	DDir            string `json:"ddir"    example:"dataset dir"`   //数据集的目录
	Dir             string `json:"dir"     example:"project dir"`   //项目任务执行的目录名，调试时候很有用
	Status          int    `json:"status"  example:"4"`             //任务的状态码
	Type            int    `json:"type"    example:"1"`             //项目类型 0 未知 1 训练 2 预测
	Types           []int  `json:"types"   example:"7"`             //训练哪几个类型的细胞
	ModPath         string `json:"modpath" example:"path of model"` //模型文件的路径
	ParameterTime   int    `json:"parameter_time"   example:"1800"` //训练使用的最长时间
	ParameterResize int    `json:"parameter_resize" example:"100"`  //训练之前统一的尺寸
	ParameterMID    int    `json:"parameter_mid"    example:"1"`    //预测使用的模型的id,只有预测时候需要
	ParameterType   int    `json:"parameter_type"   example:"0"`    //预测方式,0没标注的图 1有标注的图
}

// NewProjectJSONFile 创建项目
func NewProjectJSONFile(project models.Project, types []int) {
	dt, _ := m.GetOneDatasetByID(int(project.DID))

	_mod, _ := m.FindModelInfoByID(project.ParameterMID)

	p := ProjectInfo{
		ID:              project.ID,
		DID:             project.DID,
		DDir:            dt.Dir,
		Dir:             project.Dir,
		Status:          project.Status,
		Type:            project.Type,
		Types:           types,
		ModPath:         _mod.Path,
		ParameterTime:   project.ParameterTime,
		ParameterResize: project.ParameterResize,
		ParameterMID:    project.ParameterMID,
		ParameterType:   project.ParameterType,
	}
	data, err := json.MarshalIndent(p, "", " ") //这里返回的data值，类型是[]byte
	if err != nil {
		log.Println("ERROR:", err)
	}
	info := projectsDir + "/" + project.Dir + "/info.json"
	logger.Info.Println(info)
	writeJSON(info, data)
}
