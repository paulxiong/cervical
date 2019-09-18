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

// JobInfo 存在硬盘的JSON文件，描述每个任务的属性
type JobInfo struct {
	ID              int64    `json:"id"`
	Desc            string   `json:"desc"`
	Dir             string   `json:"dir"`
	Batchids        []string `json:"batchids"`
	Medicalids      []string `json:"medicalids"`
	Status          int      `json:"status"`
	Cntn            int      `json:"cntn"`
	Cntp            int      `json:"cntp"`
	CellCntn        int      `json:"cellcntn"`
	CellCntp        int      `json:"cellcntp"`
	Createdatts     int64    `json:"createdatts"`
	Starttimets     int64    `json:"starttimets"`
	OriginImgs      []string `json:"origin_imgs"`       // 存放原图以及原图对应的csv
	CellsCrop       []string `json:"cells_crop"`        // 存放裁剪之后的细胞图
	CellsCropMasked []string `json:"cells_crop_masked"` // 存放裁剪之后的细胞图去掉了背景
	CellsMaskNpy    []string `json:"cells_mask_npy"`    // 存放细胞对应的掩码npy文件，npy是ndarray保存成了文件
	CellsRois       []string `json:"cells_rois"`        // 存放细胞对应的的坐标
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

// GetInfoJSONPath 拿出info.json的路径
func GetInfoJSONPath(d m.Dataset) string {
	infopath := scratchRoot + "/" + d.Dir + "/info.json"
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
	c.Cntn = cntn
	c.Cntp = cntp
	c.CellCntn = 0
	c.CellCntp = 0
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
			toimgname = v.Batchid + "AA" + v.Medicalid + "AANAA" + v.Imgpath
			cntn = cntn + 1
		} else {
			toimgname = v.Batchid + "AA" + v.Medicalid + "AAPAA" + v.Imgpath
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
