package models

import (
	"time"

	"github.com/jinzhu/gorm"

	u "github.com/paulxiong/cervical/webpage/2_api_server/utils"
)

//Region 城市信息
type Region struct {
	ID        string    `json:"id"         gorm:"column:id; primary_key"` //记录ID
	CityID    int64     `json:"cityid"     gorm:"column:cityid"`          //city唯一对应的ID
	Country   string    `json:"country"    gorm:"column:country"`         //国家
	Region    string    `json:"region"     gorm:"column:region"`          //地区
	Province  string    `json:"province"   gorm:"column:province"`        //省/州
	City      string    `json:"city"       gorm:"column:city"`            //城市
	ISP       string    `json:"isp"        gorm:"column:isp"`             //运营商
	CreatedAt time.Time `json:"-" gorm:"column:created_at"`               //创建时间
}

// BeforeCreate insert之前的hook
func (r *Region) BeforeCreate(scope *gorm.Scope) error {
	if r.CreatedAt.IsZero() {
		r.CreatedAt = time.Now()
	}
	return nil
}

// NewRegion 新建地区信息
func (r *Region) NewRegion() error {
	r.MD5RegionID()
	ret := db.FirstOrCreate(r, Region{ID: r.ID})
	if ret.Error != nil {
		return ret.Error
	}
	return nil
}

// FindRegionbyID 通过用户ID查找用户
func (r *Region) FindRegionbyID() (*Region, error) {
	ret := db.Model(r).Where("id=?", r.ID).First(r)
	if ret.Error != nil {
		return r, ret.Error
	}
	return r, nil
}

// MD5RegionID 把Region的所有字符串加起来求MD5当做ID
func (r *Region) MD5RegionID() (*Region, error) {
	allstr := r.Country + r.Region + r.Province + r.City + r.ISP
	id := u.MD5(allstr)
	r.ID = id
	return r, nil
}
