package function

import (
	"fmt"
	"os"
	"path"
	"path/filepath"
	"strings"

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

// ReviewImgPath 获得存放FOV的路径
func ReviewImgPath(src string) (imgpth string) {
	// scratch/img/b157521600000025/m157527753898025/Images/076ca419a04b446d9e88d8fe03a85d69
	newimgpath := strings.Replace(src, "img", "review", 1)
	newimgdir, _ := filepath.Split(newimgpath)
	ret, err := PathExists(newimgdir)
	if ret != true || err != nil {
		NewDir(newimgdir)
	}
	return newimgpath
}

// ReviewCellPath 获得存放细胞的路径
func ReviewCellPath(src string, fovpath string) (cellpath string) {
	// projects/ek1roy1R/resize_predict/100/b157521600000025.m157527753898025.6005.076ca419a04b446d9e88d8fe03a85d69_1_100_0_2_2348_772_2448_872_100.png
	_, fileName := filepath.Split(src)
	fovdir, _ := filepath.Split(fovpath)
	celldir := strings.Replace(fovdir, "Images", "Cells", 1)
	ret, err := PathExists(celldir)
	if ret != true || err != nil {
		NewDir(celldir)
	}
	_cellpath := path.Join(celldir, fileName)
	return _cellpath
}
