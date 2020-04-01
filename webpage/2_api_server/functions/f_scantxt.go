package function

import (
	"encoding/json"
	"fmt"
	"log"
	"path"
	"strconv"

	"github.com/Unknwon/goconfig"
	u "github.com/paulxiong/cervical/webpage/2_api_server/utils"
)

func getConfigStringValue(cfg *goconfig.ConfigFile, section string, key string) (val string, err error) {
	value, err := cfg.GetValue(section, key)
	if err != nil {
		log.Printf("section or value not found %s %s\n", section, key)
		return "", err
	}
	return value, nil
}

func getConfigIntValue(cfg *goconfig.ConfigFile, section string, key string) (val int, err error) {
	value, err2 := cfg.GetValue(section, key)
	if err2 != nil {
		log.Printf("section or value not found %s %s\n", section, key)
		return 0, err2
	}
	valint64, err3 := strconv.ParseInt(value, 10, 32)
	if err3 == nil {
		return int(valint64), nil
	}
	return int(valint64), nil
}

// ImgROI 单个FOV左上角坐标在整图的位置
type ImgROI struct {
	X         int    `json:"x"`
	Y         int    `json:"y"`
	Index     int    `json:"idx"` // 从左往右从上往下数的index
	ImageFile string `json:"img"`
}

// Scantxt 显微镜扫描的配置
type Scantxt struct {
	Batchid          string   `json:"batchid"`       // 批次号
	Medicalid        string   `json:"medicalid"`     // 病历号
	RowCount         int      `json:"rowcnt"`        // 有多少行FOV
	ColumnCount      int      `json:"colcnt"`        // 有多少列FOV
	ImageWidth       int      `json:"imgwidth"`      // 单张FOV宽
	ImageHeight      int      `json:"imgheight"`     // 单张FOV高
	RealImageWidth   int      `json:"realimgwidth"`  // 单张FOV宽，拼接时候要去掉重复的边
	RealImageHeight  int      `json:"realimgheight"` // 单张FOV高，拼接时候要去掉重复的边
	SceneWidth       int      `json:"scenewidth"`    // FOV拼成全图的宽
	SceneHeight      int      `json:"sceneheight"`   // FOV拼成全图的高
	ImageFileNameExt string   `json:"imgext"`        // FOV文件的后缀
	SlideID          string   `json:"slideid"`       // 玻片ID
	Result           string   `json:"result"`        // FOV拼成全图的缩略图
	Preview          string   `json:"preview"`       // 玻片外观照片
	Imgs             []ImgROI `json:"imgs"`          // 所有FOV坐标信息
	Boundx1          int      `json:"bx1"`           // FOV拼接成的全图的左上角X
	Boundy1          int      `json:"by1"`           // FOV拼接成的全图的左上角y
	Boundx2          int      `json:"bx2"`           // FOV拼接成的全图的右下角X
	Boundy2          int      `json:"by2"`           // FOV拼接成的全图的右下角y
}

// ParseScanTXT 解析Scan.txt
func ParseScanTXT(scantxt string, bid string, mid string) (_st Scantxt, _err error) {
	var st Scantxt
	cfg, err := goconfig.LoadConfigFile(scantxt)
	if err != nil {
		log.Printf("load config failed")
		return st, err
	}
	st.Batchid = bid
	st.Medicalid = mid
	st.RowCount, _ = getConfigIntValue(cfg, "General", "RowCount")
	st.ColumnCount, _ = getConfigIntValue(cfg, "General", "ColumnCount")
	st.ImageWidth, _ = getConfigIntValue(cfg, "General", "ImageWidth")
	st.ImageHeight, _ = getConfigIntValue(cfg, "General", "ImageHeight")
	st.SceneWidth, _ = getConfigIntValue(cfg, "General", "sceneWidthAfterProcessed")
	st.SceneHeight, _ = getConfigIntValue(cfg, "General", "sceneHeightAfterProcessed")
	ImageFileName, _ := getConfigStringValue(cfg, "General", "ImageFileName")
	st.ImageFileNameExt = path.Ext(ImageFileName)
	st.SlideID, _ = getConfigStringValue(cfg, "General", "SlideID")
	st.Result, _ = getConfigStringValue(cfg, "General", "Result")
	st.Preview, _ = getConfigStringValue(cfg, "General", "Preview")
	st.Imgs = make([]ImgROI, 0)

	// 前端显示要把Result图片和Preview图片的名字做URL编码
	st.Result = u.URLEncodeFileName(st.Result)
	st.Preview = u.URLEncodeFileName(st.Preview)

	cnt := 0
	_rowpre := 0
	_colpre := 0
	for i := 1; i <= st.RowCount; i++ {
		_row := 0
		for j := 1; j <= st.ColumnCount; j++ {
			row := fmt.Sprintf("Row%3.3dx%3.3d", i, j)
			_row, _ = getConfigIntValue(cfg, "Images", row)
			col := fmt.Sprintf("Col%3.3dx%3.3d", i, j)
			_col, _ := getConfigIntValue(cfg, "Images", col)

			// 每行每列不是完全水平或者垂直，所以算实际宽高只能相邻的图片之间计算
			if i == 1 && j == 1 {
				st.Boundx1 = _col
				st.Boundy1 = _row
				_rowpre = _row
				_colpre = _col
			}
			if i == 1 && j == 2 {
				st.RealImageWidth = _col - _colpre // 计算拼接大图时候的有效图片
			}
			if i == 2 && j == 1 {
				st.RealImageHeight = _row - _rowpre // 计算拼接大图时候的有效图片
			}

			if i == st.RowCount && j == st.ColumnCount {
				st.Boundx2 = _col + st.ImageWidth
				st.Boundy2 = _row + st.ImageHeight
			}

			img := fmt.Sprintf("IMG%3.3dx%3.3d%s", i, j, st.ImageFileNameExt)
			cnt = cnt + 1
			st.Imgs = append(st.Imgs, ImgROI{
				X:         _col,
				Y:         _row,
				Index:     cnt,
				ImageFile: img,
			})
		}
	}
	return st, nil
}

// NewScanTXTJSON Scan.txt信息存到JSON文件
func NewScanTXTJSON(st Scantxt, middir string) {
	data, err := json.MarshalIndent(st, "", " ") //这里返回的data值，类型是[]byte
	if err != nil {
		log.Println("ERROR:", err)
	}
	savpath := path.Join(middir, "Scan.txt.json")
	writeJSON(savpath, data)

	// 保存一个不带图片的简单版本
	st.Imgs = make([]ImgROI, 0)
	data, err = json.MarshalIndent(st, "", " ") //这里返回的data值，类型是[]byte
	if err != nil {
		log.Println("ERROR:", err)
	}
	savpath = path.Join(middir, "Scan.txt2.json")
	writeJSON(savpath, data)
}

// LoadScanTXTJSON 读取Scan.txt信息, _type 0--不带图片信息，1--全部信息
func LoadScanTXTJSON(bid string, mid string, _type int) Scantxt {
	st := Scantxt{}
	middir := GetMedicalDir(bid, mid)
	filename := path.Join(middir, "Scan.txt.json")
	if _type == 0 {
		filename = path.Join(middir, "Scan.txt2.json")
	}
	data, err := LoadJSONFile(filename)
	if err != nil {
		return st
	}
	err = json.Unmarshal(data, &st)
	return st
}
