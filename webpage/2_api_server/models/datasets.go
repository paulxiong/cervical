package models

import (
	"fmt"
	"log"
	"time"

	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"

	"github.com/jinzhu/gorm"
)

type Image struct {
	Id        int64     `json:"id"           gorm:"column:ID"`
	Csvpath   string    `json:"csvpath"      gorm:"column:CSVPATH"`
	Imgpath   string    `json:"imgpath"      gorm:"column:IMGPATH"`
	W         int       `json:"w"            gorm:"column:W"` //X
	H         int       `json:"h"            gorm:"column:H"` //Y
	Batchid   string    `json:"batchid"      gorm:"column:BATCHID"`
	Medicalid string    `json:"medicalid"    gorm:"column:MEDICALID"`
	CreatedAt time.Time `json:"created_time" gorm:"column:CREATED_TIME"`
	UpdatedAt time.Time `json:"updated_time" gorm:"column:UPDATED_TIME"`
}

func (u *Image) BeforeCreate(scope *gorm.Scope) error {
	if u.CreatedAt.IsZero() {
		u.CreatedAt = time.Now()
	}
	if u.UpdatedAt.IsZero() {
		u.UpdatedAt = time.Now()
	}
	return nil
}

func GetImageById(imgid int64) (img Image, e error) {
	var retimg Image
	ret := db.Model(&Image{}).Where("ID = ?", imgid).First(&retimg)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return retimg, ret.Error
}

func ListImage(limit int, skip int) (totalNum int64, c []Image, e error) {
	var _i []Image
	var total int64 = 0

	db.Model(&Image{}).Count(&total)
	ret := db.Model(&Image{}).Limit(limit).Offset(skip).Find(&_i)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return total, _i, ret.Error
}

func ListImageCntByLabelType(t int) (totalNum int64, e error) {
	type res struct {
		Total int64
	}

	selector1 := "SELECT count(*) as total from (SELECT label.IMGID FROM label,image  where label.TYPE=? AND image.ID=label.IMGID GROUP BY label.IMGID) xxx;"
	selector := fmt.Sprintf("%d", t)

	ress := res{}
	ret := db.Raw(selector1, selector).Scan(&ress)
	if ret.Error != nil {
		log.Println(ret.Error)
	}

	return ress.Total, ret.Error
}

// ListBatch 查出所有的批次号
func ListBatch(limit int, skip int) (totalNum int64, c []string, e error) {
	var _b []string
	type res struct {
		Total int64
	}
	type res2 struct {
		Batchid string
	}
	_b = make([]string, 0)

	selector1 := "SELECT count(*) as total from (select BATCHID  from image group by BATCHID) xxx;"
	ress := res{}
	ret := db.Raw(selector1).Scan(&ress)
	if ret.Error != nil {
		log.Println(ret.Error)
		return 0, _b, ret.Error
	}

	selector1 = "select BATCHID as batchid from image group by BATCHID;"
	ress2 := make([]res2, 0)
	ret2 := db.Raw(selector1).Scan(&ress2)
	if ret2.Error != nil {
		log.Println(ret2.Error)
	}
	for _, v := range ress2 {
		_b = append(_b, v.Batchid)
	}

	return ress.Total, _b, ret2.Error
}

// ListMedicalIdByBatchId 查出批次号下所有的病例
func ListMedicalIdByBatchId(limit int, skip int, batchid string) (totalNum int64, c []string, e error) {
	var _b []string
	type res struct {
		Total int64
	}
	type res2 struct {
		Medicalid string
	}
	_b = make([]string, 0)

	selector1 := "SELECT count(*) as total from (select MEDICALID  from image where BATCHID=? group by MEDICALID) xxx;"
	ress := res{}
	ret := db.Raw(selector1, batchid).Scan(&ress)
	if ret.Error != nil {
		log.Println(ret.Error)
		return 0, _b, ret.Error
	}

	selector1 = "select MEDICALID as medicalid from image where BATCHID=? group by MEDICALID;"
	ress2 := make([]res2, 0)
	ret2 := db.Raw(selector1, batchid).Scan(&ress2)
	if ret2.Error != nil {
		log.Println(ret2.Error)
	}
	for _, v := range ress2 {
		_b = append(_b, v.Medicalid)
	}

	return ress.Total, _b, ret2.Error
}

// ListWantedImages 查出符合条件的图片
func ListWantedImages(limit int, skip int, batchids []string, medicalids []string, categoryid int) (c []string, e error) {
	var _b []string
	type res struct {
		Imgpath   string
		Batchid   string
		Medicalid string
	}
	_b = make([]string, 0)

	selector1 := "select IMGPATH as imgpath, BATCHID as batchid, MEDICALID as medicalid from image,label where BATCHID in (?) AND MEDICALID in (?) AND label.IMGID=image.ID AND label.TYPE=? LIMIT ? OFFSET ?;"
	ress := []res{}
	ret := db.Raw(selector1, batchids, medicalids, categoryid, limit, skip).Scan(&ress)
	if ret.Error != nil {
		log.Println(ret.Error)
		return _b, ret.Error
	}
	logger.Info.Println(ress)
	for _, v := range ress {
		_b = append(_b, v.Batchid+"/"+v.Medicalid+"/"+v.Imgpath)
	}

	return _b, ret.Error
}

// ListImagesNPTypeByMedicalId 查找出MedicalId下图片的类型(N/P)的数量
func ListImagesNPTypeByMedicalId(medicalids []string) (countN int, countP int, e error) {
	type res struct {
		Total int
	}

	selector1 := "SELECT count(*) as total from (SELECT image.CSVPATH from label,image,category where image.MEDICALID in (?) AND label.IMGID=image.ID AND label.TYPE=category.ID AND category.P1N0=? GROUP BY image.CSVPATH) xx;"
	ressN := res{}
	ressP := res{}
	ret := db.Raw(selector1, medicalids, 0).Scan(&ressN)
	if ret.Error != nil {
		log.Println(ret.Error)
		return ressN.Total, ressP.Total, ret.Error
	}
	ret2 := db.Raw(selector1, medicalids, 1).Scan(&ressP)
	if ret2.Error != nil {
		log.Println(ret2.Error)
	}
	return ressN.Total, ressP.Total, ret2.Error
}

type ImagesByMedicalId struct {
	Csvpath   string `json:"csvpath"`
	Imgpath   string `json:"imgpath"`
	Batchid   string `json:"batchid"`
	Medicalid string `json:"medicalid"`
	P1N0      int    `json:"p1n0"` //是阴性还是阳性
}

// ListImagesByMedicalId 查找出MedicalId下图片所有图片，按照n/p分开
func ListImagesByMedicalId(medicalid string) (imgs []ImagesByMedicalId, e error) {
	selector1 := "SELECT image.CSVPATH as csvpath, image.MEDICALID as medicalid, image.BATCHID as batchid, image.IMGPATH as imgpath from label,image,category where image.MEDICALID=? AND label.IMGID=image.ID AND label.TYPE=category.ID AND category.P1N0=? GROUP BY image.CSVPATH;"
	ressN := []ImagesByMedicalId{}
	ressP := []ImagesByMedicalId{}
	ressAll := make([]ImagesByMedicalId, 0)
	ret := db.Raw(selector1, medicalid, 0).Scan(&ressN)
	if ret.Error != nil {
		log.Println(ret.Error)
	}
	for _, v := range ressN {
		v.P1N0 = 0
		ressAll = append(ressAll, v)
	}
	ret2 := db.Raw(selector1, medicalid, 1).Scan(&ressP)
	if ret2.Error != nil {
		log.Println(ret2.Error)
	}
	for _, v2 := range ressP {
		v2.P1N0 = 1
		ressAll = append(ressAll, v2)
	}
	return ressAll, ret2.Error
}

type Label struct {
	Id        int64     `json:"id"            gorm:"column:ID"`    //标注信息ID
	Imgid     int64     `json:"imgid"         gorm:"column:IMGID"` //所属图片的ID
	Type      int       `json:"type"          gorm:"column:TYPE"`  //类新
	TypeOut   string    `json:"typeout"       gorm:"-"`            //类新，前端使用数据库没有
	X         int       `json:"x"             gorm:"column:X"`     //X
	Y         int       `json:"y"             gorm:"column:Y"`     //Y
	W         int       `json:"w"             gorm:"column:W"`     //X
	H         int       `json:"h"             gorm:"column:H"`     //Y     `
	CreatedAt time.Time `json:"created_time"  gorm:"column:CREATED_TIME"`
	UpdatedAt time.Time `json:"updated_time"  gorm:"column:UPDATED_TIME"`
}

func (u *Label) BeforeCreate(scope *gorm.Scope) error {
	if u.CreatedAt.IsZero() {
		u.CreatedAt = time.Now()
	}
	if u.UpdatedAt.IsZero() {
		u.UpdatedAt = time.Now()
	}
	return nil
}

func ListLabel(limit int, skip int) (totalNum int64, l []Label, e error) {
	var _l []Label
	var total int64 = 0

	db.Model(&Label{}).Count(&total)
	ret := db.Model(&Label{}).Limit(limit).Offset(skip).Find(&_l)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return total, _l, ret.Error
}

func ListLabelByType(limit int, skip int, t int) (totalNum int64, l []Label, e error) {
	var _l []Label
	var total int64 = 0

	db.Model(&Label{}).Where("TYPE = ?", t).Count(&total)
	ret := db.Model(&Label{}).Where("TYPE = ?", t).Limit(limit).Offset(skip).Find(&_l)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return total, _l, ret.Error
}

func ListLabelByImageId(limit int, skip int, imgid int) (totalNum int64, l []Label, e error) {
	var _l []Label
	var total int64 = 0

	db.Model(&Label{}).Where("IMGID = ?", imgid).Count(&total)
	ret := db.Model(&Label{}).Where("IMGID = ?", imgid).Limit(limit).Offset(skip).Find(&_l)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return total, _l, ret.Error
}

func ListLabelCountByPN(pn int) (totalNum int64, e error) {
	type res struct {
		Total int64
	}
	selector1 := "SELECT COUNT(label.IMGID) as total FROM label,category  where label.TYPE=category.ID AND category.P1N0=?;"
	ress := res{}
	ret := db.Raw(selector1, pn).Scan(&ress)
	if ret.Error != nil {
		log.Println(ret.Error)
	}

	return ress.Total, ret.Error
}

type Category struct {
	Id        int64     `json:"id"     gorm:"column:ID"`           //分类ID
	Name      string    `json:"name"   gorm:"column:NAME"`         //名字
	Other     string    `json:"other"  gorm:"column:OTHER"`        //描述
	P1N0      int       `json:"p1n0"     gorm:"column:P1N0"`       //是阴性还是阳性
	CreatedAt time.Time `json:"-"      gorm:"column:CREATED_TIME"` //创建时间
	UpdatedAt time.Time `json:"-"      gorm:"column:UPDATED_TIME"` //更新时间
}

func (u *Category) BeforeCreate(scope *gorm.Scope) error {
	if u.CreatedAt.IsZero() {
		u.CreatedAt = time.Now()
	}
	if u.UpdatedAt.IsZero() {
		u.UpdatedAt = time.Now()
	}
	return nil
}

func ListCategory(limit int, skip int) (totalNum int64, c []Category, e error) {
	var _c []Category
	var total int64 = 0

	db.Model(&Category{}).Count(&total)
	ret := db.Model(&Category{}).Limit(limit).Offset(skip).Find(&_c)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return total, _c, ret.Error
}

func GetCategoryById(id int) (c Category, e error) {
	var _c Category

	ret := db.Model(&_c).Where("Id = ?", id).First(&_c)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return _c, ret.Error
}

type Dataset struct {
	Id          int64     `json:"id"             gorm:"column:ID"`           //ID
	Type        int       `json:"type"           gorm:"column:TYPE"`         //分类
	Desc        string    `json:"desc"           gorm:"column:DESCRIPTION"`  //描述
	Status      int       `json:"status"         gorm:"column:STATUS"`       //状态 0初始化 1送去处理 2开始处理 3处理出错 4处理完成 5目录不存在 6开始训练 7训练出错 8训练完成
	Dir         string    `json:"dir"            gorm:"column:DIR"`          //文件夹名称(创建时间 + ID)
	ProcessTime time.Time `json:"processtime"    gorm:"column:PROCESS_TIME"` //开始处理数据时间
	ProcessEnd  time.Time `json:"processend"     gorm:"column:PROCESS_END"`  //处理数据结束时间
	TrainTime   time.Time `json:"traintime"      gorm:"column:TRAIN_TIME"`   //开始训练的时间
	TrainEnd    time.Time `json:"trainend"       gorm:"column:TRAIN_END"`    //训练结束的时间
	PredictTime time.Time `json:"predicttime"    gorm:"column:PREDICT_TIME"` //开始预测的时间
	PredictEnd  time.Time `json:"predictend"     gorm:"column:PREDICT_END"`  //预测结束的时间
	Percent     int64     `json:"percent"        gorm:"column:PERCENT"`      //处理数据/训练/预测的进度
	CreatedBy   int64     `json:"created_by"     gorm:"column:CREATED_BY"`   //创建者
	CreatedAt   time.Time `json:"created_at"     gorm:"column:CREATED_TIME"` //创建时间
	UpdatedAt   time.Time `json:"updated_at"     gorm:"column:UPDATED_TIME"` //更新时间
}

func (d *Dataset) BeforeCreate(scope *gorm.Scope) error {
	if d.CreatedAt.IsZero() {
		d.CreatedAt = time.Now()
	}
	if d.UpdatedAt.IsZero() {
		d.UpdatedAt = time.Now()
	}
	if d.ProcessTime.IsZero() {
		d.ProcessTime = time.Now()
		d.ProcessEnd = time.Now()
	}
	if d.TrainTime.IsZero() {
		d.TrainTime = time.Now()
		d.TrainEnd = time.Now()
	}
	if d.PredictTime.IsZero() {
		d.PredictTime = time.Now()
		d.PredictEnd = time.Now()
	}
	return nil
}

func ListDataset(limit int, skip int) (totalNum int64, c []Dataset, e error) {
	var _d []Dataset
	var total int64 = 0

	db.Model(&Dataset{}).Count(&total)
	ret := db.Model(&Dataset{}).Limit(limit).Offset(skip).Find(&_d)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return total, _d, ret.Error
}

func (d *Dataset) CreateDatasets() (e error) {
	d.Id = 0
	ret := db.Model(d).Save(&d)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}

	ret2 := db.Model(d).Where("DIR=?", d.Dir).First(&d)
	if ret2.Error != nil {
		logger.Info.Println(ret2.Error)
	}
	return ret2.Error
}

func UpdateDatasetsStatus(did int64, status int) (e error) {
	d := Dataset{}
	ret2 := db.Model(&d).Where("ID=?", did).First(&d)
	if ret2.Error != nil {
		return ret2.Error
	}
	/*
		logger.Info.Println(status, d.Status)
		if d.Status >= status {
			return ret2.Error
		}
	*/
	d.Status = status
	if status == 2 {
		d.ProcessTime = time.Now()
	}

	ret := db.Model(&d).Where("ID=?", did).Updates(d)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return ret.Error
}

// UpdateDatasetsPercent 更新任务完成的百分比
func UpdateDatasetsPercent(did int64, percent int64) (e error) {
	d := Dataset{}
	ret2 := db.Model(&d).Where("ID=?", did).First(&d)
	if ret2.Error != nil {
		return ret2.Error
	}

	d.Percent = percent

	ret := db.Model(&d).Where("ID=?", did).Updates(d)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return ret.Error
}

func GetOneDatasetsToProcess(status int, _type int) (dt Dataset, e error) {
	d := Dataset{}
	ret2 := db.Model(&d).Where("STATUS=? AND TYPE=?", status, _type).First(&d)
	if ret2.Error != nil {
		return d, ret2.Error
	}
	return d, ret2.Error
}

func GetOneDatasetById(id int) (dt Dataset, e error) {
	d := Dataset{}
	ret2 := db.Model(&d).Where("ID=?", id).First(&d)
	if ret2.Error != nil {
		return d, ret2.Error
	}
	return d, ret2.Error
}

type Model struct {
	Id        int       `json:"id"    gorm:"column:ID"`
	Type      int       `json:"type"  gorm:"column:TYPE"`
	Index     int       `json:"index" gorm:"-"`
	DId       int64     `json:"did"   gorm:"column:DID"`
	Path      string    `json:"-"     gorm:"column:PATH"`
	Desc      string    `json:"desc"  gorm:"column:DESCRIPTION"`  //描述
	CreatedAt time.Time `json:"-"     gorm:"column:CREATED_TIME"` //创建时间
	UpdatedAt time.Time `json:"-"     gorm:"column:UPDATED_TIME"` //更新时间
	// gan
	TotalEpoch       int     `json:"total_epoch"      gorm:"-"`
	ErrD_real        float32 `json:"errD_real"        gorm:"-"`
	ErrD_fake        float32 `json:"errD_fake"        gorm:"-"`
	Gradient_penalty float32 `json:"gradient_penalty" gorm:"-"`
	D_cost           float32 `json:"D_cost"           gorm:"-"`
	Mi_loss          float32 `json:"mi_loss"          gorm:"-"`
	Purity           float32 `json:"purity"           gorm:"-"`
	Entropy          float32 `json:"entropy"          gorm:"-"`
	// svm
	Ts        int     `json:"ts"        gorm:"-"`
	F1_score  float32 `json:"f1_score"  gorm:"-"`
	Recall    float32 `json:"recall"    gorm:"-"`
	Precision float32 `json:"precision" gorm:"-"`
}

func (d *Model) BeforeCreate(scope *gorm.Scope) error {
	if d.CreatedAt.IsZero() {
		d.CreatedAt = time.Now()
	}
	if d.UpdatedAt.IsZero() {
		d.UpdatedAt = time.Now()
	}
	return nil
}

func (d *Model) CreateModelInfo() (e error) {
	d.Id = 0
	_d := Model{}

	ret2 := db.Model(d).Where("PATH=?", d.Path).First(&_d)
	if ret2.Error != nil {
		logger.Info.Println(ret2.Error)
	}

	if _d.Id > 0 {
		return ret2.Error
	}

	ret := db.Model(d).Save(&d)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return ret.Error
}
