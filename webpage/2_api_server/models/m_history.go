package models

import (
	"time"

	"github.com/jinzhu/gorm"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
)

//Operationlog 用户历史记录
type Operationlog struct {
	ID         int64     `json:"id"         gorm:"column:id; primary_key"` //ID
	UserID     int64     `json:"user_id"    gorm:"column:user_id"`         //用户ID
	UserName   string    `json:"name"       gorm:"-"`                      //用户名字
	UserEmail  string    `json:"email"      gorm:"-"`                      //用户邮箱
	UserMobile string    `json:"mobile"     gorm:"-"`                      //用户手机号
	Path       string    `json:"path"       gorm:"column:path"`            //访问路径
	Query      string    `json:"query"      gorm:"column:query"`           //query string
	Method     string    `json:"method"     gorm:"column:method"`          //请求方式
	IP         string    `json:"ip"         gorm:"column:ip"`              //客户端IP
	RegionID   string    `json:"region_id"  gorm:"column:region_id"`       //客户端IP所在地理位置的ID
	Region     Region    `json:"region"     gorm:"column:-"`               //客户端IP所在地理位置
	ISP        string    `json:"-"          gorm:"column:isp"`             //运营商
	Input      string    `json:"input"      gorm:"column:input"`           //post输入
	UA         string    `json:"ua"         gorm:"column:ua"`              //UserAgent
	Code       int       `json:"code"       gorm:"column:code"`            //请求的状态码
	BodySize   int       `json:"bodysize"   gorm:"column:bodysize"`        //bodysize
	Cost       int64     `json:"cost"       gorm:"column:cost"`            //请求花费了多少微秒
	Referer    string    `json:"referer"    gorm:"column:referer"`         //Referer
	CreatedAt  time.Time `json:"created_at" gorm:"column:created_at"`      //创建时间
}

// BeforeCreate insert之前的hook
func (opl *Operationlog) BeforeCreate(scope *gorm.Scope) error {
	if opl.CreatedAt.IsZero() {
		opl.CreatedAt = time.Now()
	}
	return nil
}

// AfterFind 把数据库里面存的字符串转成数组返回
func (opl *Operationlog) AfterFind(scope *gorm.Scope) error {
	region := Region{
		ID: opl.RegionID,
	}
	region.FindRegionbyID()
	opl.Region = region
	opl.Region.ISP = opl.ISP

	opl.UserName = "unknown"
	opl.UserEmail = "unknown"
	opl.UserMobile = "unknown"
	u, err := FinduserbyID(opl.UserID)
	if err == nil {
		opl.UserName = u.Name
		opl.UserEmail = u.Email
		opl.UserMobile = u.Mobile
	}
	return nil
}

// NewOperationlog 新建地区信息
func (opl *Operationlog) NewOperationlog() error {
	ret := db.Create(opl)
	if ret.Error != nil {
		return ret.Error
	}
	return nil
}

// ListOperationlog 依次列出浏览记录
func ListOperationlog(limit int, skip int, order int) (totalNum int64, c []Operationlog, e error) {
	var _o []Operationlog
	var total int64 = 0
	ret := db.Model(&Operationlog{}).Count(&total)

	orderStr := "id DESC"
	//order, default 1, 1倒序，0顺序
	if order == 0 {
		orderStr = "id ASC"
	}

	ret = db.Model(&Operationlog{}).Order(orderStr).Limit(limit).Offset(skip).Find(&_o)
	if ret.Error != nil {
		logger.Info(ret.Error)
	}
	return total, _o, ret.Error
}

// FindOperationByID 通过ID查找浏览记录
func FindOperationByID(id int64) (o Operationlog, e error) {
	var _o Operationlog
	ret := db.Model(&_o).Where("id=?", id).First(&_o)
	return _o, ret.Error
}
