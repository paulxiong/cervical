package controllers

import (
	"strconv"
	"strings"

	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
	f "github.com/paulxiong/cervical/webpage/2_api_server/functions"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	m "github.com/paulxiong/cervical/webpage/2_api_server/models"
	u "github.com/paulxiong/cervical/webpage/2_api_server/utils"

	"github.com/gin-gonic/gin"
)

// Category2 标注信息
type Category2 struct {
	ID     int    `json:"id"`     //标注对应的id
	Cnt    int64  `json:"cnt"`    //标注次数
	CntImg int64  `json:"cntimg"` //该标注分类下的图片数量
	Name   string `json:"name"`   //名字
	P1N0   int    `json:"p1n0"`   //是阴性还是阳性
	Other  string `json:"other"`  //描述
}

// Statistics 所有数据集的统计数据
type Statistics struct {
	TotalImage     int64 `json:"totalimg"`
	TotalImageNorm int64 `json:"totalimgnorm"`
	TotalLabel     int64 `json:"totallabel"`
	TotalLabelP    int64 `json:"totallabelp"`
	TotalLabelN    int64 `json:"totallabeln"`
	TotalCategory  int64 `json:"totalcategory"`

	CategoryLists []Category2 `json:"categorylists"`
}

// AllInfo 获得所有图片及标注的统计信息
// @Description 获得所有图片及标注的统计信息
// @tags API1 数据/项目（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/dtinfo [get]
func AllInfo(c *gin.Context) {
	st := Statistics{}
	st.CategoryLists = make([]Category2, 0)

	total1, _, _ := m.ListImage(1, 0)
	st.TotalImage = total1

	total, cs, _ := m.ListCategory(100, 0)
	st.TotalCategory = total

	total2, _ := m.ListImageCntByLabelType(1)
	st.TotalImageNorm = total2

	totalN, _ := m.ListLabelCountByPN(0)
	totalP, _ := m.ListLabelCountByPN(1)

	for _, v := range cs {
		_total, _, _ := m.ListLabelByType(1, 0, int(v.Id))
		_total2, _ := m.ListImageCntByLabelType(int(v.Id))
		st.CategoryLists = append(st.CategoryLists, Category2{
			Name:   v.Name,
			Other:  v.Other,
			P1N0:   v.P1N0,
			Cnt:    _total,
			ID:     int(v.Id),
			CntImg: _total2,
		})
	}

	total2, ls2, err2 := m.ListLabel(1, 0)
	logger.Info.Println(total2, ls2, err2)
	st.TotalLabel = total2
	st.TotalLabelP = totalP
	st.TotalLabelN = totalN

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   st,
	})
	return
}

// BatchInfo 批次信息
type BatchInfo struct {
	Total  int      `json:"total"`
	Batchs []string `json:"batchs"`
}

// GetBatchInfo 获得所有批次信息
// @Description 获得所有批次信息
// @tags API1 数据/项目（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/batchinfo [get]
func GetBatchInfo(c *gin.Context) {
	total, bs, err := m.ListBatch(100, 0)
	if err != nil {
		c.JSON(e.StatusReqOK, gin.H{
			"status": e.StatusSucceed,
			"data":   "",
		})
		return
	}
	bi := BatchInfo{
		Total:  int(total),
		Batchs: bs,
	}
	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   bi,
	})
	return
}

// MedicalIDInfo 病例信息
type MedicalIDInfo struct {
	Total      int      `json:"total"`
	MedicalIds []string `json:"medicalids"`
}

// GetMedicalIDInfo 获得所有病例信息
// @Description 获得所有病例信息
// @tags API1 数据/项目（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/medicalidinfo [get]
func GetMedicalIDInfo(c *gin.Context) {
	var total int
	allms := make([]string, 0)
	batchid := c.DefaultQuery("batchid", "")
	batchids := strings.Split(batchid, "|")
	for _, v := range batchids {
		totalms, _ms, _ := m.ListMedicalIdByBatchId(100, 0, v)
		total = total + int(totalms)
		for _, mdicalid := range _ms {
			allms = append(allms, mdicalid)
		}
	}
	mi := MedicalIDInfo{
		Total:      int(total),
		MedicalIds: allms,
	}
	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   mi,
	})
	return
}

// CategoryInfo 细胞类型信息
type CategoryInfo struct {
	ID      int    `json:"id"`
	Name    string `json:"name"`
	Num     int    `json:"num"`
	Checked bool   `json:"checked"`
}

// CategorysInfo 所有细胞类型信息
type CategorysInfo struct {
	Total     int            `json:"total"`
	Categorys []CategoryInfo `json:"categorys"`
}

// GetCategoryInfo 获得细胞分类信息
// @Description 获得细胞分类信息
// @tags API1 数据/项目（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/categoryinfo [get]
func GetCategoryInfo(c *gin.Context) {
	var ci CategorysInfo
	ci.Categorys = make([]CategoryInfo, 0)
	total, cs, _ := m.ListCategory(100, 0)
	ci.Total = int(total)
	for _, v := range cs {
		ci.Categorys = append(ci.Categorys, CategoryInfo{
			ID:      int(v.Id),
			Name:    v.Name,
			Num:     0,
			Checked: false,
		})
	}
	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   ci,
	})
	return
}

type wantedCategorys struct {
	ID  int `json:"id"`
	Num int `json:"num"`
}

type wanted struct {
	Categorys  []wantedCategorys `json:"categorys"`
	Medicalids []string          `json:"medicalids"`
	Batchs     []string          `json:"batchs"`
}

type wanted2 struct {
	Images []string `json:"images"`
}

// GetImgListOfWanted 获得所选批/次病/细胞类型的图片
// @Description 获得所选批/次病/细胞类型的图片
// @tags API1 数据/项目（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/imglistsofwanted [get]
func GetImgListOfWanted(c *gin.Context) {
	images := wanted2{}
	images.Images = make([]string, 0)
	w := wanted{}
	err := c.BindJSON(&w)
	if err != nil {
		logger.Info.Println(err)
	}

	for _, v := range w.Categorys {
		logger.Info.Println(v.Num, 0, w.Batchs, w.Medicalids, v.ID)
		ws, err2 := m.ListWantedImages(v.Num, 0, w.Batchs, w.Medicalids, v.ID)
		logger.Info.Println(ws, err2)

		for _, v2 := range ws {
			images.Images = append(images.Images, v2)
		}
	}

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   images,
	})

	return
}

type imageslists struct {
	Images []m.Image `json:"images"`
}

// GetImgListOneByOne 按数据库存储的顺序依次得到图片的信息
// @Description 按数据库存储的顺序依次得到图片的信息
// @tags API1 数据/项目（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/imglistsonebyone [get]
func GetImgListOneByOne(c *gin.Context) {
	limitStr := c.DefaultQuery("limit", "1")
	skipStr := c.DefaultQuery("skip", "0")
	limit, _ := strconv.ParseInt(limitStr, 10, 64)
	skip, _ := strconv.ParseInt(skipStr, 10, 64)

	images := imageslists{}
	images.Images = make([]m.Image, 0)

	total, imgs, _ := m.ListImage(int(limit), int(skip))

	for _, v := range imgs {
		images.Images = append(images.Images, v)
	}

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   images,
		"total":  total,
	})

	return
}

// Labelslists 标注信息
type Labelslists struct {
	Labels []m.Label `json:"labels"`
	W      int       `json:"imgw"`
	H      int       `json:"imgh"`
}

// GetLabelByImageID 通过图片的ID获得对应的所有标注信息
// @Description 通过图片的ID获得对应的所有标注信息
// @tags API1 数据/项目（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/imglistsonebyone [get]
func GetLabelByImageID(c *gin.Context) {
	limitStr := c.DefaultQuery("limit", "1")
	skipStr := c.DefaultQuery("skip", "0")
	imgidStr := c.DefaultQuery("imgid", "1")
	imgid, _ := strconv.ParseInt(imgidStr, 10, 64)
	limit, _ := strconv.ParseInt(limitStr, 10, 64)
	skip, _ := strconv.ParseInt(skipStr, 10, 64)

	labels := Labelslists{}
	labels.Labels = make([]m.Label, 0)

	img, err := m.GetImageById(imgid)
	if err == nil {
		labels.W = img.W
		labels.H = img.H
	}

	total, _labels, _ := m.ListLabelByImageId(int(limit), int(skip), int(imgid))
	for _, v := range _labels {
		_c, _ := m.GetCategoryById(v.Type)
		v.TypeOut = _c.Name
		labels.Labels = append(labels.Labels, v)
	}

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   labels,
		"total":  total,
	})

	return
}

// imagesNPTypeByMedicalID 选中的批次、病例的传入参数
type imagesNPTypeByMedicalID struct {
	Batchids   []string `json:"batchids"`
	Medicalids []string `json:"medicalids"`
	Desc       string   `json:"desc"`
	Type       int      `json:"type"`
}
type imagesNPCount struct {
	CountN int `json:"countn"`
	CountP int `json:"countp"`
}

// GetImagesNPTypeByMedicalID 通过所选中的批次/病例/图片, 返回N/P图片的个数统计
// @Description 通过所选中的批次/病例/图片, 返回N/P图片的个数统计
// @tags API1 数据/项目（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/getimgnptypebymids [post]
func GetImagesNPTypeByMedicalID(c *gin.Context) {
	cnt := imagesNPCount{}
	w := imagesNPTypeByMedicalID{}
	err := c.BindJSON(&w)
	logger.Info.Println(err, w.Medicalids)

	totaln, totalp, _ := m.ListImagesNPTypeByMedicalId(w.Medicalids)
	cnt.CountN = totaln
	cnt.CountP = totalp
	logger.Info.Println(totaln, totalp)
	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   cnt,
	})
	return
}

// CreateDataset 新建数据/项目
// @Description 新建数据/项目
// @tags API1 数据/项目（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/createdataset [post]
func CreateDataset(c *gin.Context) {
	w := imagesNPTypeByMedicalID{}
	err := c.BindJSON(&w)
	if err != nil {
		logger.Info.Println(err)
	}

	// usr, _ := m.GetUserFromContext(c)

	dt := m.Dataset{}
	dt.Id = 0
	dt.CreatedBy = 1
	dt.Desc = w.Desc
	dt.Dir = u.GetRandomSalt()
	dt.Status = 0
	dt.Type = w.Type
	dt.CreateDatasets()

	imgs := make([]m.ImagesByMedicalId, 0)
	for _, v := range w.Medicalids {
		_imgs, _ := m.ListImagesByMedicalId(v)
		for _, v2 := range _imgs {
			imgs = append(imgs, v2)
		}
	}
	cntn, cntp := f.CreateDataset(imgs, dt.Dir)
	dt.Status = 1
	m.UpdateDatasetsStatus(dt.Id, dt.Status)

	f.NewJSONFile(dt, w.Batchids, w.Medicalids, cntn, cntp)

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   dt.Id,
	})

	return
}

type jobResult struct {
	ID      int64 `json:"id"`
	Type    int   `json:"type"`
	Status  int   `json:"status"`
	Percent int   `json:"percent"` // 完成百分比
}

// GetOneJob python端请求一个任务（数据处理/训练/预测），python端会指定请求任务的状态和类型
// @Description python端请求一个任务（数据处理/训练/预测），python端会指定请求任务的状态和类型
// @tags API1 任务（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 63}"
// @Router /api1/job [post]
func GetOneJob(c *gin.Context) {
	w := jobResult{}
	err := c.BindJSON(&w)

	dt, err := m.GetOneDatasetsToProcess(w.Status, w.Type)
	if err != nil {
		c.JSON(e.StatusReqOK, gin.H{
			"status": e.StatusSucceed,
			"data":   dt,
		})
		return
	}
	if w.Status == 1 {
		m.UpdateDatasetsStatus(dt.Id, 2)
	} else if w.Status == 4 {
		m.UpdateDatasetsStatus(dt.Id, 6)
	}

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   dt,
	})
	return
}

// SetJobResult python端更新任务状态/进度（数据处理/训练/预测）
// @Description python端更新任务状态/进度（数据处理/训练/预测）
// @tags API1 任务（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/jobresult [post]
func SetJobResult(c *gin.Context) {
	w := jobResult{}
	err := c.BindJSON(&w)
	if err != nil {
		logger.Info.Println(err)
		c.JSON(e.StatusReqOK, gin.H{
			"status": e.StatusSucceed,
		})
		return
	}

	m.UpdateDatasetsStatus(w.ID, w.Status)
	m.UpdateDatasetsPercent(w.ID, int64(w.Percent))

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
	})

	return
}

type listDatasets struct {
	Datasets []m.Dataset `json:"datasets"`
	Total    int64       `json:"total"`
}

// ListDatasets 按数据库存储顺序依次获得数据/项目信息
// @Description 按数据库存储顺序依次获得数据/项目信息
// @tags API1 数据/项目（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param limit query string false "limit, default 1"
// @Param skip query string false "skip, default 0"
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/listdatasets [get]
func ListDatasets(c *gin.Context) {
	limitStr := c.DefaultQuery("limit", "1")
	skipStr := c.DefaultQuery("skip", "0")
	limit, _ := strconv.ParseInt(limitStr, 10, 64)
	skip, _ := strconv.ParseInt(skipStr, 10, 64)

	total, ds, err := m.ListDataset(int(limit), int(skip))
	if err != nil {
		logger.Info.Println(err)
	}
	/*
		for idx, v := range ds {
			ds[idx].CreatedAtTs = v.CreatedAt.Unix() * 1000
			ds[idx].StartTimeTs = v.StartTime.Unix() * 1000
		}
	*/

	dts := listDatasets{}
	dts.Datasets = ds
	dts.Total = total

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   dts,
	})
	return
}

// GetJobResult 获得任务状态（数据处理/训练/预测）
// @Description 获得任务状态（数据处理/训练/预测）
// @tags API1 任务（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/jobresult [get]
func GetJobResult(c *gin.Context) {
	idStr := c.DefaultQuery("id", "1")
	id, _ := strconv.ParseInt(idStr, 10, 64)

	d, _ := m.GetOneDatasetById(int(id))

	j := f.LoadJSONFile(f.GetInfoJSONPath(d))
	logger.Info.Println(j.ID)

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   j,
	})

	return
}

// GetJobPercent 获得任务进度（数据处理/训练/预测）
// @Description 获得任务进度（数据处理/训练/预测）
// @tags API1 任务（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/jobpercent [get]
func GetJobPercent(c *gin.Context) {
	idStr := c.DefaultQuery("id", "0")
	id, _ := strconv.ParseInt(idStr, 10, 64)

	d, _ := m.GetOneDatasetById(int(id))

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   d.Percent,
	})

	return
}

// GetJobLog 获得任务数据处理/训练/预测后端产生的log
// @Description 获得任务数据处理/训练/预测后端产生的log
// @tags API1 任务（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/joblog [get]
func GetJobLog(c *gin.Context) {
	idStr := c.DefaultQuery("id", "1")
	id, _ := strconv.ParseInt(idStr, 10, 64)
	typeStr := c.DefaultQuery("type", "c") // c-- crop  t--train

	d, _ := m.GetOneDatasetById(int(id))

	j := f.GetLogContent(d, typeStr)

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   j,
	})

	return
}

// GetModelInfo 获得训练任务生成模型的信息
// @Description 获得训练任务生成模型的信息
// @tags API1 模型（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/jobmodel [get]
func GetModelInfo(c *gin.Context) {
	idStr := c.DefaultQuery("id", "1")
	id, _ := strconv.ParseInt(idStr, 10, 64)
	typeStr := c.DefaultQuery("type", "c") // s-- svm  g--gan

	d, _ := m.GetOneDatasetById(int(id))

	j := f.GetModelInfo(d, typeStr)

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   j,
	})
	return
}

// SaveModelInfo 把训练任务生成模型信息存数据库
// @Description 把训练任务生成模型信息存数据库
// @tags API1 模型（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/savemodel [get]
func SaveModelInfo(c *gin.Context) {
	w := m.Model{}
	err := c.BindJSON(&w)

	logger.Info.Println(w, err)

	err = w.CreateModelInfo()
	if err == nil {
		c.JSON(e.StatusReqOK, gin.H{
			"status": e.StatusSucceed,
			"data":   "ok",
		})
	} else {
		c.JSON(e.StatusReqOK, gin.H{
			"status": e.StatusSucceed,
			"data":   "failed",
		})
	}
	return
}
