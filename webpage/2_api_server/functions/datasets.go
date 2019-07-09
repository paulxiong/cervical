package function

import (
	"os"
	"strings"

	logger "../log"
	m "../models"
)

/*
目录结构
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

func CreateGetDataset(imgs []m.ImagesByMedicalId, dirname string) {
	err := os.MkdirAll(scratch_root+"/"+dirname, os.ModePerm) //创建多级目录
	if err != nil {
		logger.Info.Println(err)
	}

	filelist := scratch_root + "/" + dirname + "/filelist.csv"
	fd, err1 := os.OpenFile(filelist, os.O_RDWR|os.O_CREATE|os.O_APPEND, 0644)
	if err1 != nil {
		logger.Info.Println(filelist, err1)
	}
	for _, v := range imgs {
		csvname := strings.Replace(v.Imgpath, `JPG`, "csv", -1)

		imgpath := v.Batchid + "/" + v.Medicalid + "/" + v.Imgpath
		csvpath := v.Batchid + "/" + v.Medicalid + "/" + csvname
		topath := ""
		if v.P1N0 == 0 {
			topath = scratch_root + "/" + dirname + "/" + input_datasets + "/" + v.Batchid + "_" + v.Medicalid + "_N/"
		} else {
			topath = scratch_root + "/" + dirname + "/" + input_datasets + "/" + v.Batchid + "_" + v.Medicalid + "_P/"
		}

		s := imgpath + " " + csvpath + " " + topath
		fd.WriteString(s + "\n")
	}
	fd.Close()
}
