package function

import (
	"fmt"
	"os"

	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
)

const (
	inputDatasets = "origin_imgs"
	scratchRoot   = "scratch"
	datasetsDir   = "datasets"
	projectsDir   = "projects"
	csvRoot       = "csv"
)

// PathExists 判断路径对应的文件是否存在
func PathExists(path string) (bool, error) {
	_, err := os.Stat(path)
	if err == nil {
		return true, nil
	}
	if os.IsNotExist(err) {
		return false, nil
	}
	return false, err
}

// Imgpath 返回原图的相对路径
func Imgpath(batchid string, medicalid string, img string, _type int) string {
	//_type 0系统默认自带 1用户上传
	if _type == 0 {
		return fmt.Sprintf("img/%s/%s/Images/%s", batchid, medicalid, img)
	}
	return fmt.Sprintf("scratch/img/%s/%s/Images/%s", batchid, medicalid, img)
}

// NewMedicalDir 返回新上传图片的保存目录
func NewMedicalDir(batchid string, medicalid string) string {
	return fmt.Sprintf("scratch/img/%s/%s/Images/", batchid, medicalid)
}

// FileListCSVPath 返回filelist.csv的保存目录
func FileListCSVPath(dirname string) string {
	return fmt.Sprintf("%s/%s/filelist.csv", datasetsDir, dirname)
}

// csvPath 返回csv的相对路径
func csvPath(csvpath string) string {
	_csvpath := fmt.Sprintf("%s", csvpath)
	ret, err := PathExists(_csvpath)
	if ret != true || err != nil {
		logger.Info.Println("not found ", _csvpath)
		return ""
	}
	return _csvpath
}
