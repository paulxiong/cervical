package function

import (
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path"
	"strconv"

	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	models "github.com/paulxiong/cervical/webpage/2_api_server/models"
	"github.com/zhnxin/csvreader"
)

// JobInfo 存在硬盘的JSON文件，描述每个任务的属性，info.json是初始化时候，info2.json是裁剪结束之后
type JobInfo struct {
	ID          int64                  `json:"id"                example:"1"`              //任务ID
	Desc        string                 `json:"desc"              example:"description..."` //当前任务的文字描述
	Dir         string                 `json:"dir"               example:"dir name"`       //任务执行的目录名，调试时候很有用
	Batchids    []string               `json:"batchids"          example:"batch id"`       //批次号构成的数组
	Medicalids  []string               `json:"medicalids"        example:"medical id"`     //病历号构成的数组
	Status      int                    `json:"status"            example:"4"`              //任务的状态码
	Createdatts int64                  `json:"createdatts"       example:"1568891127753"`  //创建数据集的时间
	Starttimets int64                  `json:"starttimets"       example:"1568891127753"`  //开始处理数据的时间
	OriginImgs  []string               `json:"origin_imgs"       example:"fov path"`       //原始图片路径构成的数组
	CellsCrop   []string               `json:"cells_crop"        example:"cell path"`      //裁剪之后的细胞图路径构成的数组
	OriginTotal int                    `json:"origin_total"      example:"1"`              //原始图片的个数
	CellsTotal  int                    `json:"cells_total"       example:"1000"`           //裁剪之后的细胞图的个数
	BatchCnt    int                    `json:"batchcnt"          example:"1"`              //总的批次数, 初始化和结束时候的值可能不一样
	MedicalCnt  int                    `json:"medicalcnt"        example:"2"`              //总的病例数，初始化和结束时候的值可能不一样
	FovCnt      int                    `json:"fovcnt"            example:"100"`            //总的图片数，初始化和结束时候的值可能不一样
	FovnCnt     int                    `json:"fovncnt"           example:"10"`             //FOV N的个数，初始化和结束时候的值可能不一样
	FovpCnt     int                    `json:"fovpcnt"           example:"90"`             //FOV P的个数，初始化和结束时候的值可能不一样
	LabelnCnt   int                    `json:"labelncnt"         example:"100"`            //n 的标注次数，初始化时候表示标注的次数，结束时候表示细胞的个数
	LabelpCnt   int                    `json:"labelpcnt"         example:"900"`            //p 的标注次数，初始化时候表示标注的次数，结束时候表示细胞的个数
	LabelCnt    int                    `json:"labelcnt"          example:"1000"`           //总的标注次数，初始化时候表示标注的次数，结束时候表示细胞的个数
	Types       []models.CellTypesinfo `json:"types"`                                      //各个type标注次数，初始化时候表示标注的次数，结束时候表示细胞的个数
	ModPath     string                 `json:"modpath"           example:"mod path"`       //模型文件的路径
	models.DatasetParameter
}

// GetInfoJSONPath 拿出info.json的路径, isDone=1表示拿出裁剪完之后的细胞统计信息，isDone=0表示拿出裁剪之前的标注信息
func GetInfoJSONPath(dirname string, isDone int64) string {
	infopath := path.Join(datasetsDir, dirname)
	if isDone == 0 {
		infopath = path.Join(infopath, "info.json")
	} else {
		infopath = path.Join(infopath, "info2.json")
	}
	return infopath
}

// GetLogContent 读取任务的日志文件
func GetLogContent(dirname string, _type int) string {
	logpath := ""
	if _type == 1 { // 0 未知 1 数据集处理 2 训练 3 预测
		logpath = path.Join(datasetsDir, dirname, "log.txt")
	} else {
		logpath = path.Join(projectsDir, dirname, "log.txt")
	}
	data, err := ioutil.ReadFile(logpath)
	if err != nil {
		return string(data)
	}
	return string(data)
}

// NewJSONFile 创建任务的时候把任务的部分信息存到JSON文件
func NewJSONFile(d models.Dataset, batchids []string, medicalids []string, cntn int, cntp int) {
	c := JobInfo{}
	c.ID = d.ID
	c.Desc = d.Desc
	c.Status = d.Status
	c.Dir = d.Dir
	// 处理的参数
	c.ParameterGray = d.ParameterGray
	c.ParameterSize = d.ParameterSize
	c.ParameterType = d.ParameterType
	c.ParameterMid = d.ParameterMid
	c.ParameterCache = d.ParameterCache

	mod, _ := models.FindModelInfoByID(c.ParameterMid)
	c.ModPath = mod.Path

	c.Batchids = batchids
	c.Medicalids = medicalids
	c.FovnCnt = cntn
	c.FovpCnt = cntp
	data, err := json.MarshalIndent(c, "", " ") //这里返回的data值，类型是[]byte
	if err != nil {
		log.Println("ERROR:", err)
	}

	jsonpath := path.Join(datasetsDir, d.Dir, "info.json")
	writeJSON(jsonpath, data)
}

// CreateDataset 按照页面选择的 批次 病例 图片，生产filelist.csv
func CreateDataset(imgs []models.Image, dt *models.Dataset) (n int, p int) {
	fmt.Printf("boostx in CrateDataset %s", imgs)
	err := os.MkdirAll(path.Join(datasetsDir, dt.Dir), os.ModePerm) //创建多级目录
	if err != nil {
		logger.Info(err)
	}

	filelist := FileListCSVPath(dt.Dir)
	fd, err1 := os.OpenFile(filelist, os.O_RDWR|os.O_CREATE|os.O_APPEND, 0644)
	if err1 != nil {
		logger.Info(filelist, err1)
	}
	var cntn int = 0
	var cntp int = 0

	w := csv.NewWriter(fd)
	w.Write([]string{"imgid", "imgpath", "csvpath", "p1n0", "batchid", "medicalid", "imgname"})
	w.Flush()

	for _, v := range imgs {
		imgpath := Imgpath(v.Batchid, v.Medicalid, v.Imgpath, v.Type)
		csvpath := csvPath(v.Csvpath)
		w.Write([]string{fmt.Sprintf("%d", v.ID), imgpath, csvpath, strconv.Itoa(0), v.Batchid, v.Medicalid, v.Imgpath})
		w.Flush()
	}
	fd.Close()
	return cntn, cntp
}

type imginfo struct {
	Imgid     int64
	Imgpath   string
	Csvpath   string
	P1n0      int
	Batchid   string
	Medicalid string
	Imgname   string
}

// GetDatasetFileList 获得数据集的所有图片的ID
func GetDatasetFileList(dt *models.Dataset) (ids []int64) {
	csvpath := FileListCSVPath(dt.Dir)
	_ids := make([]int64, 0)
	infos := []imginfo{}
	_ = csvreader.New().UnMarshalFile(csvpath, &infos)
	for _, v := range infos {
		_ids = append(_ids, v.Imgid)
	}
	return _ids
}

// LoadJSONFileInfoJSON 加载json文件内容成struct
func LoadJSONFileInfoJSON(filename string) JobInfo {
	j := JobInfo{}
	data, err := LoadJSONFile(filename)
	if err != nil {
		return j
	}
	err = json.Unmarshal(data, &j)
	if err != nil {
		return j
	}
	return j
}
