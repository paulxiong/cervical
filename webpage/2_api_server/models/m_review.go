package models

import (
	"fmt"
	"log"
	"time"

	"github.com/jinzhu/gorm"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
)

// Review 需要医生帮忙确认单个细胞的类型,和Predict结构完全一致
type Review struct {
	ID           int64     `json:"id"            gorm:"column:id; primary_key" example:"7"`   //预测信息ID
	PRID         int64     `json:"predictid"     gorm:"column:predictid"       example:"7"`   //预测信息ID
	ImgID        int64     `json:"imgid"         gorm:"column:imgid"           example:"7"`   //所属图片的ID
	PID          int64     `json:"pid"           gorm:"column:pid"             example:"7"`   //所属项目的ID
	X1           int       `json:"x1"            gorm:"column:x1"              example:"100"` //左上角X坐标 单位是像素
	Y1           int       `json:"y1"            gorm:"column:y1"              example:"100"` //左上角Y坐标 单位是像素
	X2           int       `json:"x2"            gorm:"column:x2"              example:"100"` //右下角X坐标 单位是像素
	Y2           int       `json:"y2"            gorm:"column:y2"              example:"100"` //预右下角Y坐标 单位是像素
	CellPath     string    `json:"cellpath"      gorm:"column:cellpath"        example:"100"` //上述坐标切割出来的细胞
	ImgPath      string    `json:"imgpath"       gorm:"column:imgpath"         example:"100"` //原图路径
	W            int       `json:"w"             gorm:"column:w"`                             //原图的宽
	H            int       `json:"h"             gorm:"column:h"`                             //原图的高
	PredictScore int       `json:"predict_score" gorm:"column:predict_score"   example:"100"` //预测得分 50表示50%
	PredictType  int       `json:"predict_type"  gorm:"column:predict_type"    example:"100"` //预测的细胞类型,1到15是细胞类型, 50阴性 51阳性 100 未知, 200 不是细胞
	PredictP1n0  int       `json:"predict_p1n0"  gorm:"column:predict_p1n0"    example:"100"` //预测阴/阳性
	TrueType     int       `json:"true_type"     gorm:"column:true_type"       example:"100"` //医生标注的细胞类型 默认等于predict_type
	TrueP1n0     int       `json:"true_p1n0"     gorm:"column:true_p1n0"       example:"100"` //医生标注的阴/阳性 默认等于predict_p1n0
	VID          int64     `json:"vid"           gorm:"column:vid"             example:"7"`   //谁去做审核(verify)的用户ID
	Status       int       `json:"status"        gorm:"column:status"          example:"100"` //状态 0 未审核 1 已审核 2 移除 3 管理员确认
	CreatedBy    int64     `json:"created_by"    gorm:"column:created_by"`                    //创建者
	CreatedAt    time.Time `json:"created_at"    gorm:"column:created_at"`                    //创建时间
	UserName     string    `json:"username"      gorm:"-"`                                    //创建者名字
	UserImg      string    `json:"userimg"       gorm:"-"`                                    //创建者头像
	UpdatedAt    time.Time `json:"updated_at"    gorm:"column:updated_at"`                    //更新时间
}

// BeforeCreate insert 之前的hook
func (r *Review) BeforeCreate(scope *gorm.Scope) error {
	if r.CreatedAt.IsZero() {
		r.CreatedAt = time.Now()
	}
	if r.UpdatedAt.IsZero() {
		r.UpdatedAt = time.Now()
	}
	return nil
}

// AfterFind 添加审核账号信息
func (r *Review) AfterFind(scope *gorm.Scope) error {
	if r.VID > 0 {
		u, _ := FinduserbyID(r.VID)
		r.UserName = u.Name
		r.UserImg = u.Image
	}
	return nil
}

// GetReviewByPRID 通过预测结果ID查找审核记录
func GetReviewByPRID(prid int64) (p Review, e error) {
	var _r Review
	ret := db.Model(&_r).Where("predictid=?", prid).First(&_r)
	return _r, ret.Error
}

// GetReviewCntByPID1 通过项目ID查找审核记录条数
func GetReviewCntByPID1(pid int64) int64 {
	var total int64
	db.Model(&Review{}).Where("pid=?", pid).Count(&total)
	return total
}

// GetReviewCntByPID 通过项目ID查找审核记录条数
func GetReviewCntByPID(pid int64, _type int) int64 {
	var total int64
	db.Model(&Review{}).Where("pid=? AND predict_type=?", pid, _type).Count(&total)
	return total
}

// GetReviewByID 通过ID查找审核信息
func GetReviewByID(id int64) (r Review, e error) {
	var _r Review
	ret := db.Model(&_r).Where("id = ?", id).First(&_r)
	if ret.Error != nil {
		logger.Info(ret.Error)
	}
	return _r, ret.Error
}

// CreateReviews 新建待审核的细胞预测结果，一个很长的数组
func CreateReviews(reviews []*Review) (e error) {
	if len(reviews) < 1 {
		return nil
	}
	logger.Info(len(reviews), time.Now())
	sql1 := "INSERT  INTO `c_review` (`predictid`, `imgid`,`pid`,`x1`,`y1`,`x2`,`y2`,`cellpath`,`imgpath`,`w`,`h`,`predict_score`,`predict_type`,`predict_p1n0`,`true_type`,`true_p1n0`,`vid`,`status`) VALUES "
	sql := sql1
	// 新增预测结果
	_db := db.Begin()
	for index, v := range reviews {
		sql += fmt.Sprintf("(%d,%d,%d,%d,%d,%d,%d,\"%s\",\"%s\",%d,%d,%d,%d,%d,%d,%d,%d,%d)",
			v.PRID, v.ImgID, v.PID, v.X1, v.Y1, v.X2, v.Y2, v.CellPath, v.ImgPath, v.W, v.H, v.PredictScore,
			v.PredictType, v.PredictP1n0, v.TrueType, v.TrueP1n0, v.VID, v.Status)

		if index > 0 && index%5000 == 0 || index == len(reviews)-1 {
			sql += ";"
			ret := _db.Exec(sql)
			if ret.Error != nil {
				logger.Info(ret.Error)
				logger.Info(sql)
			}
			sql = sql1
		} else {
			sql += ","
		}
	}
	_db.Commit()
	logger.Info(time.Now(), len(sql))
	return nil
}

// ListReviews 依次列出审核的细胞
func ListReviews(limit int, skip int, status int, userid int64, owner int) (totalNum int64, r []Review, e error) {
	var total int64 = 0
	var _r []Review
	// 0 只看属于自己的, 1 查看所有用户的
	if owner == 0 {
		ret := db.Model(&Review{}).Where("status=? AND vid=?", status, userid).Count(&total)
		if ret.Error != nil {
			logger.Info(ret.Error)
		}
		ret = db.Model(&Review{}).Where("status=? AND vid=?", status, userid).Limit(limit).Offset(skip).Find(&_r)
		if ret.Error != nil {
			logger.Info(ret.Error)
		}
		return total, _r, ret.Error
	}

	ret := db.Model(&Review{}).Where("status=?", status).Count(&total)
	if ret.Error != nil {
		logger.Info(ret.Error)
	}
	ret = db.Model(&Review{}).Where("status=?", status).Limit(limit).Offset(skip).Find(&_r)
	if ret.Error != nil {
		logger.Info(ret.Error)
	}
	return total, _r, ret.Error
}

// ListReviews2 依次列出审核的细胞
func ListReviews2(pid int, limit int, skip int, status int, userid int64, owner int) (totalNum int64, r []Review, e error) {
	var total int64 = 0
	var _r []Review
	// 0 只看属于自己的, 1 查看所有用户的
	if owner == 0 {
		//status 0 未审核 1 已审核 2 移除 3 管理员确认 4 全部
		if status == 4 {
			ret := db.Model(&Review{}).Where("pid=? AND vid=?", pid, userid).Count(&total)
			if ret.Error != nil {
				logger.Info(ret.Error)
			}
			ret = db.Model(&Review{}).Where("pid=? AND vid=?", pid, userid).Limit(limit).Offset(skip).Find(&_r)
			if ret.Error != nil {
				logger.Info(ret.Error)
			}
			return total, _r, ret.Error
		}
		ret := db.Model(&Review{}).Where("status=? AND pid=? AND vid=?", status, pid, userid).Count(&total)
		if ret.Error != nil {
			logger.Info(ret.Error)
		}
		ret = db.Model(&Review{}).Where("status=? AND pid=? AND vid=?", status, pid, userid).Limit(limit).Offset(skip).Find(&_r)
		if ret.Error != nil {
			logger.Info(ret.Error)
		}
		return total, _r, ret.Error
	}

	ret := db.Model(&Review{}).Where("status=? AND pid=?", status, pid).Count(&total)
	if ret.Error != nil {
		logger.Info(ret.Error)
	}
	ret = db.Model(&Review{}).Where("status=? AND pid=?", status, pid).Limit(limit).Offset(skip).Find(&_r)
	if ret.Error != nil {
		logger.Info(ret.Error)
	}
	return total, _r, ret.Error
}

// UpdateReview 更新审核信息
func UpdateReview(id int64, trueType int, userid int64) (Review, error) {
	r, err := GetReviewByID(id)
	if err != nil {
		return r, err
	}

	// 审核细胞类型,1到15是细胞类型, 50 阴性 51 阳性 100 未知, 200 不是细胞
	// TODO: 类型计算
	var trueP1n0 int = 0

	// 状态 0 未审核 1 已审核 2 移除 3 管理员确认
	var status int = 1

	ret := db.Model(&Review{}).Where("id=?", id).Updates(map[string]interface{}{
		"true_type": trueType,
		"true_p1n0": trueP1n0,
		"status":    status,
		"vid":       userid})
	if ret.Error != nil {
		logger.Info(ret.Error)
	}
	return r, ret.Error
}

// GetProjectsByVID 查找某个用户能看到的所有需要审核的项目
func GetProjectsByVID(vid int64, limit int64, skip int64) ([]Project, int64) {
	type res struct {
		Pid int64
	}
	selector := fmt.Sprintf("select pid from c_review where vid=%d group by pid limit %d offset %d;", vid, limit, skip)
	ress := make([]res, 0)
	ret := db.Raw(selector).Scan(&ress)
	if ret.Error != nil {
		log.Println(ret.Error)
	}

	type res2 struct {
		Total int64
	}
	selector2 := fmt.Sprintf("SELECT count(1) as total from (select count(1) from c_review where vid=%d group by pid) xxx;", vid)
	ress2 := res2{}
	ret2 := db.Raw(selector2).Scan(&ress2)
	if ret2.Error != nil {
		log.Println(ret2.Error)
	}

	_ps := make([]Project, 0)
	for _, v := range ress {
		_p := Project{}
		ret2 := db.Model(&_p).Where("id=?", v.Pid).First(&_p)
		if ret2.Error == nil {
			_ps = append(_ps, _p)
		}
	}
	return _ps, ress2.Total
}
