package controllers

import (
	"fmt"
	"image"
	"strconv"

	// 支持的格式
	_ "image/jpeg"
	_ "image/png"
	"io"
	"os"
	"path"

	"github.com/gin-gonic/gin"

	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
	f "github.com/paulxiong/cervical/webpage/2_api_server/functions"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	models "github.com/paulxiong/cervical/webpage/2_api_server/models"
	res "github.com/paulxiong/cervical/webpage/2_api_server/responses"
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
// @Router /api1/zipdownload [get]
func FileDownload(c *gin.Context) {
	idStr := c.DefaultQuery("id", "0")
	id, _ := strconv.ParseInt(idStr, 10, 64)

	// GetOneDatasetByID 通过ID查找数据集
	dt, err := models.GetOneDatasetByID(int(id))
	if len(dt.Dir) < 1 || err != nil || dt.Status != 4 {
		res.ResFailedStatus(c, e.Errors["DatasetsNotFound"])
		return
	}

	randomsreing := u.GetRandomStringNum(6)
	filename := fmt.Sprintf("%d_%s_%s.zip", id, dt.Dir, randomsreing)

	//打包zip
	err = f.ZipCompressDatasets(dt.Dir, filename)
	if err != nil {
		res.ResFailedStatus(c, e.Errors["ZipFailed"])
		return
	}

	filesize := f.GetFileSize(filename)

	//下载
	contentDisposition := fmt.Sprintf("attachment; filename=%s", filename)
	c.Writer.Header().Add("Content-Disposition", contentDisposition)
	c.Writer.Header().Add("Content-Type", "application/zip")
	c.Writer.Header().Add("Accept-Length", fmt.Sprintf("%d", filesize))
	c.Writer.Header().Add("Content-Length", fmt.Sprintf("%d", filesize))
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
	res.ResSucceedString(c, fmt.Sprintf("%d 个文件被上传成功!", len(files)))
}

// UploadDatasetHandler 上传单个文件,并记录到数据集
// @Summary 上传单个文件,并记录到数据集
// @Description 上传单个文件,并记录到数据集
// @tags API1 文件（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Router /api1/upload [post]
func UploadDatasetHandler(c *gin.Context) {
	_mid := c.DefaultPostForm("mid", "")
	_bid := c.DefaultPostForm("bid", "")
	if len(_mid) < 1 || len(_bid) < 1 {
		res.ResFailedStatus(c, e.Errors["MedicalBatchInvalied"])
		return
	}

	file, err := c.FormFile("file")
	if err != nil {
		res.ResFailedStatus(c, e.Errors["UploadGetFileNameFailed"])
		return
	}

	// 文件名比较URL编码前后，如果变了直接用变了的，没变就用原来的名字(可能有问题，部分病例文件带汉字或特殊字符)
	filename := u.URLEncodeFileName(file.Filename)

	// 新建批次病例目录
	dirpath := f.NewMedicalDir(_bid, _mid)
	f.NewDir(dirpath)
	filepath := path.Join(dirpath, filename)

	if err := c.SaveUploadedFile(file, filepath); err != nil {
		res.ResFailedStatus(c, e.Errors["UploadSaveFailed"])
		return
	}

	imgfile, err1 := os.Open(filepath)
	if err1 != nil {
		res.ResFailedStatus(c, e.Errors["UploadOpenFailed"])
		return
	}
	defer imgfile.Close()
	imginfo, _, err2 := image.DecodeConfig(imgfile)
	if err2 != nil {
		res.ResFailedStatus(c, e.Errors["UploadDecodeFailed"])
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

	res.ResSucceedString(c, "ok")
	return
}

// UploadImgHandler 上传一张头像图片，不记录到数据库，用作非病例相关图片上传
// @Summary 上传一张头像图片，不记录到数据库
// @Description 上传一张头像图片，不记录到数据库
// @tags API1 文件（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Router /api1/uploadimg [post]
func UploadImgHandler(c *gin.Context) {
	file, _, err := c.Request.FormFile("file")
	if err != nil {
		res.ResFailedStatus(c, e.Errors["UploadGetFileNameFailed"])
		return
	}

	filename := u.GetUUID()
	filepath, fileURL := f.HeaderImgPathURL(filename)

	out, err := os.Create(filepath)
	if err != nil {
		res.ResFailedStatus(c, e.Errors["UploadMkdirFailed"])
		return
	}
	defer out.Close()
	_, err = io.Copy(out, file)
	if err != nil {
		res.ResFailedStatus(c, e.Errors["UploadSaveFailed"])
		return
	}

	res.ResSucceedString(c, fileURL)
	return
}

// UploadDirHandler 上传病例文件夹
// @Summary 上传病例文件夹
// @Description 上传病例文件夹
// @tags API1 文件（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Router /api1/uploaddir [post]
func UploadDirHandler(c *gin.Context) {
	_mid := c.DefaultPostForm("mid", "")
	_bid := c.DefaultPostForm("bid", "")
	if len(_mid) < 1 || len(_bid) < 1 {
		res.ResFailedStatus(c, e.Errors["MedicalBatchInvalied"])
		return
	}

	file, err := c.FormFile("file")
	if err != nil {
		res.ResFailedStatus(c, e.Errors["UploadGetFileNameFailed"])
		return
	}

	// 文件名比较URL编码前后，如果变了直接用变了的，没变就用原来的名字(可能有问题，部分病例文件带汉字或特殊字符)
	filename := u.URLEncodeFileName(file.Filename)
	if filename != "Scan.txt" {
		res.ResSucceedString(c, "ok")
		return
	}

	filepath := "Scan.txt"
	if err := c.SaveUploadedFile(file, filepath); err != nil {
		res.ResFailedStatus(c, e.Errors["UploadSaveFailed"])
		return
	}
	logger.Info.Println(filename)
	st, err2 := f.ParseScanTXT(filename)
	if err2 == nil {
		logger.Info.Println(st.Boundx2, st.Boundy2)
	}

	res.ResSucceedString(c, "ok")
	return
}
