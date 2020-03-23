package controllers

import (
	"net/http"
	"path"
	"path/filepath"
	"strings"
	"time"

	"github.com/gin-gonic/gin"

	f "github.com/paulxiong/cervical/webpage/2_api_server/functions"
	m "github.com/paulxiong/cervical/webpage/2_api_server/models"
	u "github.com/paulxiong/cervical/webpage/2_api_server/utils"
)

// checkReferer 防盗链功能
func checkReferer(c *gin.Context, rootURLpath string) {
	if m.SystemCfg == nil || m.SystemCfg.RefererEn != 2 {
		return
	}

	referers := m.SystemCfg.Referers2
	ref := c.Request.Referer()
	// 非法请求
	if ref == "" || len(referers) < 1 {
		c.Request.URL.Path = m.SystemCfg.Referer401URL
		return
	}
	//检查referer是否合法, 合法的不做任何操作直接返回
	for _, _ref := range referers {
		if strings.HasPrefix(ref, _ref) {
			// 图片不存在
			ret, err := f.PathExists(string([]byte(c.Request.URL.Path)[len(rootURLpath)+1:]))
			if ret == false || err != nil {
				c.Request.URL.Path = m.SystemCfg.Referer404URL
			}
			return
		}
	}

	c.Request.URL.Path = m.SystemCfg.Referer401URL
	return
}

// ImageAPI 图片服务器API
// @Summary 图片服务器API（图片在线缩放、旋转、裁剪等）
// @Description 图片URL，详细参数请参考 https://github.com/pierrre/imageserver
// @tags API1 文件（不需要认证）
// @Accept  json
// @Produce json
// @Param width query string false "width, 图片宽度，不传值表示原始尺寸，只传width不传height表示按照width等比例缩放"
// @Param height query string false "height, 图片高度，不传值表示原始尺寸，只传height不传width表示按照height等比例缩放"
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Router /imgs [get]
func ImageAPI(c *gin.Context) {
	imgexpires := 1
	if m.SystemCfg != nil && m.SystemCfg.ImgExpires > 0 {
		imgexpires = m.SystemCfg.ImgExpires
	}

	cfg := f.ImageServerSettings{
		MaxWidth:     4096,
		MaxHeight:    4096,
		ImgDir:       ".",
		Cachedir:     "cache",
		MemCacheSize: int64(128 * (1 << 20)), //128M
		HTTPExpires:  time.Duration(imgexpires) * time.Hour,
	}

	// 带特殊字符的文件要对文件名做特殊编码
	// 上传时候文件名是: IMG029x029汉子  @#%\.JPG
	// 存服务器文件名是: IMG029x029%E6%B1%89%E5%AD%90%20%20%40%23%25.JPG
	// 存服务器数据库文件名是: IMG029x029%E6%B1%89%E5%AD%90%20%20%40%23%25.JPG
	// 网页访问图片地址栏输入URL是: http://xx.com/xx/IMG029x029%E6%B1%89%E5%AD%90%20%20%40%23%25.JPG
	// 网页访问图片输入URL敲完回车之后地址栏是: http://xx.com/xx/IMG029x029汉子%20%20%40%23%25.JPG
	// 请求到当前函数，c.Request.URL.Path是：/xx/IMG029x029汉子  @#%\.JPG
	// 服务器上不存在文件名为【IMG029x029汉子  @#%\.JPG】的文件
	// 所以要做encode, 让文件名字变成IMG029x029%E6%B1%89%E5%AD%90%20%20%40%23%25.JPG
	// 文件名不带特殊字符没有影响
	URL := c.Request.URL.Path
	pathName, fileName := filepath.Split(URL)
	c.Request.URL.Path = path.Join(pathName, u.URLEncodeFileName(fileName))

	checkReferer(c, "/imgs")
	h := http.StripPrefix("/imgs", f.ImageServer(&cfg))
	h.ServeHTTP(c.Writer, c.Request)
}
