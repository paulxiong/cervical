package controllers

import (
	"fmt"
	"image"

	// 支持的格式
	_ "image/jpeg"
	_ "image/png"
	"io"
	"net/http"
	"os"
	"path"
	"strconv"

	"github.com/gin-gonic/gin"

	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
	f "github.com/paulxiong/cervical/webpage/2_api_server/functions"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	models "github.com/paulxiong/cervical/webpage/2_api_server/models"
	u "github.com/paulxiong/cervical/webpage/2_api_server/utils"
)

// FileDownload 细胞集合的zip下载
// @Summary 细胞集合的zip下载
// @Description 细胞集合的zip下载
// @tags API1 文件（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param id query string false "id, default 0, 数据集的ID"
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/zipdownload [get]
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

// UploadsHandler 上传多个文件
// @Summary 上传多个文件
// @Description 上传多个文件
// @tags API1 文件（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param id query string false "id, default 0, 数据集的ID"
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/uploads [post]
func UploadsHandler(c *gin.Context) {
	//获取解析后表单
	form, _ := c.MultipartForm()
	//这里是多文件上传 在之前单文件upload上传的基础上加 [] 变成upload[] 类似文件数组的意思
	files := form.File["upload[]"]
	//循环存文件到服务器本地
	logger.Info.Println(files)
	for _, file := range files {
		c.SaveUploadedFile(file, file.Filename)
	}
	c.String(http.StatusOK, fmt.Sprintf("%d 个文件被上传成功!", len(files)))
}

// UploadDatasetHandler 上传单个文件,并记录到数据集
// @Summary 上传单个文件,并记录到数据集
// @Description 上传单个文件,并记录到数据集
// @tags API1 文件（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/upload [post]
func UploadDatasetHandler(c *gin.Context) {
	_mid := c.DefaultPostForm("mid", "")
	_bid := c.DefaultPostForm("bid", "")
	if len(_mid) < 1 || len(_bid) < 1 {
		ResString(c, "invalied medicalid or batchid")
		return
	}

	file, header, err := c.Request.FormFile("file")
	if err != nil {
		ResString(c, fmt.Sprintf("file err : %s", err.Error()))
		return
	}

	// 新建批次病例目录
	dirpath := f.NewMedicalDir(_bid, _mid)
	f.NewDir(dirpath)
	filename := u.URLEncodeFileName(header.Filename)
	filepath := path.Join(dirpath, header.Filename)

	out, err := os.Create(filepath)
	if err != nil {
		logger.Info.Println(err)
		ResString(c, fmt.Sprintf("Create %s failed, %s", filepath, err.Error()))
		return
	}
	defer out.Close()
	_, err = io.Copy(out, file)
	if err != nil {
		logger.Info.Println(err)
		ResString(c, fmt.Sprintf("Create %s failed, %s", filepath, err.Error()))
		return
	}

	imgfile, err1 := os.Open(filepath)
	if err1 != nil {
		ResString(c, fmt.Sprintf("open image %s failed, %s", filepath, err1.Error()))
		return
	}
	defer imgfile.Close()
	imginfo, _, err2 := image.DecodeConfig(imgfile)
	if err2 != nil {
		ResString(c, fmt.Sprintf("Decode image %s failed, %s", filepath, err2.Error()))
		return
	}

	_u, _ := models.GetUserFromContext(c)

	// 保存图片信息到数据库
	img := &models.Image{
		ID:        0,
		Csvpath:   "",
		Imgpath:   filename,
		W:         imginfo.Width,
		H:         imginfo.Height,
		Batchid:   _bid,
		Medicalid: _mid,
		Status:    1,
		Type:      1,
		CreatedBy: _u.ID,
	}
	img.CreateImage()

	ResString(c, "ok")
	return
}
