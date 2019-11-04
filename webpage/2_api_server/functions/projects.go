package function

import (
	"encoding/json"
	"io/ioutil"
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
func NewProjectJSONFile(project models.Project, types []int, _mod *models.Model) {
	dt, _ := m.GetOneDatasetByID(int(project.DID))

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

// TrainJobInfo 存在硬盘的JSON文件，描述每个训练任务的属性，train.json是初始化时候，train2.json是训练结束之后
type TrainJobInfo struct {
	ID     int64  `json:"id"     example:"1"`    //任务ID
	Status int    `json:"status" example:"4"`    //任务的状态码
	Dir    string `json:"dir"    example:"任务目录"` //任务执行的目录名，调试时候很有用
	Types  []int  `json:"types"  example:"7"`    //训练哪几个类型的细胞
}

// NewTrainJSONFile 创建训练任务的时候把任务的部分信息存到JSON文件
func NewTrainJSONFile(id int64, types []int, dirname string, status int) {
	t := TrainJobInfo{
		ID:     id,
		Dir:    dirname,
		Types:  types,
		Status: status,
	}
	data, err := json.MarshalIndent(t, "", " ") //这里返回的data值，类型是[]byte
	if err != nil {
		log.Println("ERROR:", err)
	}
	info := scratchRoot + "/" + dirname + "/train.json"
	logger.Info.Println(info)
	writeJSON(info, data)
}

// LoadTrainJSONFile 加载json文件内容成struct
func LoadTrainJSONFile(filename string) TrainJobInfo {
	j := TrainJobInfo{}
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		return j
	}
	err = json.Unmarshal(data, &j)
	if err != nil {
		return j
	}
	return j
}

// PredictInfo 存在硬盘的JSON文件，描述预测数据集和模型
type PredictInfo struct {
	ID    int64  `json:"id"    example:"1"`    //预测任务ID
	DID   int64  `json:"did"   example:"1"`    //用来做预测的数据集的ID
	MID   int64  `json:"mid"   example:"1"`    //用来做预测的模型ID
	Types []int  `json:"types" example:"7"`    //预测哪几个类型的细胞
	DDir  string `json:"ddir"  example:"任务目录"` //用来做预测的数据集的目录
	// MDir  string `json:"mdir"  example:"任务目录"` //用来做预测的模型的目录
	MPath string `json:"mpath"  example:"模型文件的路径"` //模型文件的路径
}

// NewPredictJSONFile 创建预测任务的时候把任务的部分信息存到JSON文件
func (p *PredictInfo) NewPredictJSONFile() {
	dirname := p.DDir

	data, err := json.MarshalIndent(p, "", " ") //这里返回的data值，类型是[]byte
	if err != nil {
		log.Println("ERROR:", err)
	}
	info := scratchRoot + "/" + dirname + "/predict.json"
	logger.Info.Println(info)
	writeJSON(info, data)
}

// PredictRsult 预测的细胞的个数统计
type PredictRsult struct {
	Type    string `json:"type"      example:"1"`  //细胞类型
	Total   int    `json:"total"     example:"35"` //总共送去预测的细胞个数
	Correct int    `json:"correct"   example:"18"` //预测正确的个数
	//TotalOrg int    `json:"total_org" example:"37"` //总共送去预测的细胞原始个数，部分细胞图片不是正方形会被丢弃
}

// PredictCell 预测的细胞的信息
type PredictCell struct {
	URL     string `json:"url"     example:"任务目录"` //细胞路径用来拼接出URL
	Type    string `json:"type"    example:"1"`    //细胞类型
	Predict string `json:"predict" example:"1"`    //细胞预测为什么类型
}

// PredictInfo2 存在硬盘的JSON文件，描述预测数据集和模型以及预测结果
type PredictInfo2 struct {
	ID   int64  `json:"id"    example:"1"`    //预测任务ID
	DID  int64  `json:"did"   example:"1"`    //用来做预测的数据集的ID
	DDir string `json:"ddir"  example:"任务目录"` //用来做预测的数据集的目录
	// MDir  string `json:"mdir"  example:"任务目录"` //用来做预测的模型的目录
	// MPath string `json:"mpath"  example:"模型文件的路径"` //模型文件的路径

	PRsult          []PredictRsult `json:"result"`                          //预测的细胞的个数统计
	Cells           []PredictCell  `json:"crop_cells"`                      //预测的细胞的信息
	ParameterTime   int            `json:"parameter_time"   example:"1800"` //训练使用的最长时间
	ParameterResize int            `json:"parameter_resize" example:"100"`  //训练之前统一的尺寸
	ParameterMID    int            `json:"parameter_mid"    example:"1"`    //预测使用的模型的id,只有预测时候需要
	ParameterType   int            `json:"parameter_type"   example:"3"`    //预测方式,0没标注的图1有标注的图
}

// LoadPredictJSONFile 加载json文件内容成struct
func LoadPredictJSONFile(dirname string) PredictInfo2 {
	filename := projectsDir + "/" + dirname + "/predict2.json"
	j := PredictInfo2{}
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		logger.Info.Println(err)
		return j
	}
	err = json.Unmarshal(data, &j)
	if err != nil {
		return j
	}
	return j
}
