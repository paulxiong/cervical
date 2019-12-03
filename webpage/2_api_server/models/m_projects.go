package models

import (
	"time"

	"github.com/jinzhu/gorm"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
)

// Project 数据集的信息
type Project struct {
	ID              int64     `json:"id"         gorm:"column:id" example:"7"`         //ID
	DID             int64     `json:"did"        gorm:"column:did"`                    //数据集的id
	Desc            string    `json:"desc"       gorm:"column:description"`            //描述
	Dir             string    `json:"dir"        gorm:"column:dir"`                    //项目工作目录
	Status          int       `json:"status"     gorm:"column:status"`                 //状态, 0初始化 1送去处理 2开始处理 3处理出错 4处理完成
	Type            int       `json:"type"       gorm:"column:type"`                   //项目类型 0 未知 1 训练 2 预测
	StartTime       time.Time `json:"starttime"  gorm:"column:start_time"`             //开始处理数据时间
	EndTime         time.Time `json:"endtime"    gorm:"column:end_time"`               //处理数据结束时间
	Percent         int       `json:"percent"    gorm:"column:percent"`                //处理数据的进度
	ETA             int       `json:"ETA"        gorm:"column:ETA"`                    //预估还要多长时间结束,单位是秒
	UserName        string    `json:"username"   gorm:"-"`                             //创建者名字
	UserImg         string    `json:"userimg"    gorm:"-"`                             //创建者头像
	CreatedBy       int64     `json:"created_by" gorm:"column:created_by"`             //创建者
	CreatedAt       time.Time `json:"created_at" gorm:"column:created_at"`             //创建时间
	UpdatedAt       time.Time `json:"updated_at" gorm:"column:updated_at"`             //更新时间
	ParameterTime   int       `json:"parameter_time"   gorm:"column:parameter_time"`   //训练使用的最长时间
	ParameterResize int       `json:"parameter_resize" gorm:"column:parameter_resize"` //训练之前统一的尺寸
	ParameterMID    int       `json:"parameter_mid"    gorm:"column:parameter_mid"`    //预测使用的模型的id,只有预测时候需要
	ParameterMType  int       `json:"parameter_mtype"  gorm:"column:parameter_mtype"`  //模型的类型,不是前端传递,创建项目时候根据parameter_mid得到
	ParameterType   int       `json:"parameter_type"   gorm:"column:parameter_type"`   //预测方式,0没标注的图1有标注的图
}

// BeforeCreate insert 之前的hook
func (p *Project) BeforeCreate(scope *gorm.Scope) error {
	if p.CreatedAt.IsZero() {
		p.CreatedAt = time.Now()
	}
	if p.UpdatedAt.IsZero() {
		p.UpdatedAt = time.Now()
	}
	if p.StartTime.IsZero() {
		p.StartTime = time.Now()
	}
	if p.EndTime.IsZero() {
		p.EndTime = time.Now()
	}
	if p.Type == 2 {
		_mod, _ := FindModelInfoByID(p.ParameterMID)
		p.ParameterMType = _mod.Type
	} else if p.Type == 1 {
		p.ParameterMType = 5 //0未知 1UNET 2GAN 3SVM 4MASKRCNN 5AUTOKERAS 6 MALA
	}

	return nil
}

// AfterFind 把数据库里面存的字符串转成数组返回
func (p *Project) AfterFind(scope *gorm.Scope) error {
	if p.CreatedBy > 0 {
		u, _ := FinduserbyID(p.CreatedBy)
		p.UserName = u.Name
		p.UserImg = u.Image
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
func GetOneProjectToProcess(status int, _type int, mtype int) (p Project, e error) {
	_p := Project{}

	//预测
	if _type == 3 {
		ret2 := db.Model(&_p).Where("status=? AND type=? AND parameter_mtype=?", status, _type, mtype).First(&_p)
		if ret2.Error != nil {
			return _p, ret2.Error
		}
		return _p, ret2.Error
	}

	//训练
	ret2 := db.Model(&_p).Where("status=? AND type=?", status, _type).First(&_p)
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

	if status == 2 && p.Status == 1 {
		p.StartTime = time.Now()
	} else if status == 4 && p.Status == 2 {
		p.EndTime = time.Now()
	}
	p.Status = status

	ret := db.Model(&p).Where("id=?", pid).Updates(p)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return ret.Error
}

// UpdateProjectPercent 更新项目完成的百分比以及预估还要多长时间结束
func UpdateProjectPercent(pid int64, percent int, ETA int) (e error) {
	_p := Project{}
	ret2 := db.Model(&_p).Where("id=?", pid).First(&_p)
	if ret2.Error != nil {
		return ret2.Error
	}

	_p.Percent = percent
	_p.ETA = ETA

	ret := db.Model(&_p).Where("id=?", pid).Updates(map[string]interface{}{"process_percent": _p.Percent, "ETA": _p.ETA})
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return ret.Error
}

// ListProject 依次列出项目
func ListProject(limit int, skip int, order int, status int) (totalNum int64, c []Project, e error) {
	var _p []Project
	var total int64 = 0

	orderStr := "created_at DESC"
	//order, default 1, 1倒序，0顺序
	if order == 0 {
		orderStr = "created_at ASC"
	}

	// 0初始化 1送去处理 2开始处理 3处理出错 4处理完成 5 送去审核预测结果 6 预测结果审核完成 100 全部 101 送去审核以及核完成的预测结果
	if status == 100 {
		ret := db.Model(&Project{}).Count(&total)
		ret = db.Model(&Project{}).Order(orderStr).Limit(limit).Offset(skip).Find(&_p)
		if ret.Error != nil {
			logger.Info.Println(ret.Error)
		}
		return total, _p, ret.Error
	} else if status == 101 {
		ret := db.Model(&Project{}).Where("status=? OR status=?", 5, 6).Count(&total)
		ret = db.Model(&Project{}).Where("status=? OR status=?", 5, 6).Order(orderStr).Limit(limit).Offset(skip).Find(&_p)
		if ret.Error != nil {
			logger.Info.Println(ret.Error)
		}
		return total, _p, ret.Error
	}

	ret := db.Model(&Project{}).Where("status=?", status).Count(&total)
	ret = db.Model(&Project{}).Where("status=?", status).Order(orderStr).Limit(limit).Offset(skip).Find(&_p)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return total, _p, ret.Error
}

// GetOneProjectByID 通过ID查找项目
func GetOneProjectByID(id int) (p Project, e error) {
	_p := Project{}
	ret2 := db.Model(&_p).Where("id=?", id).First(&_p)
	if ret2.Error != nil {
		return _p, ret2.Error
	}
	return _p, ret2.Error
}
