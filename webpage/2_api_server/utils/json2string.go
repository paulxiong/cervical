package util

import (
	"encoding/json"

	"github.com/pkg/errors"
)

//Array2String 数组转字符串
func Array2String(arr *[]int) (string, error) {
	bs, err := json.Marshal(arr)
	return string(bs), errors.WithStack(err)
}

//String2Array 字符串转数组
func String2Array(str string) ([]int, error) {
	var arr []int
	err := json.Unmarshal([]byte(str), &arr)
	return arr, errors.WithStack(err)
}
