package function

import "fmt"

// Imgpath 返回原图的相对路径
func Imgpath(batchid string, medicalid string, img string) string {
	return fmt.Sprintf("img/%s/%s/Images/%s", batchid, medicalid, img)
}

// NewMedicalDir 返回新上传图片的保存目录
func NewMedicalDir(batchid string, medicalid string) string {
	return fmt.Sprintf("scratch/img/%s/%s/Images/", batchid, medicalid)
}
