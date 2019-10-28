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
	Status    int       `json:"status"     gorm:"column:status"`      //状态, 0初始化 1送去处理 2开始处理 3处理出错 4处理完成
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

// GetOneProjectToProcess 请求一个指定状态和类型的工程去处理
func GetOneProjectToProcess(status int) (p Project, e error) {
	_p := Project{}
	ret2 := db.Model(&_p).Where("status=?", status).First(&_p)
	if ret2.Error != nil {
		return _p, ret2.Error
	}
	return _p, ret2.Error
}

// UpdateProjectStatus 更新数据集的状态, 0初始化 1送去处理 2开始处理 3处理出错 4处理完成
func UpdateProjectStatus(pid int64, status int) (e error) {
	p := Project{}
	ret2 := db.Model(&p).Where("id=?", pid).First(&p)
	if ret2.Error != nil {
		return ret2.Error
	}

	p.Status = status
	/*
		if status == 2 {
			p.ProcessTime = time.Now()
		}
	*/

	ret := db.Model(&p).Where("id=?", pid).Updates(p)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return ret.Error
}

// ListProject 依次列出项目
func ListProject(limit int, skip int, order int) (totalNum int64, c []Project, e error) {
	//type, default 1, 0未知 1训练 2预测 10全部类型
	var _p []Project
	var total int64 = 0
	ret := db.Model(&Project{}).Count(&total)

	orderStr := "created_at DESC"
	//order, default 1, 1倒序，0顺序
	if order == 0 {
		orderStr = "created_at ASC"
	}

	ret = db.Model(&Project{}).Order(orderStr).Limit(limit).Offset(skip).Find(&_p)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return total, _p, ret.Error
}
