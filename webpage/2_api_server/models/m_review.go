package models

import (
	"fmt"
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

// GetReviewByPRID 通过预测结果ID查找审核记录
func GetReviewByPRID(prid int64) (p Review, e error) {
	var _r Review
	ret := db.Model(&_r).Where("predictid=?", prid).First(&_r)
	return _r, ret.Error
}

// CreateReviews 新建待审核的细胞预测结果，一个很长的数组
func CreateReviews(reviews []*Review) (e error) {
	if len(reviews) < 1 {
		return nil
	}
	logger.Info.Println(len(reviews), time.Now())
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
				logger.Info.Println(ret.Error)
				logger.Info.Println(sql)
			}
			sql = sql1
		} else {
			sql += ","
		}
	}
	_db.Commit()
	logger.Info.Println(time.Now(), len(sql))
	return nil
}

// ListReviews 依次列出审核的细胞
func ListReviews(limit int, skip int, status int, userid int64) (totalNum int64, r []Review, e error) {
	var total int64 = 0
	var _r []Review
	ret := db.Model(&Review{}).Where("status=? AND vid=?", status, userid).Count(&total)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	ret = db.Model(&Review{}).Where("status=? AND vid=?", status, userid).Find(&_r)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return total, _r, ret.Error
}

// UpdateReview 更新审核信息
func UpdateReview(id int64, trueType int, userid int64) (e error) {
	_, err := GetReviewByPRID(id)
	if err != nil {
		return err
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
		logger.Info.Println(ret.Error)
	}
	return ret.Error
}
