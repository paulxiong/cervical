package controllers

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
	"strconv"

	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
	f "github.com/paulxiong/cervical/webpage/2_api_server/functions"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	models "github.com/paulxiong/cervical/webpage/2_api_server/models"
	res "github.com/paulxiong/cervical/webpage/2_api_server/responses"
	u "github.com/paulxiong/cervical/webpage/2_api_server/utils"

	"github.com/gin-gonic/gin"
)

// newProject 新建项目
type newProject struct {
	Desc            string `json:"desc"             example:"this is a project"` //项目的描述
	DID             int64  `json:"did"              example:"1"`                 //选择的数据集的ID, 训练项目表示训练和评估数据集， 预测项目表示预测使用的数据
	Type            int    `json:"type"             example:"1"`                 //项目类型 0 未知 1 保留 2 训练 3 预测
	Celltypes       []int  `json:"celltypes"        example:"7"`                 //选择哪几个类型做训练或者预测
	ParameterTime   int    `json:"parameter_time"   example:"1800"`              //训练使用的最长时间,单位是秒
	ParameterResize int    `json:"parameter_resize" example:"100"`               //训练/预测之前统一的尺寸,单位是像素
	ParameterMID    int    `json:"parameter_mid"    example:"1"`                 //预测使用的模型的id,只有预测时候需要
	ParameterType   int    `json:"parameter_type"   example:"0"`                 //预测方式,0没标注的图 1有标注的图
}

// CreateProject 新建(训练/预测)项目
// @Summary 新建(训练/预测)项目
// @Description 新建(训练/预测)项目
// @tags API1 项目（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param CreateProject body controllers.newProject true "新建(训练/预测)项目"
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Router /api1/createproject [post]
func CreateProject(c *gin.Context) {
	np := newProject{}
	err := c.BindJSON(&np)
	if err != nil {
		logger.Info.Println(err)
		res.ResFailedStatus(c, e.Errors["PostDataInvalied"])
		return
	}

	usr, _ := models.GetUserFromContext(c)

	p := models.Project{
		ID:              0,
		DID:             np.DID,
		Desc:            np.Desc,
		Dir:             u.GetRandomSalt(),
		Status:          1, //送去处理
		Type:            np.Type,
		ParameterTime:   np.ParameterTime,
		ParameterResize: np.ParameterResize,
		ParameterMID:    np.ParameterMID,
		ParameterType:   np.ParameterType,
		CreatedBy:       usr.ID,
	}

	_mod, _ := models.FindModelInfoByID(p.ParameterMID)
	p.ParameterMType = _mod.Type

	logger.Info.Println(np.Desc)
	logger.Info.Println(np.DID)

	p.CreateProject()

	f.NewProjectJSONFile(p, np.Celltypes, _mod)

	res.ResSucceedInt64(c, p.ID)
	return
}

type listProjectsData struct {
	Projects []models.Project `json:"projects"` //项目列表的数组
	Total    int64            `json:"total"`    //项目总个数
}

// ListProjects 按数据库存储顺序依次获得项目信息
// @Summary 按数据库存储顺序依次获得项目信息
// @Description 按数据库存储顺序依次获得项目信息
// @tags API1 项目（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param limit query string false "limit, default 1"
// @Param skip query string false "skip, default 0"
// @Param status query string false "status, default 100, 0初始化 1送去处理 2开始处理 3处理出错 4处理完成 5 送去审核预测结果 6 预测结果审核完成 100 全部 101 送去审核以及核完成的预测结果"
// @Param order query string false "order, default 1, 1倒序，0顺序，顺序是指创建时间"
// @Success 200 {object} controllers.listProjectsData
// @Router /api1/listprojects [get]
func ListProjects(c *gin.Context) {
	limitStr := c.DefaultQuery("limit", "1")
	skipStr := c.DefaultQuery("skip", "0")
	orderStr := c.DefaultQuery("order", "1")
	statusStr := c.DefaultQuery("status", "100")
	limit, _ := strconv.ParseInt(limitStr, 10, 64)
	skip, _ := strconv.ParseInt(skipStr, 10, 64)
	_order, _ := strconv.ParseInt(orderStr, 10, 64)
	status, _ := strconv.ParseInt(statusStr, 10, 64)

	total, p, err := models.ListProject(int(limit), int(skip), int(_order), int(status))
	if err != nil {
		logger.Info.Println(err)
	}

	dts := listProjectsData{}
	dts.Projects = p
	dts.Total = total
	res.ResSucceedStruct(c, dts)
	return
}

// GetTrainResult 根据传递来的项目ID，获取训练结果及信息
// @Summary 根据传递来的项目ID，获取训练结果及信息
// @Description 根据传递来的项目ID，获取训练结果及信息
// @Description status：
// @Description 200 成功
// @tags API1 项目（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param id query string false "项目的ID, default 0"
// @Success 200 {object} models.Model
// @Router /api1/trainresult [get]
func GetTrainResult(c *gin.Context) {
	idStr := c.DefaultQuery("id", "1")
	id, _ := strconv.ParseInt(idStr, 10, 64)

	d, err := models.GetOneProjectByID(int(id))
	if err != nil || d.Status != 4 {
		res.ResFailedStatus(c, e.Errors["ProjectNotReady"])
		return
	}

	modinfo := f.LoadModJSONFile(d.Dir)

	res.ResSucceedStruct(c, modinfo)
	return
}

// oneProjectPredict 按参数获得一个项目的预测结果
func oneProjectPredict(pinfo models.Project, limit int64, skip int64, correc int64) *f.PredictInfo2 {
	j := f.LoadPredictJSONFile(pinfo.Dir, 0)
	if j.ID < 1 || limit > 0 {
		// limit>0 说明需要细胞列表，要从predict2.json读取
		j = f.LoadPredictJSONFile(pinfo.Dir, 1)
	}

	j.CellsTotal = len(j.Cells)
	if j.CellsTotal > int(limit) {
		var CellsCrop []f.PredictCell
		for index, v := range j.Cells {
			if index < int(skip) {
				continue
			}
			if correc == 0 && v.Type == v.Predict {
				continue
			} else if correc == 1 && v.Type != v.Predict {
				continue
			}
			if len(CellsCrop) >= int(limit) {
				break
			}
			CellsCrop = append(CellsCrop, v)
		}
		j.Cells = CellsCrop
	}

	j.CorrecTotal = 0
	j.InCorrecTotal = 0
	for _, v := range j.PRsult {
		j.CorrecTotal = j.CorrecTotal + v.Correct
		j.CorrecTotal = j.CorrecTotal + (v.Total - v.Correct)
	}
	return &j
}

// GetPredictResult 根据传递来的项目ID，返回预测的结果
// @Summary 根据传递来的项目ID，返回预测的结果
// @Description 创建预测任务
// @Description status：
// @Description 200 创建
// @tags API1 项目（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param id query string false "id, default 0, 项目ID"
// @Param limit query string false "limit, default 500, 细胞图个数上限制"
// @Param skip query string false "skip, default 0, 细胞图跳过的个数"
// @Param correct query string false "correct, default 1, 0--预测错误 1--预测正确"
// @Success 200 {object} function.PredictInfo2
// @Router /api1/predictresult [get]
func GetPredictResult(c *gin.Context) {
	idStr := c.DefaultQuery("id", "0")
	id, _ := strconv.ParseInt(idStr, 10, 64)
	limitStr := c.DefaultQuery("limit", "500")
	skipStr := c.DefaultQuery("skip", "0")
	correctStr := c.DefaultQuery("correct", "1")
	limit, _ := strconv.ParseInt(limitStr, 10, 64)
	skip, _ := strconv.ParseInt(skipStr, 10, 64)
	correc, _ := strconv.ParseInt(correctStr, 10, 64)

	pinfo, err := models.GetOneProjectByID(int(id))
	if err != nil {
		res.ResFailedStatus(c, e.Errors["ProjectNotReady"])
		return
	}

	j := oneProjectPredict(pinfo, limit, skip, correc)
	res.ResSucceedStruct(c, j)
	return
}

type predictresult struct {
	ID     int64            `json:"id"     example:"1"`           //预测任务ID
	DID    int64            `json:"did"    example:"1"`           //用来做预测的数据集的ID
	DDir   string           `json:"ddir"   example:"dir name"`    //用来做预测的数据集的目录
	Dir    string           `json:"dir"    example:"dir name"`    //项目目录
	Desc   string           `json:"desc"   example:"description"` //项目描述
	FovCnt int              `json:"fovcnt" example:"1"`           //FOV个数
	Saved  int              `json:"saved"  example:"1"`           //该项目结果是否已经保存过，0 -- 未保存 1-- 已经
	PRsult []f.PredictRsult `json:"result"`                       //预测的细胞的个数统计
}

type allpredictresult struct {
	Projects []*predictresult `json:"projects"` //项目信息数组
	Total    int64            `json:"total"`    //项目个数
}

// GetAllPredictResult 返回所有预测完毕项目的细胞个数统计结果
// @Summary 返回所有预测完毕项目的细胞个数统计结果
// @Description 创建预测任务
// @Description status：
// @Description 200 创建
// @tags API1 项目（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param limit query string false "limit, default 500, 单次获得项目个数上限制"
// @Param skip query string false "skip, default 0, 项目跳过的个数"
// @Param status query string false "status, default 100, 0初始化 1送去处理 2开始处理 3处理出错 4处理完成 5 送去审核预测结果 6 预测结果审核完成 100 全部 101 送去审核以及核完成的预测结果"
// @Param order query string false "order, default 1, 1倒序，0顺序，顺序是指创建时间"
// @Success 200 {object} function.PredictInfo2
// @Router /api1/allpredictresult [get]
func GetAllPredictResult(c *gin.Context) {
	limitStr := c.DefaultQuery("limit", "500")
	skipStr := c.DefaultQuery("skip", "0")
	limit, _ := strconv.ParseInt(limitStr, 10, 64)
	skip, _ := strconv.ParseInt(skipStr, 10, 64)
	orderStr := c.DefaultQuery("order", "1")
	statusStr := c.DefaultQuery("status", "100")
	_order, _ := strconv.ParseInt(orderStr, 10, 64)
	status, _ := strconv.ParseInt(statusStr, 10, 64)

	total, p, err := models.ListProject(int(limit), int(skip), int(_order), int(status))
	if err != nil {
		logger.Info.Println(err)
	}

	allp := allpredictresult{}
	allp.Projects = make([]*predictresult, 0)
	for _, v := range p {
		j := oneProjectPredict(v, 0, 0, 1)
		d, _ := models.GetOneDatasetByID(int(v.DID))
		// 从数据集的配置文件info.json查找FOV个数，如果查不到再从info2.json查找, 因为之前的老代码只在info2.json里面有FOV个数
		j2 := f.LoadJSONFile(f.GetInfoJSONPath(d.Dir, 0))
		if j2.FovCnt < 1 {
			j2 = f.LoadJSONFile(f.GetInfoJSONPath(d.Dir, 1))
		}

		Saved := 0
		r, err2 := models.GetOneResultByPID(j.ID)
		if err2 == nil && r.ID > 0 {
			Saved = 1
		}

		_pr := &predictresult{
			ID:     j.ID,
			DID:    j.DID,
			DDir:   j.DDir,
			Dir:    v.Dir,
			Desc:   v.Desc,
			FovCnt: j2.FovCnt,
			Saved:  Saved,
			PRsult: j.PRsult,
		}
		allp.Projects = append(allp.Projects, _pr)
	}
	allp.Total = total

	res.ResSucceedStruct(c, allp)
	return
}

// RemoveProject 删除项目记录及项目相关的文件
// @Summary 删除项目记录及项目相关的文件
// @Description 删除项目记录及项目相关的文件
// @tags API1 项目（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param pid query string false "pid, default 0, 项目ID"
// @Param dropdt query string false "dropdt, default 0, 1删除数据集，0不删除数据集"
// @Success 200 {string} json "{"ping": "ok",	"status": 200}"
// @Router /api1/removeproject [get]
func RemoveProject(c *gin.Context) {
	pidStr := c.DefaultQuery("pid", "0")
	dropdtStr := c.DefaultQuery("dropdt", "0")
	pid, _ := strconv.ParseInt(pidStr, 10, 64)
	dropdt, _ := strconv.ParseInt(dropdtStr, 10, 64)

	pinfo, err := models.GetOneProjectByID(int(pid))
	if err != nil {
		res.ResFailedStatus(c, e.Errors["ProjectNotReady"])
		return
	}
	imgIDs := make([]int64, 0)
	predicts, _, _ := models.GetPredictAllByPID(pid)
	for _, v := range predicts {
		imgIDs = append(imgIDs, v.ImgID)
	}
	projectdir := f.GetProjectPath(pinfo.Dir)
	f.RemoveDir(projectdir)
	models.RemovePredictsByPid(pid)
	models.RemoveProjectByID(pid)

	if dropdt == 1 {
		models.RemoveImagesByIDs(imgIDs)

		dinfo, err2 := models.GetOneDatasetByID(int(pinfo.DID))
		if err2 != nil || len(dinfo.MedicalIDs1) < 1 || len(dinfo.BatchIDs1) < 1 {
			res.ResFailedStatus(c, e.Errors["DatasetsNotFound"])
			return
		}
		dpath, cellpath, imgpath := f.GetDatasetPath(dinfo.Dir, dinfo.MedicalIDs1[0], dinfo.BatchIDs1[0])
		f.RemoveDir(cellpath)
		f.RemoveDir(imgpath)
		f.RemoveDir(dpath)
		models.RemoveDatasetByID(pinfo.DID)
	}

	res.ResSucceedString(c, "ok")
	return
}

// projectResult 预测项目的结果记录
type projectResult struct {
	DID      int64  `json:"did"      example:"2"`           //数据集的id
	PID      int64  `json:"pid"      example:"3"`           //项目的id
	Desc     string `json:"desc"     example:"description"` //项目的描述
	PCnt     int    `json:"pcnt"     example:"100"`         //阳性细胞个数
	NCnt     int    `json:"ncnt"     example:"100"`         //阴性细胞个数
	UCnt     int    `json:"ucnt"     example:"100"`         //不是细胞个数
	FOVCnt   int    `json:"fovcnt"   example:"100"`         //FOV的个数
	P1N0     int    `json:"p1n0"     example:"50"`          //例预测的阴阳性 50阴性51阳性100未知
	TrueP1N0 int    `json:"truep1n0" example:"51"`          //病例实际的阴阳性 50阴性51阳性100未知
	Remark   string `json:"remark"   example:"remark"`      //备注
}

// CreateProjectResult 新建预测项目的结果记录
// @Summary 新建预测项目的结果记录
// @Description 新建预测项目的结果记录
// @tags API1 项目（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param projectResult body controllers.projectResult true "预测项目的结果"
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Router /api1/result [post]
func CreateProjectResult(c *gin.Context) {
	pr := projectResult{}
	err := c.BindJSON(&pr)
	if err != nil {
		logger.Info.Println(err)
		res.ResFailedStatus(c, e.Errors["PostDataInvalied"])
		return
	}

	usr, _ := models.GetUserFromContext(c)

	r := models.Result{
		ID:        0,
		DID:       pr.DID,
		PID:       pr.PID,
		Desc:      pr.Desc,
		PCnt:      pr.PCnt,
		NCnt:      pr.NCnt,
		UCnt:      pr.UCnt,
		FOVCnt:    pr.FOVCnt,
		P1N0:      pr.P1N0,
		TrueP1N0:  pr.TrueP1N0,
		Remark:    pr.Remark,
		CreatedBy: usr.ID,
	}
	r.CreateOrUpdateResult()

	res.ResSucceedString(c, "ok")
	return
}

// projectResult 预测项目的结果记录
type projectResults struct {
	Total    int64           `json:"total"`   //预测项目的结果记录个数
	Projects []models.Result `json:"results"` //预测项目的结果记录
}

// GetProjectResult 返回所有新建预测项目的结果记录
// @Summary 返回所有新建预测项目的结果记录
// @Description 返回所有新建预测项目的结果记录
// @tags API1 项目（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param limit query string false "limit, default 500, 预测项目的结果记录个数上限制"
// @Param skip query string false "skip, default 0, 预测项目的结果记录跳过的个数"
// @Success 200 {object} function.PredictInfo2
// @Router /api1/result [get]
func GetProjectResult(c *gin.Context) {
	limitStr := c.DefaultQuery("limit", "500")
	skipStr := c.DefaultQuery("skip", "0")
	limit, _ := strconv.ParseInt(limitStr, 10, 64)
	skip, _ := strconv.ParseInt(skipStr, 10, 64)

	allresults := projectResults{}
	allresults.Total, allresults.Projects, _ = models.ListResult(limit, skip)
	res.ResSucceedStruct(c, allresults)
	return
}

// downloadResultIDs 要下载的记录ID
type downloadResultIDs struct {
	IDs []int64 `json:"ids"` //要下载的记录ID
}

// DownloadResult 下载预测项目的结果记录为csv文件
// @Summary 下载预测项目的结果记录为csv文件
// @Description 下载预测项目的结果记录为csv文件
// @tags API1 项目（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param downloadResultIDs body controllers.downloadResultIDs true "要下载的记录ID"
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Router /api1/downloadresult [post]
func DownloadResult(c *gin.Context) {
	dr := downloadResultIDs{}
	err1 := c.ShouldBindJSON(&dr)
	if err1 != nil {
		res.ResFailedStatus(c, e.Errors["PostDataInvalied"])
		return
	}

	filename := u.GetRandomStringNum(6)
	csvname := fmt.Sprintf("%s.csv", filename)

	fd, err1 := os.OpenFile(csvname, os.O_RDWR|os.O_CREATE|os.O_APPEND, 0644)
	if err1 != nil {
		logger.Info.Println(csvname, err1)
	}
	w := csv.NewWriter(fd)
	w.Write([]string{"编号", "项目ID", "数据集ID", "批次和病例号", "阴性细胞数", "阳性细胞数", "过滤杂质数", "FOV数", "模型预测结果", "医生诊断结果", "备注"})
	w.Flush()
	for _, v := range dr.IDs {
		r, err2 := models.GetOneResultByID(v)
		if err2 != nil || r.ID < 1 {
			continue
		}
		w.Write([]string{
			fmt.Sprintf("%d", r.ID),
			fmt.Sprintf("%d", r.PID),
			fmt.Sprintf("%d", r.DID),
			r.Desc,
			fmt.Sprintf("%d", r.NCnt),
			fmt.Sprintf("%d", r.PCnt),
			fmt.Sprintf("%d", r.UCnt),
			fmt.Sprintf("%d", r.FOVCnt),
			fmt.Sprintf("%d", r.P1N0),
			fmt.Sprintf("%d", r.TrueP1N0),
			r.Remark,
		})
		w.Flush()
	}
	fd.Close()

	filesize := f.GetFileSize(csvname)
	if filesize < 1 {
		res.ResFailedStatus(c, e.Errors["CsvFailed"])
		return
	}

	//下载
	contentDisposition := fmt.Sprintf("attachment; filename=%s", csvname)
	c.Writer.Header().Add("Content-Disposition", contentDisposition)
	c.Writer.Header().Add("Content-Type", "application/zip")
	c.Writer.Header().Add("Accept-Length", fmt.Sprintf("%d", filesize))
	c.Writer.Header().Add("Content-Length", fmt.Sprintf("%d", filesize))
	c.File(csvname)
	return
}

// DownloadCells 下载指定预测结束之后项目的指定细胞类型的所有细胞
// @Summary 下载指定预测结束之后项目的指定细胞类型的所有细胞
// @Description 下载指定预测结束之后项目的指定细胞类型的所有细胞
// @tags API1 项目（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param pid query string false "pid, default 0, 要现在细胞所在的项目ID"
// @Param celltype query string false "celltype, default 0, 要现在细胞所属的预测类型"
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Router /api1/downloadresult [get]
func DownloadCells(c *gin.Context) {
	pidStr := c.DefaultQuery("pid", "0")
	pid, _ := strconv.ParseInt(pidStr, 10, 64)
	_typeStr := c.DefaultQuery("celltype", "0")
	_type, _ := strconv.ParseInt(_typeStr, 10, 64)

	pinfo, err := models.GetOneProjectByID(int(pid))
	if err != nil {
		res.ResFailedStatus(c, e.Errors["ProjectNotReady"])
		return
	}

	// 创建目录作为临时存储文件使用
	dirname := u.GetRandomStringNum(6)
	zipname := fmt.Sprintf("cell-%d-%d-%s.zip", pid, _type, dirname)
	csvname := fmt.Sprintf("cell-%d-%d-%s.csv", pid, _type, dirname)

	//初始化CSv
	fd, err1 := os.OpenFile(csvname, os.O_RDWR|os.O_CREATE|os.O_APPEND, 0644)
	if err1 != nil {
		logger.Info.Println(csvname, err1)
		res.ResFailedStatus(c, e.Errors["ZipFailed"])
		return
	}
	w := csv.NewWriter(fd)
	w.Write([]string{"cell", "type", "score"})
	w.Flush()

	var skip int64 = 0
	var limit int64 = 1000000 //这里偷懒了，应该用遍历的方法
	var correc int64 = 0
	filesname := make([]string, 0)
	filestype := make([]string, 0)
	filesscore := make([]float32, 0)
	j := oneProjectPredict(pinfo, limit, skip, correc)
	for _, v := range j.Cells {
		if v.Predict != int(_type) {
			continue
		}
		filesname = append(filesname, v.URL)
		filestype = append(filestype, fmt.Sprintf("%d", v.Predict))
		filesscore = append(filesscore, v.Score)
		_, fileName := filepath.Split(v.URL)
		w.Write([]string{fileName, fmt.Sprintf("%d", v.Predict), fmt.Sprintf("%f", v.Score)})
	}

	correc = 1
	j = oneProjectPredict(pinfo, limit, skip, correc)
	for _, v := range j.Cells {
		if v.Predict != int(_type) {
			continue
		}
		filesname = append(filesname, v.URL)
		filestype = append(filestype, fmt.Sprintf("%d", v.Predict))
		filesscore = append(filesscore, v.Score)

		_, fileName := filepath.Split(v.URL)
		w.Write([]string{fileName, fmt.Sprintf("%d", v.Predict), fmt.Sprintf("%f", v.Score)})
	}

	w.Flush()
	fd.Close()
	filesname = append(filesname, csvname)
	filestype = append(filestype, "csv")

	//打包zip
	err = f.ZipCompressReviews(filesname, filestype, zipname)
	if err != nil {
		res.ResFailedStatus(c, e.Errors["ZipFailed"])
		return
	}

	filesize := f.GetFileSize(zipname)
	if filesize < 1 {
		res.ResFailedStatus(c, e.Errors["ZipFailed"])
		return
	}

	//下载
	contentDisposition := fmt.Sprintf("attachment; filename=%s", zipname)
	c.Writer.Header().Add("Content-Disposition", contentDisposition)
	c.Writer.Header().Add("Content-Type", "application/zip")
	c.Writer.Header().Add("Accept-Length", fmt.Sprintf("%d", filesize))
	c.Writer.Header().Add("Content-Length", fmt.Sprintf("%d", filesize))
	c.File(zipname)
	return
}
