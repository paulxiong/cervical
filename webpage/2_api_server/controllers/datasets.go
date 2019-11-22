package controllers

import (
	"strconv"
	"strings"

	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
	f "github.com/paulxiong/cervical/webpage/2_api_server/functions"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	models "github.com/paulxiong/cervical/webpage/2_api_server/models"
	res "github.com/paulxiong/cervical/webpage/2_api_server/responses"
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
// @Summary 获得所有图片及标注的统计信息
// @Description 获得所有图片及标注的统计信息
// @tags API1 数据（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Router /api1/dtinfo [get]
func AllInfo(c *gin.Context) {
	st := Statistics{}
	st.CategoryLists = make([]Category2, 0)

	total1, _, _ := models.ListImage(1, 0)
	st.TotalImage = total1

	total, cs, _ := models.ListCategory(100, 0)
	st.TotalCategory = total

	total2, _ := models.ListImageCntByLabelType(1)
	st.TotalImageNorm = total2

	totalN, _ := models.ListLabelCountByPN(0)
	totalP, _ := models.ListLabelCountByPN(1)

	for _, v := range cs {
		_total, _, _ := models.ListLabelByType(1, 0, int(v.ID))
		_total2, _ := models.ListImageCntByLabelType(int(v.ID))
		st.CategoryLists = append(st.CategoryLists, Category2{
			Name:   v.Name,
			Other:  v.Other,
			P1N0:   v.P1N0,
			Cnt:    _total,
			ID:     int(v.ID),
			CntImg: _total2,
		})
	}

	total2, ls2, err2 := models.ListLabel(1, 0)
	logger.Info.Println(total2, ls2, err2)
	st.TotalLabel = total2
	st.TotalLabelP = totalP
	st.TotalLabelN = totalN

	res.ResSucceedStruct(c, st)
	return
}

// BatchInfo 批次信息
type BatchInfo struct {
	Total  int      `json:"total"  example:"100"` // 总批次个数
	Batchs []string `json:"batchs" example:"abc"` // 批次数组
}

// GetBatchInfo 获得所有批次信息
// @Summary 获得所有批次信息
// @Description 获得所有批次信息
// @tags API1 数据（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param limit query string false "limit, default 100"
// @Param skip query string false "skip, default 0"
// @Success 200 {object} controllers.BatchInfo
// @Router /api1/batchinfo [get]
func GetBatchInfo(c *gin.Context) {
	limitStr := c.DefaultQuery("limit", "100")
	skipStr := c.DefaultQuery("skip", "0")
	limit, _ := strconv.ParseInt(limitStr, 10, 64)
	skip, _ := strconv.ParseInt(skipStr, 10, 64)

	total, bs, err := models.ListBatch(int(limit), int(skip))
	if err != nil {
		res.ResFailedStatus(c, e.Errors["BatchListFailed"])
		return
	}
	bi := BatchInfo{
		Total:  int(total),
		Batchs: bs,
	}
	res.ResSucceedStruct(c, bi)
	return
}

// MedicalIDInfo 病例信息
type MedicalIDInfo struct {
	Total      int      `json:"total"`
	MedicalIds []string `json:"medicalids"`
}

// GetMedicalIDInfo 获得所有病例信息
// @Summary 获得所有病例信息
// @Description 获得所有病例信息
// @tags API1 数据（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {object} controllers.MedicalIDInfo
// @Router /api1/medicalidinfo [get]
func GetMedicalIDInfo(c *gin.Context) {
	var total int
	allms := make([]string, 0)
	batchid := c.DefaultQuery("batchid", "")
	batchids := strings.Split(batchid, "|")
	for _, v := range batchids {
		totalms, _ms, _ := models.ListMedicalIDByBatchID(100, 0, v)
		total = total + int(totalms)
		for _, mdicalid := range _ms {
			allms = append(allms, mdicalid)
		}
	}
	mi := MedicalIDInfo{
		Total:      int(total),
		MedicalIds: allms,
	}
	res.ResSucceedStruct(c, mi)
	return
}

// CategoryInfo 细胞类型信息
type CategoryInfo struct {
	ID   int    `json:"id"   example:"1"`    // 细胞类型对应的ID
	Name string `json:"name" example:"Norm"` // 细胞类型的英文缩写
	Desc string `json:"desc" example:"正常细胞"` // 细胞类型的中文描述
}

// CategorysInfo 所有细胞类型信息
type CategorysInfo struct {
	Total     int            `json:"total" example:"100"` // 总数
	Categorys []CategoryInfo `json:"categorys"`           // 分类
}

// GetCategoryInfo 获得细胞分类信息
// @Summary 获得细胞分类信息
// @Description 获得细胞分类信息
// @tags API1 数据（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {object} controllers.CategorysInfo
// @Router /api1/categoryinfo [get]
func GetCategoryInfo(c *gin.Context) {
	var ci CategorysInfo
	ci.Categorys = make([]CategoryInfo, 0)
	total, cs, _ := models.ListCategory(100, 0)
	ci.Total = int(total)
	for _, v := range cs {
		ci.Categorys = append(ci.Categorys, CategoryInfo{
			ID:   int(v.ID),
			Name: v.Name,
			Desc: v.Other,
		})
	}
	res.ResSucceedStruct(c, ci)
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
	Images []string `json:"images" example:"abc.png"` // 图片路径数组
}

// GetImgListOfWanted 获得所选批/次病/细胞类型的图片
// @Summary 获得所选批/次病/细胞类型的图片
// @Description 获得所选批/次病/细胞类型的图片
// @tags API1 数据（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {object} controllers.wanted2
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
		ws, err2 := models.ListWantedImages(v.Num, 0, w.Batchs, w.Medicalids, v.ID)
		logger.Info.Println(ws, err2)

		for _, v2 := range ws {
			images.Images = append(images.Images, v2)
		}
	}

	res.ResSucceedStruct(c, images)
	return
}

type imageslists struct {
	Total  int64          `json:"total"`
	Images []models.Image `json:"images"`
}

// GetImgListOneByOne 按数据库存储的顺序依次得到图片的信息
// @Summary 按数据库存储的顺序依次得到图片的信息
// @Description 按数据库存储的顺序依次得到图片的信息
// @tags API1 数据（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {object} controllers.imageslists
// @Router /api1/imglistsonebyone [get]
func GetImgListOneByOne(c *gin.Context) {
	limitStr := c.DefaultQuery("limit", "1")
	skipStr := c.DefaultQuery("skip", "0")
	limit, _ := strconv.ParseInt(limitStr, 10, 64)
	skip, _ := strconv.ParseInt(skipStr, 10, 64)

	images := imageslists{}
	images.Images = make([]models.Image, 0)

	total, imgs, _ := models.ListImage(int(limit), int(skip))

	for _, v := range imgs {
		images.Images = append(images.Images, v)
	}
	images.Total = total

	res.ResSucceedStruct(c, images)
	return
}

// imagesNPTypeByMedicalID 选中的批次、病例的传入参数
type imagesNPTypeByMedicalID struct {
	Batchids       []string `json:"batchids"   example:"redhouse"`          //批次号数组
	Medicalids     []string `json:"medicalids" example:"1817134"`           //病历号数组
	Desc           string   `json:"desc"       example:"this is a dataset"` //数据集的文字描述
	ParameterGray  int      `json:"parameter_gray"  example:"1"`            //数据处理时候颜色，默认1使用灰色，0使用彩色
	ParameterSize  int      `json:"parameter_size"  example:"100"`          //切割的正方形边长，默认100像素
	ParameterType  int      `json:"parameter_type"  example:"0"`            //切割类型，0--图片直接检测并切割出细胞 1--按照标注csv切割细胞 2--mask-rcnn检测细胞和csv交集的切割
	ParameterMid   int      `json:"parameter_mid"   example:"12"`           //切割使用的模型id
	ParameterCache int      `json:"parameter_cache" example:"1"`            //是否使用裁剪过的cache，0--不使用1--使用
}
type imagesNPCount struct {
	CountN int `json:"countn"`
	CountP int `json:"countp"`
}

// GetImagesNPTypeByMedicalID 通过所选中的批次/病例/图片, 返回N/P图片的个数统计
// @Summary 通过所选中的批次/病例/图片, 返回N/P图片的个数统计
// @Description 通过所选中的批次/病例/图片, 返回N/P图片的个数统计
// @tags API1 数据（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {object} controllers.imagesNPCount
// @Router /api1/getimgnptypebymids [post]
func GetImagesNPTypeByMedicalID(c *gin.Context) {
	cnt := imagesNPCount{}
	w := imagesNPTypeByMedicalID{}
	err := c.BindJSON(&w)
	if err != nil {
		res.ResFailedStatus(c, e.Errors["PostDataInvalied"])
		return
	}

	totaln, totalp, _ := models.ListImagesNPTypeByMedicalID(w.Medicalids)
	cnt.CountN = totaln
	cnt.CountP = totalp

	res.ResSucceedStruct(c, cnt)
	return
}

// CreateDataset 新建数据集
// @Summary 新建数据集
// @Description 新建数据集
// @tags API1 数据集（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param createdataset body controllers.imagesNPTypeByMedicalID true "创建数据集"
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Router /api1/createdataset [post]
func CreateDataset(c *gin.Context) {
	w := imagesNPTypeByMedicalID{}
	err := c.BindJSON(&w)
	if err != nil {
		res.ResFailedStatus(c, e.Errors["PostDataInvalied"])
		return
	}

	usr, _ := models.GetUserFromContext(c)

	dt := models.Dataset{}
	dt.ID = 0
	dt.CreatedBy = usr.ID
	dt.Desc = w.Desc
	dt.Dir = u.GetRandomSalt()
	dt.Status = 0
	dt.BatchIDs1 = w.Batchids
	dt.MedicalIDs1 = w.Medicalids
	// 处理的参数
	dt.ParameterGray = w.ParameterGray
	dt.ParameterSize = w.ParameterSize
	dt.ParameterType = w.ParameterType
	dt.ParameterMid = w.ParameterMid
	dt.ParameterCache = w.ParameterCache

	dt.CreateDatasets()

	//根据病历号取出所有的图片
	medicalids := make([]models.Image, 0)
	for _, v := range w.Medicalids {
		_, _imgs, _ := models.ListImagesByMedicalID2(v)
		for _, v2 := range _imgs {
			medicalids = append(medicalids, v2)
		}
	}
	if len(medicalids) < 1 {
		res.ResFailedStatus(c, e.Errors["MedicalImageNotFound"])
		return
	}

	cntn, cntp := f.CreateDataset(medicalids, &dt)
	dt.Status = 1
	models.UpdateDatasetsStatus(dt.ID, dt.Status)

	f.NewJSONFile(dt, w.Batchids, w.Medicalids, cntn, cntp)

	res.ResSucceedInt64(c, dt.ID)
	return
}

type jobResult struct {
	ID      int64 `json:"id"`     // 数据集ID或者项目ID
	Type    int   `json:"type"`   // 0未知 1数据处理 2训练 3预测
	Status  int   `json:"status"` // 0初始化 1送去处理 2开始处理 3处理出错 4处理完成
	MType   int   `json:"mtype"`  // 目前预测时候有用,表示使用哪种模型,0未知 1UNET 2GAN 3SVM 4MASKRCNN 5AUTOKERAS 6 MALA
	ETA     int   `json:"ETA"`
	Percent int   `json:"percent"` // 完成百分比
}

// GetOneJob python端请求一个任务（数据处理/训练/预测），python端会指定请求任务的状态和类型
// @Summary python端请求一个任务（数据处理/训练/预测），python端会指定请求任务的状态和类型
// @Description python端请求一个任务（数据处理/训练/预测），python端会指定请求任务的状态和类型。注意文档的返回值有２中，为了区分其中一种code写成了2000，其实应该是200
// @tags API1 任务（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {object} models.Dataset
// @Success 2000 {object} models.Project
// @Router /api1/job [post]
func GetOneJob(c *gin.Context) {
	w := jobResult{}
	c.BindJSON(&w)

	//数据处理
	if w.Type == 1 {
		dt, err := models.GetOneDatasetsToProcess(w.Status)
		if err != nil {
			res.ResSucceedStruct(c, dt)
			return
		}
		//0初始化 1送去处理 2开始处理 3处理出错 4处理完成 5目录不存在 6送去训练
		if w.Status == 1 {
			models.UpdateDatasetsStatus(dt.ID, 2)
		}

		res.ResSucceedStruct(c, dt)
	} else if w.Type == 2 || w.Type == 3 {
		project, err := models.GetOneProjectToProcess(w.Status, w.Type, w.MType)
		if err != nil {
			res.ResSucceedStruct(c, project)
			return
		}
		//0初始化 1送去处理 2开始处理 3处理出错 4处理完成 5 送去审核预测结果 6 预测结果审核完成
		if w.Status == 1 {
			models.UpdateProjectStatus(project.ID, 2)
		}
		res.ResSucceedStruct(c, project)
	}
	return
}

// SetJobResult python端更新任务状态/进度（数据处理/训练/预测）
// @Summary python端更新任务状态/进度（数据处理/训练/预测）
// @Description python端更新任务状态/进度（数据处理/训练/预测）
// @tags API1 任务（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Router /api1/jobresult [post]
func SetJobResult(c *gin.Context) {
	w := jobResult{}
	err := c.BindJSON(&w)
	if err != nil {
		res.ResFailedStatus(c, e.Errors["PostDataInvalied"])
		return
	}
	// 0未知 1数据处理 2训练 3预测
	if w.Type == 1 {
		models.UpdateDatasetsStatus(w.ID, w.Status)
		models.UpdateDatasetsPercent(w.ID, w.Percent, w.ETA)
		if w.Status == 4 { //处理完成
			done := 1 //处理完1 处理之前0
			d, _ := models.GetOneDatasetByID(int(w.ID))
			j := f.LoadJSONFile(f.GetInfoJSONPath(d.Dir, int64(done)))
			models.UpdateDatasetsCellTypes(w.ID, j.Types)
		}
	} else if w.Type == 2 || w.Type == 3 {
		models.UpdateProjectStatus(w.ID, w.Status)
		models.UpdateProjectPercent(w.ID, w.Percent, w.ETA)
	}

	// 预测任务结束时候要把结果写入数据库
	// 训练任务： 0初始化 1送去处理 2开始处理 3处理出错 4处理完成 5 送去审核预测结果 6 预测结果审核完成
	if w.Type == 3 && w.Status == 4 {
		_p, err2 := models.GetOneProjectByID(int(w.ID))
		if err2 == nil && len(_p.Dir) > 0 {
			result := f.LoadPredictJSONFile(_p.Dir)
			for _, v := range result.Cells {
				logger.Info.Println(v.URL, v.Type, v.Predict, v.Score, v.X1, v.Y1, v.X2, v.Y2)
				// PredictType := 100 //1到15是细胞类型，51-阳性  50-阴性， 100 未知
				cellpredict := &models.Predict{
					ID:           0,
					ImgID:        v.ImgID,
					PID:          w.ID,
					X1:           v.X1,
					Y1:           v.Y1,
					X2:           v.X2,
					Y2:           v.Y2,
					CellPath:     v.URL,
					PredictScore: int(v.Score * 100),
					PredictType:  v.Predict,
					PredictP1n0:  0,
					TrueType:     v.Predict,
					TrueP1n0:     0,
					VID:          0,
					Status:       0,
				}
				cellpredict.CreatePredict()

				// 状态改为送去审核, 0初始化 1送去处理 2开始处理 3处理出错 4处理完成 5 送去审核预测结果 6 预测结果审核完成
				models.UpdateProjectStatus(w.ID, 5)
			}
		}
	}
	res.ResSucceedString(c, "ok")
	return
}

type listDatasets struct {
	Datasets []models.Dataset `json:"datasets"`
	Total    int64            `json:"total"`
}

// ListDatasets 按数据库存储顺序依次获得数据集信息
// @Summary 按数据库存储顺序依次获得数据集信息
// @Description 按数据库存储顺序依次获得数据集信息
// @tags API1 数据集（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param limit query string false "limit, default 1"
// @Param skip query string false "skip, default 0"
// @Param order query string false "order, default 1, 1倒序，0顺序，顺序是指创建时间"
// @Success 200 {object} controllers.listDatasets
// @Router /api1/listdatasets [get]
func ListDatasets(c *gin.Context) {
	limitStr := c.DefaultQuery("limit", "1")
	skipStr := c.DefaultQuery("skip", "0")
	orderStr := c.DefaultQuery("order", "1")
	limit, _ := strconv.ParseInt(limitStr, 10, 64)
	skip, _ := strconv.ParseInt(skipStr, 10, 64)
	_order, _ := strconv.ParseInt(orderStr, 10, 64)

	total, ds, err := models.ListDataset(int(limit), int(skip), int(_order))
	if err != nil {
		logger.Info.Println(err)
	}

	dts := listDatasets{}
	dts.Datasets = ds
	dts.Total = total

	res.ResSucceedStruct(c, dts)
	return
}

// GetJobResult 获得数据集状态
// @Summary 获得数据集状态。查看完成前的标注信息还是完成后的细胞统计信息，二者返回的数据结构完全一致
// @Description 获得数据集状态。查看完成前的标注信息还是完成后的细胞统计信息，二者返回的数据结构完全一致
// @tags API1 任务（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param did query string false "did, default 1, 数据集的ID"
// @Param done query string false "查看完成前的标注信息还是完成后的细胞统计信息, default 0 是完成之前的标注信息， 1是完成之后的细胞信息"
// @Param limit query string false "limit, default 10000, 细胞图个数上限制"
// @Param skip query string false "skip, default 0, 细胞图跳过的个数"
// @Param limit2 query string false "limit2, default 100, 原图个数上限制"
// @Param skip2 query string false "skip2, default 0, 原图跳过的个数"
// @Success 200 {object} function.JobInfo
// @Router /api1/jobresult [get]
func GetJobResult(c *gin.Context) {
	didStr := c.DefaultQuery("did", "1")
	did, _ := strconv.ParseInt(didStr, 10, 64)
	limitStr := c.DefaultQuery("limit", "10000")
	skipStr := c.DefaultQuery("skip", "0")
	limit, _ := strconv.ParseInt(limitStr, 10, 64)
	skip, _ := strconv.ParseInt(skipStr, 10, 64)
	limit2Str := c.DefaultQuery("limit2", "100")
	skip2Str := c.DefaultQuery("skip2", "0")
	limit2, _ := strconv.ParseInt(limit2Str, 10, 64)
	skip2, _ := strconv.ParseInt(skip2Str, 10, 64)

	doneStr := c.DefaultQuery("done", "0")
	done, _ := strconv.ParseInt(doneStr, 10, 64)

	d, _ := models.GetOneDatasetByID(int(did))

	j := f.LoadJSONFile(f.GetInfoJSONPath(d.Dir, done))
	if len(j.CellsCrop) > int(limit) {
		var CellsCrop []string
		for index, v := range j.CellsCrop {
			if index < int(skip) {
				continue
			}
			if len(CellsCrop) >= int(limit) {
				break
			}
			CellsCrop = append(CellsCrop, v)
		}
		j.CellsCrop = CellsCrop
	}
	if len(j.OriginImgs) > int(limit2) {
		var OriginImgs []string
		for index, v := range j.OriginImgs {
			if index < int(skip2) {
				continue
			}
			if len(OriginImgs) >= int(limit2) {
				break
			}
			OriginImgs = append(OriginImgs, v)
		}
		j.OriginImgs = OriginImgs
	}

	j.Status = d.Status

	res.ResSucceedStruct(c, j)
	return
}

type datasetPercent struct {
	Percent int `json:"percent" example:"50"` //进度50%
	ETA     int `json:"ETA" example:"1800"`   //预测还有1800秒结束
	Status  int `json:"status" example:"4"`   //当前任务状态
}

// GetJobPercent 获得任务进度（数据处理/训练/预测）
// @Summary 获得任务进度（数据处理/训练/预测）
// @Description 获得任务进度（数据处理/训练/预测）
// @tags API1 任务（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param id query string false "id, default 1, 被预测的数据集ID/被预测或训练的项目的ID，即目标任务的ID"
// @Param type query string false "type, default 1, 查询的对象 0 未知 1 数据集处理 2 训练 3 预测"
// @Success 200 {object} controllers.datasetPercent
// @Router /api1/jobpercent [get]
func GetJobPercent(c *gin.Context) {
	idStr := c.DefaultQuery("id", "1")
	id, _ := strconv.ParseInt(idStr, 10, 64)
	typeStr := c.DefaultQuery("type", "1") // 0 未知 1 数据集处理 2 训练 3 预测
	_type, _ := strconv.ParseInt(typeStr, 10, 64)

	percent := datasetPercent{}

	if _type == 1 {
		d, _ := models.GetOneDatasetByID(int(id))
		percent.Percent = d.ProcessPercent
		percent.ETA = d.ETA
		percent.Status = d.Status
	} else if _type == 2 || _type == 3 {
		p, _ := models.GetOneProjectByID(int(id))
		percent.Percent = p.Percent
		percent.ETA = p.ETA
		percent.Status = p.Status
	}

	res.ResSucceedStruct(c, percent)
	return
}

// GetJobLog 获得任务数据处理/训练/预测后端产生的log
// @Summary 获得任务数据处理/训练/预测后端产生的log
// @Description 获得任务数据处理/训练/预测后端产生的log
// @tags API1 任务（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param id query string false "id, default 1, 被预测的数据集ID/被预测或训练的项目的ID"
// @Param type query string false "type, default 1, 查询的对象 0 未知 1 数据集处理 2 训练 3 预测"
// @Success 200 {string} json "{"data": "日志字符串",	"status": 200}"
// @Router /api1/joblog [get]
func GetJobLog(c *gin.Context) {
	idStr := c.DefaultQuery("id", "1")
	id, _ := strconv.ParseInt(idStr, 10, 64)
	typeStr := c.DefaultQuery("type", "1") // 0 未知 1 数据集处理 2 训练 3 预测
	_type, _ := strconv.ParseInt(typeStr, 10, 64)

	dirname := ""

	if _type == 1 {
		d, _ := models.GetOneDatasetByID(int(id))
		dirname = d.Dir
	} else if _type == 2 || _type == 3 {
		project, _ := models.GetOneProjectByID(int(id))
		dirname = project.Dir
	}
	logstr := f.GetLogContent(dirname, int(_type))
	res.ResSucceedString(c, logstr)
	return
}

// ImageBase FOV图片基础信息
type imgofmedical struct {
	ID      int64  `json:"id"      example:"100"`       //图片的ID
	Imgpath string `json:"imgpath" example:"img/1.png"` //图片的半截URL
	W       int    `json:"w"       example:"100"`       //图片宽
	H       int    `json:"h"       example:"100"`       //图片高
}

type imgsofmedical struct {
	Imgs  []*imgofmedical `json:"imgs"`                 //图片的数组
	Total int             `json:"total"  example:"100"` //图片的个数
}

// GetImgListOfMedicalID 获得所选批/次病的所有图片
// @Summary 获得所选批/次病的所有图片
// @Description 获得所选批/次病的所有图片
// @tags API1 数据（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param bid query string false "bid, default 空字符串, 批次号"
// @Param mdcid query string false "mdcid, default 空字符串, 病历号"
// @Param limit query string false "limit, default 100, 个数上限制"
// @Param skip query string false "skip, default 0, 跳过的个数"
// @Success 200 {object} controllers.imgsofmedical
// @Router /api1/getimgbymid [get]
func GetImgListOfMedicalID(c *gin.Context) {
	MedicalID := c.DefaultQuery("mdcid", "")
	BatchID := c.DefaultQuery("bid", "")
	limitStr := c.DefaultQuery("limit", "100")
	skipStr := c.DefaultQuery("skip", "0")
	limit, _ := strconv.ParseInt(limitStr, 10, 32)
	skip, _ := strconv.ParseInt(skipStr, 10, 32)

	if len(MedicalID) < 1 || len(BatchID) < 1 {
		res.ResFailedStatus(c, e.Errors["MedicalBatchInvalied"])
		return
	}

	total, _imgs, err := models.ListImageOfMedicalID(BatchID, MedicalID, limit, skip)
	if err != nil {
		res.ResFailedStatus(c, e.Errors["MedicalImageNotFound"])
		return
	}
	imgs := imgsofmedical{
		Total: total,
	}
	imgs.Imgs = make([]*imgofmedical, 0)

	for _, v := range _imgs {
		imgs.Imgs = append(imgs.Imgs, &imgofmedical{
			ID:      v.ID,
			Imgpath: f.Imgpath(BatchID, MedicalID, v.Imgpath, v.Type),
			W:       v.W,
			H:       v.H,
		})
	}
	res.ResSucceedStruct(c, imgs)
	return
}

/*
type treeNode struct {
	Value    string      `json:"value"      example:"100"` // 节点值
	Label    string      `json:"label"      example:"100"` // 节点名字
	Children []*treeNode `json:"children"`                 //子节点
}

// GetImgTree 获得所批次/病例/图片的树状结构
// @Summary 获得所批次/病例/图片的树状结构
// @Description 获得所批次/病例/图片的树状结构
// @tags API1 数据（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {object} controllers.imgsofmedical
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/getimgtree [get]
func GetImgTree(c *gin.Context) {
	_, bs, err := models.ListBatch(100, 0)
	if err != nil {
		c.JSON(e.StatusReqOK, gin.H{
			"status": e.StatusSucceed,
			"data":   "",
		})
		return
	}

	trees := make([]treeNode, 0)

	// 批次ID
	for _, v := range bs {
		tree1 := treeNode{Value: v, Label: v}
		_, _ms, _ := models.ListMedicalIDByBatchID(10000, 0, v)
		tree1.Children = make([]*treeNode, 0)
		for _, mdicalid := range _ms {
			tree2 := &treeNode{Value: mdicalid, Label: mdicalid}
			_, imgs, _ := models.ListImageOfMedicalID(v, mdicalid, 10000, 0)
			tree2.Children = make([]*treeNode, 0)
			for _, _img := range imgs {
				tree3 := &treeNode{Value: fmt.Sprintf("%d", _img.ID), Label: f.Imgpath(v, mdicalid, _img.Imgpath, _img.Type)}
				tree2.Children = append(tree2.Children, tree3)
			}

			tree1.Children = append(tree1.Children, tree2)
		}

		trees = append(trees, tree1)
	}
	ResStruct(c, trees)
	return
}
*/
