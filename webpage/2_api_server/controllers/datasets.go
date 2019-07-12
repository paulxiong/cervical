package controllers

import (
	"strconv"
	"strings"

	e "../error"
	f "../functions"
	logger "../log"
	m "../models"
	u "../utils"

	"github.com/gin-gonic/gin"
)

// Category2 标注信息
type Category2 struct {
	Id     int    `json:"id"`     //标注对应的id
	Cnt    int64  `json:"cnt"`    //标注次数
	CntImg int64  `json:"cntimg"` //该标注分类下的图片数量
	Name   string `json:"name"`   //名字
	P1N0   int    `json:"p1n0"`   //是阴性还是阳性
	Other  string `json:"other"`  //描述
}

type Statistics struct {
	TotalImage     int64 `json:"totalimg"`
	TotalImageNorm int64 `json:"totalimgnorm"`
	TotalLabel     int64 `json:"totallabel"`
	TotalLabelP    int64 `json:"totallabelp"`
	TotalLabelN    int64 `json:"totallabeln"`
	TotalCategory  int64 `json:"totalcategory"`

	CategoryLists []Category2 `json:"categorylists"`
}

func AllInfo(c *gin.Context) {
	st := Statistics{}
	st.CategoryLists = make([]Category2, 0)

	total1, _, _ := m.ListImage(1, 0)
	st.TotalImage = total1

	total, cs, _ := m.ListCategory(100, 0)
	st.TotalCategory = total

	total2, _ := m.ListImageCntByLabelType(1)
	st.TotalImageNorm = total2

	total_n, _ := m.ListLabelCountByPN(0)
	total_p, _ := m.ListLabelCountByPN(1)

	for _, v := range cs {
		_total, _, _ := m.ListLabelByType(1, 0, int(v.Id))
		_total2, _ := m.ListImageCntByLabelType(int(v.Id))
		st.CategoryLists = append(st.CategoryLists, Category2{
			Name:   v.Name,
			Other:  v.Other,
			P1N0:   v.P1N0,
			Cnt:    _total,
			Id:     int(v.Id),
			CntImg: _total2,
		})
	}

	total2, ls2, err2 := m.ListLabel(1, 0)
	logger.Info.Println(total2, ls2, err2)
	st.TotalLabel = total2
	st.TotalLabelP = total_p
	st.TotalLabelN = total_n

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   st,
	})
	return
}

type BatchInfo struct {
	Total  int      `json:"total"`
	Batchs []string `json:"batchs"`
}

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

type MedicalIdInfo struct {
	Total      int      `json:"total"`
	MedicalIds []string `json:"medicalids"`
}

func GetMedicalIdInfo(c *gin.Context) {
	var total int = 0
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
	mi := MedicalIdInfo{
		Total:      int(total),
		MedicalIds: allms,
	}
	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   mi,
	})
	return
}

type CategoryInfo struct {
	Id      int    `json:"id"`
	Name    string `json:"name"`
	Num     int    `json:"num"`
	Checked bool   `json:"checked"`
}

type CategorysInfo struct {
	Total     int            `json:"total"`
	Categorys []CategoryInfo `json:"categorys"`
}

func GetCategoryInfo(c *gin.Context) {
	var ci CategorysInfo
	ci.Categorys = make([]CategoryInfo, 0)
	total, cs, _ := m.ListCategory(100, 0)
	ci.Total = int(total)
	for _, v := range cs {
		ci.Categorys = append(ci.Categorys, CategoryInfo{
			Id:      int(v.Id),
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
	Id  int `json:"id"`
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

func GetImgListOfWanted(c *gin.Context) {
	images := wanted2{}
	images.Images = make([]string, 0)
	w := wanted{}
	err := c.BindJSON(&w)
	if err != nil {
		logger.Info.Println(err)
	}

	for _, v := range w.Categorys {
		logger.Info.Println(v.Num, 0, w.Batchs, w.Medicalids, v.Id)
		ws, err2 := m.ListWantedImages(v.Num, 0, w.Batchs, w.Medicalids, v.Id)
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

func GetImgListOneByOne(c *gin.Context) {
	limit_str := c.DefaultQuery("limit", "1")
	skip_str := c.DefaultQuery("skip", "0")
	limit, _ := strconv.ParseInt(limit_str, 10, 64)
	skip, _ := strconv.ParseInt(skip_str, 10, 64)

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

type Labelslists struct {
	Labels []m.Label `json:"labels"`
}

func GetLabelByImageId(c *gin.Context) {
	limit_str := c.DefaultQuery("limit", "1")
	skip_str := c.DefaultQuery("skip", "0")
	imgid_str := c.DefaultQuery("imgid", "1")
	imgid, _ := strconv.ParseInt(imgid_str, 10, 64)
	limit, _ := strconv.ParseInt(limit_str, 10, 64)
	skip, _ := strconv.ParseInt(skip_str, 10, 64)

	labels := Labelslists{}
	labels.Labels = make([]m.Label, 0)

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

type imagesNPTypeByMedicalId struct {
	Batchids   []string `json:"batchids"`
	Medicalids []string `json:"medicalids"`
	Desc       string   `json:"desc"`
}
type imagesNPCount struct {
	CountN int `json:"countn"`
	CountP int `json:"countp"`
}

func GetImagesNPTypeByMedicalId(c *gin.Context) {
	cnt := imagesNPCount{}
	w := imagesNPTypeByMedicalId{}
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

func CreateDataset(c *gin.Context) {
	w := imagesNPTypeByMedicalId{}
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

	f.NewJsonFile(dt, w.Batchids, w.Medicalids, cntn, cntp)

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   "",
	})

	return
}

func GetOneJob(c *gin.Context) {
	dt, err := m.GetOneDatasetsToCrop()
	if err != nil {
		c.JSON(e.StatusReqOK, gin.H{
			"status": e.StatusSucceed,
			"data":   dt,
		})
		return
	}
	m.UpdateDatasetsStatus(dt.Id, 2)

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   dt,
	})
	return
}

type jobResult struct {
	Id     int64 `json:"id"`
	Status int   `json:"status"`
}

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

	m.UpdateDatasetsStatus(w.Id, w.Status)

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
	})

	return
}

type listDatasets struct {
	Datasets []m.Dataset `json:"datasets"`
	Total    int64       `json:"total"`
}

func ListDatasets(c *gin.Context) {
	limit_str := c.DefaultQuery("limit", "1")
	skip_str := c.DefaultQuery("skip", "0")
	limit, _ := strconv.ParseInt(limit_str, 10, 64)
	skip, _ := strconv.ParseInt(skip_str, 10, 64)

	total, ds, err := m.ListDataset(int(limit), int(skip))
	if err != nil {
		logger.Info.Println(err)
	}
	for idx, v := range ds {
		ds[idx].CreatedAtTs = v.CreatedAt.Unix() * 1000
		ds[idx].StartTimeTs = v.StartTime.Unix() * 1000
	}

	dts := listDatasets{}
	dts.Datasets = ds
	dts.Total = total

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   dts,
	})
	return
}

func GetJobResult(c *gin.Context) {
	id_str := c.DefaultQuery("id", "1")
	id, _ := strconv.ParseInt(id_str, 10, 64)

	d, _ := m.GetOneDatasetById(int(id))

	j := f.LoadJsonFile(f.GetInfoJsonPath(d))
	logger.Info.Println(j.Id)

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   j,
	})

	return
}

func GetJobLog(c *gin.Context) {
	id_str := c.DefaultQuery("id", "1")
	id, _ := strconv.ParseInt(id_str, 10, 64)

	d, _ := m.GetOneDatasetById(int(id))

	j := f.GetLogContent(d)

	c.JSON(e.StatusReqOK, gin.H{
		"status": e.StatusSucceed,
		"data":   j,
	})

	return
}
