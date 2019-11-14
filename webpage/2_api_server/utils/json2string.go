package util

import (
	"encoding/json"

	"github.com/pkg/errors"
)

//IntArray2String int数组转字符串
func IntArray2String(arr *[]int) (string, error) {
	bs, err := json.Marshal(arr)
	return string(bs), errors.WithStack(err)
}

//String2IntArray 字符串转int数组
func String2IntArray(str string) ([]int, error) {
	var arr []int
	err := json.Unmarshal([]byte(str), &arr)
	return arr, errors.WithStack(err)
}

//StrArray2String string数组转字符串
func StrArray2String(arr *[]string) (string, error) {
	bs, err := json.Marshal(arr)
	return string(bs), errors.WithStack(err)
}

//String2StrArray 字符串转string数组
func String2StrArray(str string) ([]string, error) {
	var arr []string
	err := json.Unmarshal([]byte(str), &arr)
	return arr, errors.WithStack(err)
}
