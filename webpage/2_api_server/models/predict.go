package models

import (
	"time"

	"github.com/jinzhu/gorm"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
)

// Predict 单个细胞的预测结果
type Predict struct {
	ID           int64     `json:"id"            gorm:"column:id; primary_key" example:"7"`   //预测信息ID
	ImgID        int64     `json:"imgid"         gorm:"column:imgid"           example:"7"`   //所属图片的ID
	PID          int64     `json:"pid"           gorm:"column:pid"             example:"7"`   //所属项目的ID
	X1           int       `json:"x1"            gorm:"column:x1"              example:"100"` //左上角X坐标 单位是像素
	Y1           int       `json:"y1"            gorm:"column:y1"              example:"100"` //左上角Y坐标 单位是像素
	X2           int       `json:"x2"            gorm:"column:x2"              example:"100"` //右下角X坐标 单位是像素
	Y2           int       `json:"y2"            gorm:"column:y2"              example:"100"` //预右下角Y坐标 单位是像素
	CellPath     string    `json:"cellpath"      gorm:"column:cellpath"        example:"100"` //上述坐标切割出来的细胞
	PredictScore int       `json:"predict_score" gorm:"column:predict_score"   example:"100"` //预测得分 50表示50%
	PredictType  int       `json:"predict_type"  gorm:"column:predict_type"    example:"100"` //预测的细胞类型
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
func (p *Predict) BeforeCreate(scope *gorm.Scope) error {
	if p.CreatedAt.IsZero() {
		p.CreatedAt = time.Now()
	}
	if p.UpdatedAt.IsZero() {
		p.UpdatedAt = time.Now()
	}
	return nil
}

// FindPredictbyImgIDPIDXY 查找细胞预测结果是否存在
func (p *Predict) FindPredictbyImgIDPIDXY() (*Predict, error) {
	_p := &Predict{}
	ret := db.Model(_p).Where("pid=? AND imgid=? AND x1=? AND x2=? AND y1=? AND y2=?", p.PID, p.ImgID, p.X1, p.X2, p.Y1, p.Y2).First(_p)
	if ret.Error != nil {
		return _p, ret.Error
	}
	return _p, nil
}

// CreatePredict 新建一个细胞预测结果
func (p *Predict) CreatePredict() (e error) {
	p.ID = 0

	_, err := p.FindPredictbyImgIDPIDXY()
	if err == nil {
		return err
	}

	ret := db.Model(p).Save(&p)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return ret.Error
}

// ListPredict 通过图片ID查找预测
func ListPredict(limit int, skip int, imgid int) (totalNum int64, p []Predict, e error) {
	var _p []Predict
	var total int64 = 0

	db.Model(&Predict{}).Where("imgid=?", imgid).Count(&total)
	ret := db.Model(&Predict{}).Where("imgid=?", imgid).Limit(limit).Offset(skip).Find(&_p)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return total, _p, ret.Error
}
