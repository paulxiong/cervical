package models

import (
	"time"

	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	u "github.com/paulxiong/cervical/webpage/2_api_server/utils"

	"github.com/jinzhu/gorm"
)

// Model 模型信息
type Model struct {
	ID            int       `json:"id"             gorm:"column:id"`             //id
	Type          int       `json:"type"           gorm:"column:type"`           //模型类别 0未知 1UNET 2GAN 3SVM 4MASKRCNN 5AUTOKERAS
	PID           int64     `json:"pid"            gorm:"column:pid"`            //从哪个项目训练出来的
	Path          string    `json:"path"           gorm:"column:path"`           //模型文件路径
	Desc          string    `json:"desc"           gorm:"column:description"`    //模型的文字描述
	Recall        float32   `json:"recall"         gorm:"column:recall"`         //训练评估得到的召回率,整数0.66表示66%
	Precision     float32   `json:"precision"      gorm:"column:precision1"`     //训练评估得到的准确率,整数0.66表示66%
	Ntrain        int       `json:"n_train"        gorm:"column:n_train"`        //训练用了多少张图片
	Nclasses      int       `json:"n_classes"      gorm:"column:n_classes"`      //训练有几个分类
	Types1        []int     `json:"types"          gorm:"-"`                     //训练的标签, 数组(传递给前端，数据库没有这个字段)
	Types2        string    `json:"-"              gorm:"column:types"`          //训练的标签, 字符串存储(存数据库，前端没有这个字段)
	InputShape    string    `json:"input_shape"    gorm:"column:input_shape"`    //训练输入的尺寸
	ModelCount    int       `json:"model_count"    gorm:"column:model_count"`    //产生的模型个数
	BestModel     int       `json:"best_model"     gorm:"column:best_model"`     //本次训练出的所有模型里面最优模型是第几个
	Loss          float32   `json:"loss"           gorm:"column:loss"`           //损失
	MetricValue   float32   `json:"metric_value"   gorm:"column:metric_value"`   //训练的准确度
	EvaluateValue float32   `json:"evaluate_value" gorm:"column:evaluate_value"` //评估准确度
	CreatedAt     time.Time `json:"created_at"     gorm:"column:created_at"`     //创建时间
	UpdatedAt     time.Time `json:"updated_at"     gorm:"column:updated_at"`     //更新时间
	CreatedBy     int64     `json:"-"              gorm:"column:created_by"`     //创建者ID
}

// BeforeCreate insert之前的hook
func (d *Model) BeforeCreate(scope *gorm.Scope) error {
	if d.CreatedAt.IsZero() {
		d.CreatedAt = time.Now()
	}
	if d.UpdatedAt.IsZero() {
		d.UpdatedAt = time.Now()
	}

	str, err2 := u.Array2String(&d.Types1)
	if err2 == nil {
		d.Types2 = str
	}
	return nil
}

// AfterFind 把数据库里面存的字符串转成数组返回
func (d *Model) AfterFind(scope *gorm.Scope) error {
	if d.Types2 != "" {
		arr, err := u.String2Array(d.Types2)
		if err == nil {
			d.Types1 = arr
		}
	}
	return nil
}

// CreateModelInfo 把模型信息记录到数据库
func (d *Model) CreateModelInfo() (e error) {
	d.ID = 0
	_d := Model{}

	ret2 := db.Model(d).Where("path=?", d.Path).First(&_d)
	if ret2.Error != nil {
		logger.Info.Println(ret2.Error)
	}

	if _d.ID > 0 {
		return ret2.Error
	}

	ret := db.Model(d).Save(&d)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return ret.Error
}

// ListModel 依次列出模型
func ListModel(limit int, skip int, _type int) (totalNum int64, c []Model, e error) {
	var _d []Model
	var total int64 = 0

	//返回可用来做分类的模型
	if _type == 5 || _type == 6 {
		db.Model(&Model{}).Where("type>4").Count(&total)
		ret := db.Model(&Model{}).Where("type>4").Limit(limit).Offset(skip).Find(&_d)
		if ret.Error != nil {
			logger.Info.Println(ret.Error)
		}
		return total, _d, ret.Error
	}

	db.Model(&Model{}).Where("type=?", _type).Count(&total)
	ret := db.Model(&Model{}).Where("type=?", _type).Limit(limit).Offset(skip).Find(&_d)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return total, _d, ret.Error
}

// FindModelInfoByPath 通过模型文件路径查找模型信息
func FindModelInfoByPath(modpath string) (m *Model, e error) {
	_d := Model{}

	ret2 := db.Model(&_d).Where("path=?", modpath).First(&_d)
	if ret2.Error != nil {
		logger.Info.Println(ret2.Error)
	}
	return &_d, ret2.Error
}

// FindModelInfoByID 通过模型的ID查找模型信息
func FindModelInfoByID(mid int) (m *Model, e error) {
	_d := Model{}

	ret2 := db.Model(&_d).Where("id=?", mid).First(&_d)
	if ret2.Error != nil {
		logger.Info.Println(ret2.Error)
	}
	return &_d, ret2.Error
}

// ModelInfoSaved 判断模型信息是否已经存入数据库
func (d *Model) ModelInfoSaved() bool {
	_d := Model{}

	ret2 := db.Model(&_d).Where("path=?", d.Path).First(&_d)
	if ret2.Error != nil {
		logger.Info.Println(ret2.Error)
	}
	if _d.Path != "" && len(_d.Path) > 0 {
		return true
	}
	return false
}
