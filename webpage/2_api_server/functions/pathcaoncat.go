package function

import "fmt"

// Imgpath 返回原图的相对路径
func Imgpath(batchid string, medicalid string, img string) string {
	return fmt.Sprintf("img/%s/%s/Images/%s", batchid, medicalid, img)
}
