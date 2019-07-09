package models

import (
	"fmt"
	"log"
	"time"

	logger "../log"

	"github.com/jinzhu/gorm"
)

type Image struct {
	Id        int64     `json:"id"           gorm:"column:ID"`
	Csvpath   string    `json:"csvpath"      gorm:"column:CSVPATH"`
	Imgpath   string    `json:"imgpath"      gorm:"column:IMGPATH"`
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
	Imgpath   string `json:"imgpath"`
	Batchid   string `json:"batchid"`
	Medicalid string `json:"medicalid"`
	P1N0      int    `json:"p1n0"` //是阴性还是阳性
}

// ListImagesByMedicalId 查找出MedicalId下图片所有图片，按照n/p分开
func ListImagesByMedicalId(medicalid string) (imgs []ImagesByMedicalId, e error) {
	selector1 := "SELECT image.MEDICALID as medicalid, image.BATCHID as batchid, image.IMGPATH as imgpath from label,image,category where image.MEDICALID=? AND label.IMGID=image.ID AND label.TYPE=category.ID AND category.P1N0=? GROUP BY image.CSVPATH;"
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
	Id        int64     `json:"id"          gorm:"column:ID"`           //分类ID
	Desc      string    `json:"desc"        gorm:"column:DESCRIPTION"`  //描述
	Status    int       `json:"status"      gorm:"column:STATUS"`       //状态 0初始化1用户要求开始处理2开始处理3处理出错4处理完成5目录不存在
	Dir       string    `json:"dir"         gorm:"column:DIR"`          //文件夹名称(创建时间 + ID)
	CreatedBy int64     `json:"created_by"  gorm:"column:CREATED_BY"`   //创建者
	CreatedAt time.Time `json:"-"           gorm:"column:CREATED_TIME"` //创建时间
	StartTime time.Time `json:"-"           gorm:"column:START_TIME"`   //开始处理的时间
	UpdatedAt time.Time `json:"-"           gorm:"column:UPDATED_TIME"` //更新时间
}

func (d *Dataset) BeforeCreate(scope *gorm.Scope) error {
	if d.CreatedAt.IsZero() {
		d.CreatedAt = time.Now()
	}
	if d.UpdatedAt.IsZero() {
		d.UpdatedAt = time.Now()
	}
	if d.StartTime.IsZero() {
		d.StartTime = time.Now()
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
		logger.Info.Println(ret2.Error)
		return ret2.Error
	}

	if d.Status != 0 || d.Status == status {
		return ret2.Error
	}
	d.Status = status

	ret := db.Model(&d).Where("ID=?", did).Updates(d)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return ret.Error
}

func GetOneDatasetsToCrop() (dt Dataset, e error) {
	d := Dataset{}
	ret2 := db.Model(&d).Where("STATUS=?", 1).First(&d)
	if ret2.Error != nil {
		logger.Info.Println(ret2.Error)
		return d, ret2.Error
	}
	return d, ret2.Error
}
