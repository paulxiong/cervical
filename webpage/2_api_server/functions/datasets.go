package function

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"os"
	"strings"

	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	m "github.com/paulxiong/cervical/webpage/2_api_server/models"
	"github.com/toolkits/file"
)

/*
CSV和JPG存放路径
lambdatest/
├── csv
│   └── 20190523
│       └── TCT
│           └── 1807178
│               └── IMG001x008.csv
└── img
    └── 20190523
        └── 1807178
            ├── Images
            │   └── IMG001x001.JPG
            └── Thumbs


要生成的目录结构
scratch/
└── vqoM7xEt
    ├── 30.log
    ├── cells
    │   ├── crop
    │   ├── crop_masked
    │   ├── mask_npy
    │   │   ├── 17P0603=1903779=P=IMG032x009.JPG_563_1885_663_1985.npy
    │   │   ├── 17P0603=1903779=P=IMG032x009.JPG_563_1910_663_2010.npy
    │   └── rois
    │       ├── 17P0603=1903779=N=IMG033x021.JPG_.csv
    │       └── 17P0603=1903779=P=IMG036x013.JPG_.csv
    ├── filelist.csv
    ├── info.json
    └── origin_imgs
        ├── 17P0603=1903779=N=IMG033x021.csv
        ├── 17P0603=1903779=N=IMG033x021.JPG
*/
const (
	inputDatasets = "origin_imgs"
	scratchRoot   = "scratch"
)

type typesinfo struct {
	CellType int `json:"celltype" example:"7"`   //细胞的类型
	LabelCnt int `json:"labelcnt" example:"900"` //类型的个数
}

// JobInfo 存在硬盘的JSON文件，描述每个任务的属性，info.json是初始化时候，info2.json是裁剪结束之后
type JobInfo struct {
	ID              int64       `json:"id"                example:"1"`             //任务ID
	Desc            string      `json:"desc"              example:"任务描述"`          //当前任务的文字描述
	Dir             string      `json:"dir"               example:"任务目录"`          //任务执行的目录名，调试时候很有用
	Batchids        []string    `json:"batchids"          example:"批次号"`           //批次号构成的数组
	Medicalids      []string    `json:"medicalids"        example:"病历号"`           //病历号构成的数组
	Status          int         `json:"status"            example:"4"`             //任务的状态码
	Createdatts     int64       `json:"createdatts"       example:"1568891127753"` //创建数据集的时间
	Starttimets     int64       `json:"starttimets"       example:"1568891127753"` //开始处理数据的时间
	OriginImgs      []string    `json:"origin_imgs"       example:"原始图片路径"`        // 原始图片路径构成的数组
	CellsCrop       []string    `json:"cells_crop"        example:"细胞图片"`          // 裁剪之后的细胞图路径构成的数组
	CellsCropMasked []string    `json:"cells_crop_masked" example:"细胞核图片"`         // 裁剪之后的细胞核路径构成的数组
	CellsMaskNpy    []string    `json:"cells_mask_npy"    example:"细胞核掩码"`         // 细胞核掩码，这里默认是空数组
	CellsRois       []string    `json:"cells_rois"        example:"细胞核在FOV的坐标"`    // 细胞核坐标，这里默认是空数组
	BatchCnt        int         `json:"batchcnt"          example:"1"`             //总的批次数, 初始化和结束时候的值可能不一样
	MedicalCnt      int         `json:"medicalcnt"        example:"2"`             //总的病例数，初始化和结束时候的值可能不一样
	FovCnt          int         `json:"fovcnt"            example:"100"`           //总的图片数，初始化和结束时候的值可能不一样
	FovnCnt         int         `json:"fovncnt"           example:"10"`            //FOV N的个数，初始化和结束时候的值可能不一样
	FovpCnt         int         `json:"fovpcnt"           example:"90"`            //FOV P的个数，初始化和结束时候的值可能不一样
	LabelnCnt       int         `json:"labelncnt"         example:"100"`           //n 的标注次数，初始化时候表示标注的次数，结束时候表示细胞的个数
	LabelpCnt       int         `json:"labelpcnt"         example:"900"`           //p 的标注次数，初始化时候表示标注的次数，结束时候表示细胞的个数
	LabelCnt        int         `json:"labelcnt"          example:"1000"`          //总的标注次数，初始化时候表示标注的次数，结束时候表示细胞的个数
	Types           []typesinfo `json:"types"`                                     //各个type标注次数，初始化时候表示标注的次数，结束时候表示细胞的个数
}

func writeJSON(cfg string, jsonByte []byte) {
	if cfg == "" {
		logger.Info.Println("please specify json file")
	}
	_, err := file.WriteBytes(cfg, jsonByte)
	if err != nil {
		logger.Info.Println("write config file:", cfg, "fail:", err)
	}
}

// GetInfoJSONPath 拿出info.json的路径, isDone=1表示拿出裁剪完之后的细胞统计信息，isDone=0表示拿出裁剪之前的标注信息
func GetInfoJSONPath(d m.Dataset, isDone int64) string {
	infopath := scratchRoot + "/" + d.Dir + "/"
	if isDone == 0 {
		infopath = infopath + "info.json"
	} else {
		infopath = infopath + "info2.json"
	}
	return infopath
}

// GetLogContent 读取任务的日志文件
func GetLogContent(d m.Dataset, _type string) string {
	logpath := ""
	if _type == "c" {
		logpath = scratchRoot + "/" + d.Dir + "/" + fmt.Sprintf("%d.log", d.Id)
	} else {
		logpath = scratchRoot + "/" + d.Dir + "/" + "log"
	}
	data, err := ioutil.ReadFile(logpath)
	if err != nil {
		return string(data)
	}
	return string(data)
}

// GetModelInfo 读取生成模型的日志文件
func GetModelInfo(d m.Dataset, _type string) []m.Model {
	logpath := ""
	minfo := []m.Model{}
	modeltype := 1 // 0未知 1UNET 2GAN 3SVM
	if _type == "s" {
		logpath = scratchRoot + "/" + d.Dir + "/svm_model.txt"
		modeltype = 3
	} else {
		logpath = scratchRoot + "/" + d.Dir + "/gan_model.txt"
		modeltype = 2
	}

	f, err := os.Open(logpath)
	if err != nil {
		return minfo
	}
	buf := bufio.NewReader(f)
	for {
		line, err := buf.ReadString('\n')
		line = strings.TrimSpace(line)
		if err != nil {
			if err == io.EOF {
				return minfo
			}
			return minfo
		}
		_minfo := m.Model{}
		if err2 := json.Unmarshal([]byte(line), &_minfo); err2 == nil {
			_minfo.Type = modeltype
			_minfo.DId = d.Id
			minfo = append(minfo, _minfo)
		} else {
			logger.Info.Println(err2)
		}
	}
}

// NewJSONFile 创建任务的时候把任务的部分信息存到JSON文件
func NewJSONFile(d m.Dataset, batchids []string, medicalids []string, cntn int, cntp int) {
	c := JobInfo{}
	c.ID = d.Id
	c.Desc = d.Desc
	c.Status = d.Status
	c.Dir = d.Dir
	c.Batchids = batchids
	c.Medicalids = medicalids
	c.FovnCnt = cntn
	c.FovpCnt = cntp
	data, err := json.MarshalIndent(c, "", " ") //这里返回的data值，类型是[]byte
	if err != nil {
		log.Println("ERROR:", err)
	}

	info := scratchRoot + "/" + d.Dir + "/info.json"
	writeJSON(info, data)
}

// CreateDataset 按照页面选择的 批次 病例 图片，生产filelist.csv
func CreateDataset(imgs []m.ImagesByMedicalId, dirname string) (n int, p int) {
	err := os.MkdirAll(scratchRoot+"/"+dirname, os.ModePerm) //创建多级目录
	if err != nil {
		logger.Info.Println(err)
	}

	filelist := scratchRoot + "/" + dirname + "/filelist.csv"
	fd, err1 := os.OpenFile(filelist, os.O_RDWR|os.O_CREATE|os.O_APPEND, 0644)
	if err1 != nil {
		logger.Info.Println(filelist, err1)
	}

	var cntn int = 0
	var cntp int = 0
	for _, v := range imgs {
		imgpath := v.Batchid + "/" + v.Medicalid + "/Images/" + v.Imgpath
		csvpath := v.Csvpath
		toimgname := ""
		if v.P1N0 == 0 {
			toimgname = v.Batchid + "." + v.Medicalid + ".N." + v.Imgpath
			cntn = cntn + 1
		} else {
			toimgname = v.Batchid + "." + v.Medicalid + ".P." + v.Imgpath
			cntp = cntp + 1
		}
		s := imgpath + " " + csvpath + " " + toimgname
		fd.WriteString(s + "\n")
	}
	fd.Close()
	return cntn, cntp
}

// LoadJSONFile 加载json文件内容成struct
func LoadJSONFile(filename string) JobInfo {
	j := JobInfo{}
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
