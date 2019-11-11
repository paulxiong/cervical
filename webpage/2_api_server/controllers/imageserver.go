package controllers

import (
	"net/http"
	"time"

	"github.com/gin-gonic/gin"

	f "github.com/paulxiong/cervical/webpage/2_api_server/functions"
)

// ImageAPI 图片服务器API
// @Summary 图片服务器API（图片在线缩放、旋转、裁剪等）
// @Description 图片URL，详细参数请参考 https://github.com/pierrre/imageserver
// @tags API1 文件（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param width query string false "width, 图片宽度，不传值表示原始尺寸，只传width不传height表示按照width等比例缩放"
// @Param height query string false "height, 图片高度，不传值表示原始尺寸，只传height不传width表示按照height等比例缩放"
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/imgs [get]
func ImageAPI(c *gin.Context) {
	cfg := f.ImageServerSettings{
		MaxWidth:     4096,
		MaxHeight:    4096,
		ImgDir:       "upload",
		Cachedir:     "cache",
		MemCacheSize: int64(128 * (1 << 20)), //128M
		HTTPExpires:  7 * 24 * time.Hour,
	}

	h := http.StripPrefix("/imgs", f.ImageServer(&cfg))
	h.ServeHTTP(c.Writer, c.Request)
}
