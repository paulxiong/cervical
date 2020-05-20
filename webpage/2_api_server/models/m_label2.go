package models

import (
	"time"

	"github.com/jinzhu/gorm"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
)

// Label2 标注的信息
type Label2 struct {
	ID        string    `json:"id"            gorm:"column:id; primary_key" example:"1"`   //标注信息 时间辍+项目ID+数据集ID+用户ID+随机字符串
	PreID     int64     `json:"preid"         gorm:"column:preid"           example:"2"`   //预测的ID 人工标注的默认是0
	PID       int64     `json:"pid"           gorm:"column:pid"             example:"2"`   //项目ID
	DID       int64     `json:"did"           gorm:"column:did"             example:"2"`   //数据集ID
	TypeID    int       `json:"typeid"        gorm:"column:typeid"          example:"2"`   //类型的ID
	X1        int       `json:"x1"            gorm:"column:x1"              example:"0"`   //左上角X
	Y1        int       `json:"y1"            gorm:"column:y1"              example:"0"`   //左上角Y
	X2        int       `json:"x2"            gorm:"column:x2"              example:"320"` //右下角X
	Y2        int       `json:"y2"            gorm:"column:y2"              example:"320"` //右下角Y
	Status    int       `json:"status"        gorm:"column:status"          example:"1"`   //状态, 0 未审核 1 已审核 2 移除
	CreatedBy int64     `json:"created_by"    gorm:"column:created_by"`                    //创建者
	CreatedAt time.Time `json:"created_at"    gorm:"column:created_at"`
	UpdatedAt time.Time `json:"updated_at"    gorm:"column:updated_at"`
}

/*
alter table c_label2 add status INT NOT NULL  DEFAULT 0 COMMENT '状态 0 未审核 1 已审核 2 移除 10 审核+未审核的' after y2;
*/

// BeforeCreate insert之前的hook
func (l *Label2) BeforeCreate(scope *gorm.Scope) error {
	if l.CreatedAt.IsZero() {
		l.CreatedAt = time.Now()
	}
	if l.UpdatedAt.IsZero() {
		l.UpdatedAt = time.Now()
	}
	return nil
}

// InsertLabel2 新建标注信息
func (l *Label2) InsertLabel2() (e error) {
	_l := Label2{}
	l.Status = 0
	ret := db.Model(l).Where("id=?", l.ID).First(&_l)
	if ret.Error == nil && _l.X2 > 0 {
		return nil
	}
	if l.PreID > 0 {
		ret = db.Model(l).Where("preid=?", l.PreID).First(&_l)
		if ret.Error == nil && _l.X2 > 0 {
			return nil
		}
	}

	ret2 := db.Model(l).Save(l)
	if ret2.Error != nil {
		logger.Info(ret2.Error)
	}
	return ret2.Error
}

// RemoveLabel2 删除标注信息
func (l *Label2) RemoveLabel2() (e error) {
	ret2 := db.Model(l).Where("id=?", l.ID).Updates(map[string]interface{}{"status": 2})
	if ret2.Error != nil {
		logger.Info(ret2.Error)
	}

	return ret2.Error
}

// UpdateLabel2 更新标注信息
func (l *Label2) UpdateLabel2() (e error) {
	ret2 := db.Model(l).Where("id=?", l.ID).Updates(map[string]interface{}{"x1": l.X1, "y1": l.Y1, "x2": l.X2, "y2": l.Y2, "typeid": l.TypeID, "status": 1})
	if ret2.Error != nil {
		logger.Info(ret2.Error)
	}

	return ret2.Error
}

// ListLabel2 依次列出标注信息
func ListLabel2(limit int, skip int) (totalNum int64, l []Label2, e error) {
	var _l []Label2
	var total int64 = 0

	db.Model(&Label2{}).Count(&total)
	ret := db.Model(&Label2{}).Limit(limit).Offset(skip).Find(&_l)
	if ret.Error != nil {
		logger.Info(ret.Error)
	}
	return total, _l, ret.Error
}

// ListLabel2ByPid 依次列出标注信息
func ListLabel2ByPid(limit int, skip int, pid int) (totalNum int64, l []Label2, e error) {
	var _l []Label2
	var total int64 = 0

	db.Model(&Label2{}).Where("pid = ?", pid).Count(&total)
	ret := db.Model(&Label2{}).Where("pid = ?", pid).Limit(limit).Offset(skip).Find(&_l)
	if ret.Error != nil {
		logger.Info(ret.Error)
	}
	return total, _l, ret.Error
}

// ListLabel2ByType 通过标注细胞类型列出标注信息
func ListLabel2ByType(limit int, skip int, t int) (totalNum int64, l []Label2, e error) {
	var _l []Label2
	var total int64 = 0

	db.Model(&Label2{}).Where("typeid = ?", t).Count(&total)
	ret := db.Model(&Label2{}).Where("typeid = ?", t).Limit(limit).Offset(skip).Find(&_l)
	if ret.Error != nil {
		logger.Info(ret.Error)
	}
	return total, _l, ret.Error
}
