package util

import (
	"net/url"
	"strings"
)

// URLEncodeFileName 把传入的文件名做URL编码，防止页面无显示
func URLEncodeFileName(filename string) (newfilename string) {
	if len(filename) < 1 {
		return filename
	}
	v := url.Values{}
	v.Add("target", filename)
	body := v.Encode()
	newname := body[len("target="):len(body)]
	newname = strings.Replace(newname, "+", "%20", -1)
	return newname
}
