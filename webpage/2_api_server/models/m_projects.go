package models

import (
	"encoding/json"
	"time"

	"github.com/jinzhu/gorm"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	"github.com/pkg/errors"
)

// ProjectCellstype 预测的细胞的个数统计
type ProjectCellstype struct {
	Type  int `json:"type"      example:"1"`  //细胞类型
	Total int `json:"total"     example:"35"` //细胞个数
}

//cellstype2String string数组转字符串
func cellstype2String(arr *[]ProjectCellstype) (string, error) {
	bs, err := json.Marshal(arr)
	return string(bs), errors.WithStack(err)
}

//string2cellstype 字符串转string数组
func string2cellstype(str string) ([]ProjectCellstype, error) {
	var arr []ProjectCellstype
	err := json.Unmarshal([]byte(str), &arr)
	return arr, errors.WithStack(err)
}

// Project 数据集的信息
type Project struct {
	ID              int64              `json:"id"         gorm:"column:id" example:"7"`         //ID
	DID             int64              `json:"did"        gorm:"column:did"`                    //数据集的id
	Desc            string             `json:"desc"       gorm:"column:description"`            //描述
	Dir             string             `json:"dir"        gorm:"column:dir"`                    //项目工作目录
	Status          int                `json:"status"     gorm:"column:status"`                 //状态, 0初始化 1送去处理 2开始处理 3处理出错 4处理完成
	Type            int                `json:"type"       gorm:"column:type"`                   //项目类型 0 未知 1 训练 2 预测
	StartTime       time.Time          `json:"starttime"  gorm:"column:start_time"`             //开始处理数据时间
	EndTime         time.Time          `json:"endtime"    gorm:"column:end_time"`               //处理数据结束时间
	Percent         int                `json:"percent"    gorm:"column:percent"`                //处理数据的进度
	ETA             int                `json:"ETA"        gorm:"column:ETA"`                    //预估还要多长时间结束,单位是秒
	UserName        string             `json:"username"   gorm:"-"`                             //创建者名字
	UserImg         string             `json:"userimg"    gorm:"-"`                             //创建者头像
	CreatedBy       int64              `json:"created_by" gorm:"column:created_by"`             //创建者
	CreatedAt       time.Time          `json:"created_at" gorm:"column:created_at"`             //创建时间
	UpdatedAt       time.Time          `json:"updated_at" gorm:"column:updated_at"`             //更新时间
	ParameterTime   int                `json:"parameter_time"   gorm:"column:parameter_time"`   //训练使用的最长时间
	ParameterResize int                `json:"parameter_resize" gorm:"column:parameter_resize"` //训练之前统一的尺寸
	ParameterMID    int                `json:"parameter_mid"    gorm:"column:parameter_mid"`    //预测使用的模型的id,只有预测时候需要
	ParameterMType  int                `json:"parameter_mtype"  gorm:"column:parameter_mtype"`  //模型的类型,不是前端传递,创建项目时候根据parameter_mid得到
	ParameterType   int                `json:"parameter_type"   gorm:"column:parameter_type"`   //预测方式,0没标注的图1有标注的图
	CellsType1      string             `json:"-"                gorm:"column:cellstype"`        //预测完之后的细胞类型统计
	CellsType2      []ProjectCellstype `json:"cellstype"        gorm:"-"`                       //预测完之后的细胞类型统计
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
	p.CellsType1 = "[]"
	return nil
}

// AfterFind 把数据库里面存的字符串转成数组返回
func (p *Project) AfterFind(scope *gorm.Scope) error {
	if p.CreatedBy > 0 {
		u, _ := FinduserbyID(p.CreatedBy)
		p.UserName = u.Name
		p.UserImg = u.Image
	}
	if p.CellsType1 != "" {
		cells, err := string2cellstype(p.CellsType1)
		if err == nil {
			p.CellsType2 = cells
		}
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

// UpdateProjectStatus 更新项目的状态, 0初始化 1送去处理 2开始处理 3处理出错 4处理完成 5 送去审核预测结果 6 预测结果审核完成
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

	ret := db.Model(&p).Where("id=?", pid).Updates(map[string]interface{}{
		"starttime": p.StartTime,
		"endtime":   p.EndTime,
		"status":    p.Status})
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return ret.Error
}

// UpdateProjectCellsType 更新项目的预测细胞类型统计
func UpdateProjectCellsType(pid int64, cellstype []ProjectCellstype) (e error) {
	cellstypestring, err := cellstype2String(&cellstype)
	if err != nil {
		return err
	}

	ret := db.Model(&Project{}).Where("id=?", pid).Updates(map[string]interface{}{"cellstype": cellstypestring})
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

// RemoveProjectByID 删除项目
func RemoveProjectByID(pid int64) (e error) {
	// 删除当前项目的所有预测结果
	ret := db.Where("id=?", pid).Delete(Project{})
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return ret.Error
}

// Result 预测结果信息统计，目前只有内部测试使用
type Result struct {
	ID        int64     `json:"id"         gorm:"column:id; primary_key" example:"1"`           //ID
	DID       int64     `json:"did"        gorm:"column:did"             example:"2"`           //数据集的id
	PID       int64     `json:"pid"        gorm:"column:pid"             example:"3"`           //项目的id
	Desc      string    `json:"desc"       gorm:"column:description"     example:"description"` //项目的描述
	PCnt      int       `json:"pcnt"       gorm:"column:pcnt"            example:"100"`         //阳性细胞个数
	NCnt      int       `json:"ncnt"       gorm:"column:ncnt"            example:"100"`         //阴性细胞个数
	UCnt      int       `json:"ucnt"       gorm:"column:ucnt"            example:"100"`         //不是细胞个数
	FOVCnt    int       `json:"fovcnt"     gorm:"column:fovcnt"          example:"100"`         //FOV的个数
	P1N0      int       `json:"p1n0"       gorm:"column:p1n0"            example:"50"`          //例预测的阴阳性 50阴性51阳性100未知
	TrueP1N0  int       `json:"truep1n0"   gorm:"column:truep1n0"        example:"51"`          //病例实际的阴阳性 50阴性51阳性100未知
	Remark    string    `json:"remark"     gorm:"column:remark"          example:"remark"`      //备注
	CreatedBy int64     `json:"-"          gorm:"column:created_by"      example:"7"`           //创建者
	CreatedAt time.Time `json:"created_at" gorm:"column:created_at"      example:"7"`           //创建时间
	UpdatedAt time.Time `json:"updated_at" gorm:"column:updated_at"      example:"7"`           //更新时间
	UserName  string    `json:"username"   gorm:"-"`                                            //创建者名字
	UserImg   string    `json:"userimg"    gorm:"-"`                                            //创建者头像
}

// BeforeCreate insert 之前的hook
func (r *Result) BeforeCreate(scope *gorm.Scope) error {
	if r.CreatedAt.IsZero() {
		r.CreatedAt = time.Now()
	}
	if r.UpdatedAt.IsZero() {
		r.UpdatedAt = time.Now()
	}
	if r.P1N0 == 0 {
		r.P1N0 = 100
	}
	if r.TrueP1N0 == 0 {
		r.TrueP1N0 = 100
	}
	return nil
}

// AfterFind 把数据库里面存的字符串转成数组返回
func (r *Result) AfterFind(scope *gorm.Scope) error {
	if r.CreatedBy > 0 {
		u, _ := FinduserbyID(r.CreatedBy)
		r.UserName = u.Name
		r.UserImg = u.Image
	}
	return nil
}

// UpdateResult 更新项目的预测结果记录
func (r *Result) UpdateResult() (e error) {
	updater := make(map[string]interface{})

	if r.Desc != "" {
		updater["description"] = r.Desc
	}
	if r.PCnt > 0 {
		updater["pcnt"] = r.PCnt
	}
	if r.NCnt > 0 {
		updater["ncnt"] = r.NCnt
	}
	if r.UCnt > 0 {
		updater["ucnt"] = r.UCnt
	}
	if r.FOVCnt > 0 {
		updater["fovcnt"] = r.FOVCnt
	}
	if r.P1N0 > 0 {
		updater["p1n0"] = r.P1N0
	}
	if r.TrueP1N0 > 0 {
		updater["truep1n0"] = r.TrueP1N0
	}
	if r.Remark != "" {
		updater["remark"] = r.Remark
	}
	ret := db.Model(&Result{}).Where("pid=?", r.PID).Updates(updater)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return ret.Error
}

// CreateOrUpdateResult 新建一个项目的预测结果记录,如果已经存在就更新
func (r *Result) CreateOrUpdateResult() (e error) {
	r.ID = 0
	var total int64

	ret := db.Model(&Result{}).Where("pid=?", r.PID).Count(&total)
	if ret.Error == nil && total > 0 {
		err := r.UpdateResult()
		if err != nil {
			logger.Info.Println(err)
		}
		return err
	}

	ret2 := db.Model(r).Create(&r)
	if ret2.Error != nil {
		logger.Info.Println(ret2.Error)
	}
	return ret2.Error
}

// ListResult 依次列出项目的预测结果记录
func ListResult(limit int64, skip int64) (totalNum int64, c []Result, e error) {
	var _r []Result
	var total int64 = 0

	ret := db.Model(&Result{}).Count(&total)
	ret = db.Model(&Result{}).Limit(limit).Offset(skip).Find(&_r)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return total, _r, ret.Error
}

// GetOneResultByPID 通过PID查找项目记录
func GetOneResultByPID(pid int64) (p Result, e error) {
	_p := Result{}
	ret2 := db.Model(&_p).Where("pid=?", pid).First(&_p)
	if ret2.Error != nil {
		return _p, ret2.Error
	}
	return _p, ret2.Error
}
