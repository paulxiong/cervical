package models

import (
	"time"

	"github.com/gin-gonic/gin"
	"github.com/jinzhu/gorm"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
)

//Errorlog 错误日志
type Errorlog struct {
	ID           int64        `json:"id"            gorm:"column:id; primary_key" example:"1"`            //ID
	Type         int          `json:"type"          gorm:"column:type"            example:"0"`            //类型, 0前端
	Opid         int64        `json:"opid"          gorm:"column:opid"            example:"12"`           //访客记录ID
	Operationlog Operationlog `json:"operationlog"  gorm:"-"`                                             //访客记录
	Errlog       string       `json:"errlog"        gorm:"column:errlog"          example:"error string"` //错误内容
	CreatedBy    int64        `json:"created_by"    gorm:"column:created_by"`                             //创建者
	CreatedAt    time.Time    `json:"created_time"  gorm:"column:created_at"`
	UpdatedAt    time.Time    `json:"-"             gorm:"column:updated_at"`
}

// BeforeCreate insert之前的hook
func (err *Errorlog) BeforeCreate(scope *gorm.Scope) error {
	if err.CreatedAt.IsZero() {
		err.CreatedAt = time.Now()
	}
	if err.UpdatedAt.IsZero() {
		err.UpdatedAt = time.Now()
	}
	return nil
}

// AfterFind 查出opid的内容
func (err *Errorlog) AfterFind(scope *gorm.Scope) error {
	err.Operationlog, _ = FindOperationByID(err.Opid)
	return nil
}

// NewErrorLog 新建错误日志
func (err *Errorlog) NewErrorLog() error {
	ret := db.Model(err).Create(err)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
		return ret.Error
	}
	return nil
}

// ErrorlogLists 按顺序列出所有错误日志
func ErrorlogLists(limit int, skip int, order int) (el []Errorlog, t int, err error) {
	var _el []Errorlog
	var total int = 0
	db.Model(&Errorlog{}).Count(&total)

	orderStr := "created_at DESC"
	if order == 0 { //order, default 1, 1倒序，0顺序
		orderStr = "created_at ASC"
	}
	ret := db.Model(&Errorlog{}).Order(orderStr).Limit(limit).Offset(skip).Find(&_el)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return _el, total, ret.Error
}

// UpdateErrorlog 更新错误日志的opid
func UpdateErrorlog(elid int64, opid int64) (err error) {
	if elid == 0 || opid == 0 {
		return nil
	}
	ret := db.Model(&Errorlog{}).Where("id=?", elid).Updates(map[string]interface{}{"opid": opid})
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return ret.Error
}

// GetErrorlogIDFromContext 从请求上下文获得错误日志的ID
func GetErrorlogIDFromContext(c *gin.Context) (int64, bool) {
	_elid, exists := c.Get("elid")
	if exists == true && _elid != nil {
		elid := _elid.(int64)
		return elid, exists
	}
	return 0, exists
}

// SaveErrorlogIDtoContext 把错误日志的ID存到请求上下文
func SaveErrorlogIDtoContext(c *gin.Context, elid int64) {
	c.Set("elid", elid)
}
