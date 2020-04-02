package controllers

import (
	"fmt"
	"strconv"

	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
	f "github.com/paulxiong/cervical/webpage/2_api_server/functions"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	models "github.com/paulxiong/cervical/webpage/2_api_server/models"
	res "github.com/paulxiong/cervical/webpage/2_api_server/responses"
	u "github.com/paulxiong/cervical/webpage/2_api_server/utils"

	"github.com/gin-gonic/gin"
)

type _predictsByPID struct {
	ID           int64  `json:"id" `                         //ID
	PredictType  int    `json:"predict_type"  example:"100"` //预测的细胞类型,1到15是细胞类型, 50阴性 51阳性 100 未知, 200 不是细胞
	TrueType     int    `json:"true_type"     example:"100"` //医生标注的细胞类型 默认等于predict_type
	PredictScore int    `json:"predict_score" example:"100"` //预测得分 50表示50%
	X1           int    `json:"x1"            example:"100"` //在当前FOV的x1
	Y1           int    `json:"y1"            example:"100"` //在当前FOV的y1
	X2           int    `json:"x2"            example:"100"` //在当前FOV的x2
	Y2           int    `json:"y2"            example:"100"` //在当前FOV的y2
	CellPath     string `json:"cellpath"      example:"100"` //上述坐标切割出来的细胞
}

// PredictCount 用户审核的统计
type predictsByPID struct {
	Predicts []_predictsByPID `json:"predicts"` //预测结果
	Total    int64            `json:"total" `   //预测总数
}

// GetPredictsByPID 通过项目ID取出所有预测信息
// @Summary 通过项目ID取出所有预测信息
// @Description 通过项目ID取出所有预测信息
// @tags API1 医生检查细胞类型（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param pid query string false "pid, default 0, 所属项目的ID"
// @Param limit query string false "limit, default 1"
// @Param skip query string false "skip, default 0"
// @Param status query string false "status, default 1, 0 未审核 1 已审核 2 移除 3 管理员已确认 4 未审核+已审核"
// @Success 200 {object} controllers.predictsByPID
// @Router /api1/predictsbypid [get]
func GetPredictsByPID(c *gin.Context) {
	pidStr := c.DefaultQuery("pid", "0")
	limitStr := c.DefaultQuery("limit", "1")
	skipStr := c.DefaultQuery("skip", "0")
	statusStr := c.DefaultQuery("status", "1")
	pid, _ := strconv.ParseInt(pidStr, 10, 64)
	limit, _ := strconv.ParseInt(limitStr, 10, 64)
	skip, _ := strconv.ParseInt(skipStr, 10, 64)
	status, _ := strconv.ParseInt(statusStr, 10, 64)

	p, total, _ := models.GetPredictByPID(pid, int(status), 1000000, 0)

	_predicts := predictsByPID{}
	_predicts.Predicts = make([]_predictsByPID, 0)
	_predicts.Total = total
	for index, v := range p {
		if index < int(skip) || len(_predicts.Predicts) >= int(limit) {
			continue
		}
		//已经添加到细胞审核的就不需要重复添加了
		_r, err1 := models.GetReviewByPRID(v.ID)
		if err1 == nil || _r.ID > 0 {
			continue
		}
		_predicts.Predicts = append(_predicts.Predicts, _predictsByPID{
			ID:           v.ID,
			PredictType:  v.PredictType,
			TrueType:     v.TrueType,
			PredictScore: 0,
			X1:           v.X1,
			Y1:           v.Y1,
			X2:           v.X2,
			Y2:           v.Y2,
		})
	}

	res.ResSucceedStruct(c, _predicts)
	return
}

// GetPredictsByPIDSortByScore 通过项目ID和预测类型取出所有预测信息，按照得分排序
// @Summary 通过项目ID和预测类型取出所有预测信息，按照得分排序
// @Description 通过项目ID和预测类型取出所有预测信息，按照得分排序
// @tags API1 医生检查细胞类型（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param pid query string false "pid, default 0, 所属项目的ID"
// @Param limit query string false "limit, default 1"
// @Param skip query string false "skip, default 0"
// @Param status query string false "status, default 1, 0 未审核 1 已审核 2 移除 3 管理员已确认 4 未审核+已审核"
// @Param type query string false "type, default 50,　细胞预测类型"
// @Param order query string false "order, default 0, 0倒序，1顺序"
// @Success 200 {object} controllers.predictsByPID
// @Router /api1/predictsbypid2 [get]
func GetPredictsByPIDSortByScore(c *gin.Context) {
	pidStr := c.DefaultQuery("pid", "0")
	limitStr := c.DefaultQuery("limit", "1")
	skipStr := c.DefaultQuery("skip", "0")
	statusStr := c.DefaultQuery("status", "1")
	typeStr := c.DefaultQuery("type", "50")
	orderStr := c.DefaultQuery("order", "0")
	pid, _ := strconv.ParseInt(pidStr, 10, 64)
	limit, _ := strconv.ParseInt(limitStr, 10, 64)
	skip, _ := strconv.ParseInt(skipStr, 10, 64)
	status, _ := strconv.ParseInt(statusStr, 10, 64)
	_type, _ := strconv.ParseInt(typeStr, 10, 64)
	order, _ := strconv.ParseInt(orderStr, 10, 64)

	// 第3个参数limit给了500+limit，因为下面要过滤，不能保证最后返回的就是limit个数,skip也不在查找时候做，这里将来改进
	p, total, _ := models.GetPredictByPIDAndType(pid, int(status), int(limit+500), int(0), int(_type), int(order))
	logger.Info.Println(total, len(p))
	total2 := models.GetReviewCntByPID(pid, int(_type)) // 已经分配过的个数

	_predicts := predictsByPID{}
	_predicts.Predicts = make([]_predictsByPID, 0)
	_predicts.Total = total - total2
	if _predicts.Total < 1 {
		_predicts.Total = 0
		res.ResSucceedStruct(c, _predicts)
		return
	}
	index := 0
	for _, v := range p {
		if len(_predicts.Predicts) >= int(limit) {
			break
		}
		//已经添加到细胞审核的就不需要重复添加了
		_r, err1 := models.GetReviewByPRID(v.ID)
		if err1 == nil || _r.ID > 0 {
			continue
		}
		index = index + 1

		if index < int(skip+1) {
			continue
		}
		_predicts.Predicts = append(_predicts.Predicts, _predictsByPID{
			ID:           v.ID,
			PredictType:  v.PredictType,
			TrueType:     v.TrueType,
			PredictScore: v.PredictScore,
			CellPath:     v.CellPath,
			X1:           v.X1,
			Y1:           v.Y1,
			X2:           v.X2,
			Y2:           v.Y2,
		})
	}

	res.ResSucceedStruct(c, _predicts)
	return
}

type setreview struct {
	PredictsID []int64 `json:"predicts"`              //预测的ID的数组
	PID        int64   `json:"pid"       example:"7"` //所属项目的ID
	VID        int64   `json:"vid" `                  //指定给哪个用户去审核
}

// SetPredictsReview 把项目下的指定预测结果分配给指定的人员做审核
// @Summary 把项目下的指定预测结果分配给指定的人员做审核
// @Description 把项目下的指定预测结果分配给指定的人员做审核
// @tags API1 医生检查细胞类型（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param setreview body controllers.setreview true "把哪些预测指定给谁去审核"
// @Success 200 {string} json "{"ping": "ok",	"status": 200}"
// @Router /api1/setpredictsreview [post]
func SetPredictsReview(c *gin.Context) {
	sr := setreview{}
	err := c.ShouldBindJSON(&sr)
	if err != nil {
		res.ResFailedStatus(c, e.Errors["PostDataInvalied"])
		return
	}

	reviews := make([]*models.Review, 0)

	for _, v := range sr.PredictsID {
		//已经添加到细胞审核的就不需要重复添加了
		_r, err1 := models.GetReviewByPRID(v)
		if err1 == nil || _r.ID > 0 {
			continue
		}
		p, err1 := models.FindPredictbyID(v)
		if err1 != nil {
			continue
		}
		img, err2 := models.GetImageByID(p.ImgID)
		if err2 != nil {
			continue
		}

		//　拷贝FOV和细胞图到审核专门用的目录
		imgpath := f.Imgpath(img.Batchid, img.Medicalid, img.Imgpath, img.Type)
		imgnewpath := f.ReviewImgPath(imgpath)
		f.CopyFile(imgpath, imgnewpath)

		cellnewpath := f.ReviewCellPath(p.CellPath, imgnewpath)
		f.CopyFile(p.CellPath, cellnewpath)

		reviews = append(reviews, &models.Review{
			ID:           0,
			PRID:         p.ID,
			ImgID:        p.ImgID,
			PID:          p.PID,
			X1:           p.X1,
			Y1:           p.Y1,
			X2:           p.X2,
			Y2:           p.Y2,
			CellPath:     cellnewpath,
			ImgPath:      imgnewpath,
			W:            img.W,
			H:            img.H,
			PredictScore: p.PredictScore,
			PredictType:  p.PredictType,
			PredictP1n0:  p.PredictP1n0,
			TrueType:     p.TrueType,
			TrueP1n0:     p.TrueP1n0,
			VID:          sr.VID,
			Status:       0, //0 未审核 1 已审核 2 移除 3 管理员已确认
		})
	}
	models.CreateReviews(reviews)

	res.ResSucceedString(c, "ok")
	return
}

// reviewslist 用户审核的统计
type reviewslist struct {
	Reviews []models.Review `json:"reviews"` //预测结果
	Total   int64           `json:"total" `  //预测总数
}

// GetReviews 依次获得等待审核的细胞信息
// @Summary 依次获得等待审核的细胞信息
// @Description 依次获得等待审核的细胞信息
// @tags API1 医生检查细胞类型（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param limit query string false "limit, default 1"
// @Param skip query string false "skip, default 0"
// @Param owner query string false "owner, default 0, 0 只看属于自己的, 1 查看所有用户的"
// @Param status query string false "status, default 0, 0 未审核 1 已审核"
// @Success 200 {object} controllers.reviewslist
// @Router /api1/reviews [get]
func GetReviews(c *gin.Context) {
	limitStr := c.DefaultQuery("limit", "1")
	skipStr := c.DefaultQuery("skip", "0")
	statusStr := c.DefaultQuery("status", "0")
	ownerStr := c.DefaultQuery("owner", "0")
	limit, _ := strconv.ParseInt(limitStr, 10, 64)
	skip, _ := strconv.ParseInt(skipStr, 10, 64)
	status, _ := strconv.ParseInt(statusStr, 10, 64)
	owner, _ := strconv.ParseInt(ownerStr, 10, 64)

	usr, _ := models.GetUserFromContext(c)

	rl := reviewslist{}
	rl.Total, rl.Reviews, _ = models.ListReviews(int(limit), int(skip), int(status), usr.ID, int(owner))
	res.ResSucceedStruct(c, rl)
	return
}

// GetReviewsByPID 通过项目ID依次获得项目下等待审核的细胞信息
// @Summary 通过项目ID依次获得项目下等待审核的细胞信息
// @Description 通过项目ID依次获得项目下等待审核的细胞信息
// @tags API1 医生检查细胞类型（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param limit query string false "limit, default 1"
// @Param skip query string false "skip, default 0"
// @Param pid query string false "pid, default 0"
// @Param owner query string false "owner, default 0, 0 只看属于自己的, 1 查看所有用户的"
// @Param status query string false "status, default 0, 0 未审核 1 已审核 2 移除 3 管理员确认 4 全部(只在看自己的生效)"
// @Success 200 {object} controllers.reviewslist
// @Router /api1/reviewsbypid [get]
func GetReviewsByPID(c *gin.Context) {
	limitStr := c.DefaultQuery("limit", "1")
	skipStr := c.DefaultQuery("skip", "0")
	statusStr := c.DefaultQuery("status", "0")
	ownerStr := c.DefaultQuery("owner", "0")
	pidStr := c.DefaultQuery("pid", "0")
	limit, _ := strconv.ParseInt(limitStr, 10, 64)
	skip, _ := strconv.ParseInt(skipStr, 10, 64)
	status, _ := strconv.ParseInt(statusStr, 10, 64)
	owner, _ := strconv.ParseInt(ownerStr, 10, 64)
	pid, _ := strconv.ParseInt(pidStr, 10, 64)

	usr, _ := models.GetUserFromContext(c)

	rl := reviewslist{}
	rl.Total, rl.Reviews, _ = models.ListReviews2(int(pid), int(limit), int(skip), int(status), usr.ID, int(owner))
	res.ResSucceedStruct(c, rl)
	return
}

type reviewupdate struct {
	ID       int64 `json:"id"`        // 细胞Review的ID
	TrueType int   `json:"true_type"` // 审核细胞类型,1到15是细胞类型, 50 阴性 51 阳性 100 未知, 200 不是细胞
}

// UpdateReview 医生审核细胞信息写回数据库
// @Summary 医生审核信息写回数据库
// @Description 医生审核信息写回数据库
// @tags API1 医生检查细胞类型（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param predictupdate body controllers.reviewupdate true "医生审核信息"
// @Success 200 {string} json "{"ping": "ok",	"status": 200}"
// @Router /api1/review [post]
func UpdateReview(c *gin.Context) {
	ru := reviewupdate{}
	err := c.ShouldBindJSON(&ru)
	if err != nil {
		res.ResFailedStatus(c, e.Errors["PostDataInvalied"])
		return
	}

	usr, _ := models.GetUserFromContext(c)

	models.UpdateReview(ru.ID, ru.TrueType, usr.ID)
	res.ResSucceedString(c, "ok")
	return
}

type reviewsid struct {
	ReviewsID []int64 `json:"reviews"` //审核的ID数组
}

// DownloadReviews 下载选中的审核完成的细胞
// @Summary 下载选中的审核完成的细胞
// @Description 下载选中的审核完成的细胞
// @tags API1 医生检查细胞类型（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Success 200 {string} json "{"ping": "ok",	"status": 200}"
// @Router /api1/downloadreviews [post]
func DownloadReviews(c *gin.Context) {
	rids := reviewsid{}
	err := c.ShouldBindJSON(&rids)
	if err != nil {
		res.ResFailedStatus(c, e.Errors["PostDataInvalied"])
		return
	}

	// 创建目录作为临时存储文件使用
	dirname := u.GetRandomStringNum(6)
	zipname := fmt.Sprintf("%s.zip", dirname)

	filesname := make([]string, 0)
	filestype := make([]string, 0)
	for _, v := range rids.ReviewsID {
		_r, err1 := models.GetReviewByID(v)
		if err1 != nil {
			continue
		}
		ret, _ := f.PathExists(_r.CellPath)
		if ret != true {
			logger.Info.Printf("cell file not found %s", _r.CellPath)
			continue
		}
		filesname = append(filesname, _r.CellPath)
		filestype = append(filestype, fmt.Sprintf("%d", _r.TrueType))
	}

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
