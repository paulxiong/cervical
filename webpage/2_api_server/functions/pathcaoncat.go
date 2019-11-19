package function

import (
	"fmt"
	"os"
	"path"

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
	_csvpath := fmt.Sprintf("%s/%s", csvRoot, csvpath)
	ret, err := PathExists(_csvpath)
	if ret != true || err != nil {
		logger.Info.Println("not found ", _csvpath)
		return ""
	}
	return _csvpath
}

// HeaderImgPathURL 用户头像的相对路径
func HeaderImgPathURL(filename string) (string, string) {
	_dirpath := path.Join(scratchRoot, "static")
	_imgpath := path.Join(_dirpath, filename)
	_imgURL := path.Join("/imgs", _imgpath)
	ret, err := PathExists(_dirpath)
	if ret != true || err != nil {
		NewDir(_dirpath)
		return _dirpath, _imgURL
	}
	return _imgpath, _imgURL
}
