package models

import (
	"time"

	"github.com/jinzhu/gorm"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
)

// Project 数据集的信息
type Project struct {
	ID        int64     `json:"id"         gorm:"column:id"`          //ID
	DID       int64     `json:"did"        gorm:"column:did"`         //数据集的id
	Desc      string    `json:"desc"       gorm:"column:description"` //项目工作目录
	Dir       string    `json:"dir"        gorm:"column:dir"`         //描述
	Status    int       `json:"status"     gorm:"column:status"`      //状态
	Type      int       `json:"type"       gorm:"column:type"`        //项目类型 0 未知 1 训练 2 预测
	CreatedBy int64     `json:"created_by" gorm:"column:created_by"`  //创建者
	CreatedAt time.Time `json:"created_at" gorm:"column:created_at"`  //创建时间
	UpdatedAt time.Time `json:"updated_at" gorm:"column:updated_at"`  //更新时间
}

// BeforeCreate insert 之前的hook
func (p *Project) BeforeCreate(scope *gorm.Scope) error {
	if p.CreatedAt.IsZero() {
		p.CreatedAt = time.Now()
	}
	if p.UpdatedAt.IsZero() {
		p.UpdatedAt = time.Now()
	}
	return nil
}

// CreateProject 新建一个项目
func (p *Project) CreateProject() (e error) {
	p.ID = 0
	ret := db.Model(p).Save(&p)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}

	ret2 := db.Model(p).Where("dir=?", p.Dir).First(&p)
	if ret2.Error != nil {
		logger.Info.Println(ret2.Error)
	}
	return ret2.Error
}
