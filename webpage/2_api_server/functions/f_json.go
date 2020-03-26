package function

import (
	"io/ioutil"

	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	"github.com/toolkits/file"
)

func writeJSON(jsonfilepath string, jsonByte []byte) {
	if jsonfilepath == "" {
		logger.Info.Println("please specify json file")
	}
	_, err := file.WriteBytes(jsonfilepath, jsonByte)
	if err != nil {
		logger.Info.Println("write config file:", jsonfilepath, "fail:", err)
	}
}

// LoadJSONFile 加载json文件内容返回[]byte
func LoadJSONFile(filename string) ([]byte, error) {
	data, err := ioutil.ReadFile(filename)
	return data, err
}
