package function

import (
	"bufio"
	"encoding/json"
	"io"
	"io/ioutil"
	"os"
	"strings"

	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	m "github.com/paulxiong/cervical/webpage/2_api_server/models"
)

// GetModelInfo 读取生成模型的日志文件
func GetModelInfo(d m.Dataset, _type string) []m.Model {
	logpath := ""
	minfo := []m.Model{}
	modeltype := 1 // 0未知 1UNET 2GAN 3SVM
	if _type == "s" {
		logpath = scratchRoot + "/" + d.Dir + "/svm_model.txt"
		modeltype = 3
	} else {
		logpath = scratchRoot + "/" + d.Dir + "/gan_model.txt"
		modeltype = 2
	}

	f, err := os.Open(logpath)
	if err != nil {
		return minfo
	}
	buf := bufio.NewReader(f)
	for {
		line, err := buf.ReadString('\n')
		line = strings.TrimSpace(line)
		if err != nil {
			if err == io.EOF {
				return minfo
			}
			return minfo
		}
		_minfo := m.Model{}
		if err2 := json.Unmarshal([]byte(line), &_minfo); err2 == nil {
			_minfo.Type = modeltype
			_minfo.PID = d.ID
			minfo = append(minfo, _minfo)
		} else {
			logger.Info(err2)
		}
	}
}

// LoadModJSONFile 加载json文件内容成struct
func LoadModJSONFile(dirname string) m.Model {
	filename := projectsDir + "/" + dirname + "/mod.json"
	j := m.Model{}
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		logger.Info(err)
		return j
	}
	err = json.Unmarshal(data, &j)
	if err != nil {
		return j
	}
	return j
}
