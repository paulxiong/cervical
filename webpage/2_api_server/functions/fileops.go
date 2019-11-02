package function

import (
	"encoding/csv"
	"os"

	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	u "github.com/paulxiong/cervical/webpage/2_api_server/utils"
)

// NewDir 递归创建目录
func NewDir(dirname string) error {
	err := os.MkdirAll(dirname, os.ModePerm)
	return err
}

// ZipCompress 创建zip压缩文件
func ZipCompress(dirname string, dest string) error {
	cellslist := datasetsDir + "/" + dirname + "/cellslist.csv"
	file, err := os.Open(cellslist)
	if err != nil {
		logger.Info.Println(err)
		return err
	}
	defer file.Close()
	reader := csv.NewReader(file)
	if reader == nil {
		logger.Info.Println("NewReader return nil, file:", file)
		return err
	}
	records, err := reader.ReadAll()
	if err != nil {
		logger.Info.Println(err)
		return err
	}

	pathindex := 9
	typeindex := 15
	colNum := len(records[0])
	for i := 0; i < colNum; i++ {
		if records[0][i] == "cellpath" {
			pathindex = i
		}
		if records[0][i] == "celltype" {
			typeindex = i
		}
	}

	filesname := make([]string, 0)
	filestype := make([]string, 0)
	recordNum := len(records)
	for i := 0; i < recordNum; i++ {
		if i == 0 {
			continue
		}
		cellpath := records[i][pathindex]
		celltype := records[i][typeindex]

		cellpath = cellpath[len("/ai/thumbor/data/loader/"):]

		filesname = append(filesname, cellpath)
		filestype = append(filestype, celltype)
	}

	err = u.ZipCompress(filesname, filestype, dest)
	return err
}
