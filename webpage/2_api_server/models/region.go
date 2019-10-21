package models

import (
	"time"

	"github.com/jinzhu/gorm"
)

//Region 城市信息
type Region struct {
	ID        int64     `json:"id"         gorm:"column:id"`       //city唯一对应的ID
	Country   string    `json:"country"    gorm:"column:country"`  //国家
	Region    string    `json:"region"     gorm:"column:region"`   //地区
	Province  string    `json:"province"   gorm:"column:province"` //省/州
	City      string    `json:"city"       gorm:"column:city"`     //城市
	ISP       string    `json:"isp"        gorm:"column:-"`        //运营商
	CreatedAt time.Time `json:"-" gorm:"column:created_at"`        //创建时间
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
	_, err := r.FindRegionbyID()
	if err == nil {
		return nil
	}

	ret := db.Create(r)
	if ret.Error != nil {
		return ret.Error
	}
	return nil
}

// FindRegionbyID 通过用户ID查找用户
func (r *Region) FindRegionbyID() (*Region, error) {
	ret := db.First(r, r.ID)
	if ret.Error != nil {
		return r, ret.Error
	}
	return r, nil
}
