package function

import (
	"fmt"
	"log"
	"path"
	"strconv"

	"github.com/Unknwon/goconfig"
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
	RowCount         int      `json:"rowcnt"`      // 有多少行FOV
	ColumnCount      int      `json:"colcnt"`      // 有多少列FOV
	ImageWidth       int      `json:"imgwidth"`    // 单张FOV宽
	ImageHeight      int      `json:"imgheight"`   // 单张FOV高
	SceneWidth       int      `json:"scenewidth"`  // FOV拼成全图的宽
	SceneHeight      int      `json:"sceneheight"` // FOV拼成全图的高
	ImageFileNameExt string   `json:"imgext"`      // FOV文件的后缀
	SlideID          string   `json:"slideid"`     // 玻片ID
	Result           string   `json:"result"`      // FOV拼成全图的缩略图
	Preview          string   `json:"preview"`     // 玻片外观照片
	Imgs             []ImgROI `json:"imgs"`        // 所有FOV坐标信息
	Boundx1          int      `json:"bx1"`         // FOV拼接成的全图的左上角X
	Boundy1          int      `json:"by1"`         // FOV拼接成的全图的左上角y
	Boundx2          int      `json:"bx2"`         // FOV拼接成的全图的右下角X
	Boundy2          int      `json:"by2"`         // FOV拼接成的全图的右下角y
}

// ParseScanTXT 解析Scan.txt
func ParseScanTXT(scantxt string) (_st Scantxt, _err error) {
	var st Scantxt
	cfg, err := goconfig.LoadConfigFile(scantxt)
	if err != nil {
		log.Printf("load config failed")
		return st, err
	}
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

	cnt := 0
	for i := 1; i <= st.RowCount; i++ {
		for j := 1; j <= st.ColumnCount; j++ {
			row := fmt.Sprintf("Row%3.3dx%3.3d", i, j)
			_row, _ := getConfigIntValue(cfg, "Images", row)
			col := fmt.Sprintf("Col%3.3dx%3.3d", i, j)
			_col, _ := getConfigIntValue(cfg, "Images", col)

			if i == 1 && j == 1 {
				st.Boundx1 = _col
				st.Boundy1 = _row
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
