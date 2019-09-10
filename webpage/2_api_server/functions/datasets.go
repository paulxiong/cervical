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
└── 156256766279800000001
    ├── input_datasets
    │   └── 1807237_P
    ├── input_datasets_denoising
    │   └── 1807237_P_20190523_1807237_IMG005x022
    │       └── images
    ├── middle_mask
    │   └── predict
    │       └── test
    │           └── colour
    │               └── 1807237_P_20190523_1807237_IMG005x022
    └── output_datasets
        ├── 1807237_N_20190523_1807237_IMG001x014.JPG_output
        │   ├── crops
        │   └── preview
*/
const (
	input_datasets           = "input_datasets"
	input_datasets_denoising = "input_datasets_denoising"
	middle_mask              = "middle_mask"
	output_datasets          = "output_datasets"
	image_root               = ""
	csv_root                 = ""
	scratch_root             = "scratch"
)

type JobInfo struct {
	Id                           int64    `json:"id"`
	Desc                         string   `json:"desc"`
	Dir                          string   `json:"dir"`
	Batchids                     []string `json:"batchids"`
	Medicalids                   []string `json:"medicalids"`
	Status                       int      `json:"status"`
	Cntn                         int      `json:"cntn"`
	Cntp                         int      `json:"cntp"`
	CellCntn                     int      `json:"cellcntn"`
	CellCntp                     int      `json:"cellcntp"`
	Createdatts                  int64    `json:"createdatts"`
	Starttimets                  int64    `json:"starttimets"`
	Input_datasets_img           []string `json:"input_datasets_img"`
	Input_datasets_csv           []string `json:"input_datasets_csv"`
	Input_datasets_denoising     []string `json:"input_datasets_denoising"`
	Middle_mask                  []string `json:"middle_mask"`
	Output_datasets_crop         []string `json:"output_datasets_crop"`
	Output_datasets_crop_n       []string `json:"output_datasets_crop_n"`
	Output_datasets_crop_p       []string `json:"output_datasets_crop_p"`
	Output_datasets_npy          []string `json:"output_datasets_npy"`
	Output_datasets_slide_npy    []string `json:"output_datasets_slide_npy"`
	Output_datasets_crop_preview []string `json:"output_datasets_crop_preview"`
}

func WriteJson(cfg string, jsonByte []byte) {
	if cfg == "" {
		logger.Info.Println("please specify json file")
	}
	_, err := file.WriteBytes(cfg, jsonByte)
	if err != nil {
		logger.Info.Println("write config file:", cfg, "fail:", err)
	}
}

func GetInfoJsonPath(d m.Dataset) string {
	infopath := scratch_root + "/" + d.Dir + "/info.json"
	return infopath
}

func GetLogContent(d m.Dataset, _type string) string {
	logpath := ""
	if _type == "c" {
		logpath = scratch_root + "/" + d.Dir + "/" + fmt.Sprintf("%d.log", d.Id)
	} else {
		logpath = scratch_root + "/" + d.Dir + "/" + "log"
	}
	data, err := ioutil.ReadFile(logpath)
	if err != nil {
		return string(data)
	}
	return string(data)
}

func GetModelInfo(d m.Dataset, _type string) []m.Model {
	logpath := ""
	minfo := []m.Model{}
	modeltype := 1 // 0未知 1UNET 2GAN 3SVM
	if _type == "s" {
		logpath = scratch_root + "/" + d.Dir + "/svm_model.txt"
		modeltype = 3
	} else {
		logpath = scratch_root + "/" + d.Dir + "/gan_model.txt"
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

func NewJsonFile(d m.Dataset, batchids []string, medicalids []string, cntn int, cntp int) {
	c := JobInfo{}
	c.Id = d.Id
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

	info := scratch_root + "/" + d.Dir + "/info.json"
	WriteJson(info, data)
}

func CreateDataset(imgs []m.ImagesByMedicalId, dirname string) (n int, p int) {
	err := os.MkdirAll(scratch_root+"/"+dirname, os.ModePerm) //创建多级目录
	if err != nil {
		logger.Info.Println(err)
	}

	filelist := scratch_root + "/" + dirname + "/filelist.csv"
	fd, err1 := os.OpenFile(filelist, os.O_RDWR|os.O_CREATE|os.O_APPEND, 0644)
	if err1 != nil {
		logger.Info.Println(filelist, err1)
	}

	var cntn int = 0
	var cntp int = 0
	for _, v := range imgs {
		imgpath := v.Batchid + "/" + v.Medicalid + "/Images/" + v.Imgpath
		csvpath := v.Csvpath
		topath := ""
		if v.P1N0 == 0 {
			topath = dirname + "/" + input_datasets + "/" + v.Batchid + "_" + v.Medicalid + "_N/"
			cntn = cntn + 1
		} else {
			topath = dirname + "/" + input_datasets + "/" + v.Batchid + "_" + v.Medicalid + "_P/"
			cntp = cntp + 1
		}
		s := imgpath + " " + csvpath + " " + topath
		fd.WriteString(s + "\n")
	}
	fd.Close()
	return cntn, cntp
}

func LoadJsonFile(filename string) JobInfo {
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
