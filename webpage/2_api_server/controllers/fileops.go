package controllers

import (
	"fmt"
	"strconv"

	"github.com/gin-gonic/gin"

	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
	f "github.com/paulxiong/cervical/webpage/2_api_server/functions"
	models "github.com/paulxiong/cervical/webpage/2_api_server/models"
)

// FileDownload 细胞集合的zip下载
// @Summary 细胞集合的zip下载
// @Description 细胞集合的zip下载
// @tags API1 模型（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param id query string false "id, default 0, 数据集的ID"
// @Success 200 {object} controllers.listMods
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/listmodel [get]
func FileDownload(c *gin.Context) {
	idStr := c.DefaultQuery("id", "0")
	id, _ := strconv.ParseInt(idStr, 10, 64)

	// GetOneDatasetByID 通过ID查找数据集
	dt, err := models.GetOneDatasetByID(int(id))
	if len(dt.Dir) < 1 || err != nil || dt.Status != 4 {
		c.JSON(e.StatusReqOK, gin.H{
			"status": e.StatusSucceed,
			"data":   "data not found or not ready",
		})
		return
	}

	filename := fmt.Sprintf("%d_%s.zip", id, dt.Dir)

	//打包zip
	err = f.ZipCompress(dt.Dir, filename)
	if err != nil {
		c.JSON(e.StatusReqOK, gin.H{
			"status": e.StatusSucceed,
			"data":   "data not avalied",
		})
		return
	}

	//下载
	contentDisposition := fmt.Sprintf("attachment; filename=%s", filename)
	c.Writer.Header().Add("Content-Disposition", contentDisposition)
	c.Writer.Header().Add("Content-Type", "application/octet-stream")
	c.File(filename)
}
