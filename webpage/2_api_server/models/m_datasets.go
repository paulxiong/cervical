package models

import (
	"fmt"
	"log"
	"time"

	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	u "github.com/paulxiong/cervical/webpage/2_api_server/utils"

	"github.com/jinzhu/gorm"
)

// Image FOV图片信息
type Image struct {
	ID        int64     `json:"id"           gorm:"column:ID; primary_key"`
	Csvpath   string    `json:"csvpath"      gorm:"column:CSVPATH"`
	Imgpath   string    `json:"imgpath"      gorm:"column:IMGPATH"`
	W         int       `json:"w"            gorm:"column:W"` //X
	H         int       `json:"h"            gorm:"column:H"` //Y
	Batchid   string    `json:"batchid"      gorm:"column:BATCHID"`
	Medicalid string    `json:"medicalid"    gorm:"column:MEDICALID"`
	CreatedBy int64     `json:"created_by"   gorm:"column:created_by"` //创建者
	Status    int       `json:"status"       gorm:"column:status"`     //0删除1正常
	Type      int       `json:"type"         gorm:"column:type"`       //0系统默认自带1用户上传
	CreatedAt time.Time `json:"created_time" gorm:"column:CREATED_TIME"`
	UpdatedAt time.Time `json:"updated_time" gorm:"column:UPDATED_TIME"`
}

// BeforeCreate insert之前的hook
func (i *Image) BeforeCreate(scope *gorm.Scope) error {
	if i.CreatedAt.IsZero() {
		i.CreatedAt = time.Now()
	}
	if i.UpdatedAt.IsZero() {
		i.UpdatedAt = time.Now()
	}
	return nil
}

// CreateImage 新建一个图片信息到数据库
func (i *Image) CreateImage() (e error) {
	i.ID = 0
	img := Image{}
	ret1 := db.Model(&img).Where("BATCHID=? AND MEDICALID=? AND IMGPATH=?", img.Batchid, img.Medicalid, img.Imgpath).First(&img)
	if ret1.Error == nil && len(img.Imgpath) > 0 {
		return nil
	}

	ret := db.Model(i).Save(i)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}

	return ret.Error
}

// GetImageByID 通过图片ID查找图片信息
func GetImageByID(imgid int64) (img Image, e error) {
	var retimg Image
	ret := db.Model(&Image{}).Where("ID = ?", imgid).First(&retimg)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return retimg, ret.Error
}

// ListImage 依次按照ID顺序返回图片信息
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

// ListImageOfMedicalID 根据批次号病例号查找所有的图片
func ListImageOfMedicalID(bid string, mdcid string, limit int64, skip int64) (totalNum int, c []Image, e error) {
	var _i []Image
	var total int = 0

	db.Model(&Image{}).Where("BATCHID=? AND MEDICALID=?", mdcid, bid).Count(&total)
	ret := db.Model(&Image{}).Where("BATCHID=? AND MEDICALID=?", bid, mdcid).Limit(limit).Offset(skip).Find(&_i)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return total, _i, ret.Error
}

// ListImageCntByLabelType 通过标注的类型来依次列出有这种标注类型的FOV图片
func ListImageCntByLabelType(t int) (totalNum int64, e error) {
	type res struct {
		Total int64
	}

	selector1 := "SELECT count(*) as total from (SELECT c_label.IMGID FROM c_label,c_image  where c_label.TYPE=? AND c_image.ID=c_label.IMGID GROUP BY c_label.IMGID) xxx;"
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

	selector1 := "SELECT count(*) as total from (select BATCHID  from c_image group by BATCHID) xxx;"
	ress := res{}
	ret := db.Raw(selector1).Scan(&ress)
	if ret.Error != nil {
		log.Println(ret.Error)
		return 0, _b, ret.Error
	}

	selector1 = "select BATCHID as batchid from c_image group by BATCHID;"
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

// ListMedicalIDByBatchID 查出批次号下所有的病例
func ListMedicalIDByBatchID(limit int, skip int, batchid string) (totalNum int64, c []string, e error) {
	var _b []string
	type res struct {
		Total int64
	}
	type res2 struct {
		Medicalid string
	}
	_b = make([]string, 0)

	selector1 := "SELECT count(*) as total from (select MEDICALID  from c_image where BATCHID=? group by MEDICALID) xxx;"
	ress := res{}
	ret := db.Raw(selector1, batchid).Scan(&ress)
	if ret.Error != nil {
		log.Println(ret.Error)
		return 0, _b, ret.Error
	}

	selector1 = "select MEDICALID as medicalid from c_image where BATCHID=? group by MEDICALID;"
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

	selector1 := "select IMGPATH as imgpath, BATCHID as batchid, MEDICALID as medicalid from c_image,c_label where BATCHID in (?) AND MEDICALID in (?) AND c_label.IMGID=image.ID AND c_label.TYPE=? LIMIT ? OFFSET ?;"
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

// ListImagesNPTypeByMedicalID 查找出MedicalId下图片的类型(N/P)的数量
func ListImagesNPTypeByMedicalID(medicalids []string) (countN int, countP int, e error) {
	type res struct {
		Total int
	}

	selector1 := "SELECT count(*) as total from (SELECT c_image.CSVPATH from c_label,c_image,c_category where c_image.MEDICALID in (?) AND c_label.IMGID=c_image.ID AND c_label.TYPE=c_category.ID AND c_category.P1N0=? GROUP BY c_image.CSVPATH) xx;"
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

// ImagesByMedicalID 某一病例下图片的信息
type ImagesByMedicalID struct {
	Type      int    `json:"type"`
	Csvpath   string `json:"csvpath"`
	Imgpath   string `json:"imgpath"`
	Batchid   string `json:"batchid"`
	Medicalid string `json:"medicalid"`
	P1N0      int    `json:"p1n0"` //是阴性还是阳性
}

// ListImagesByMedicalID 查找出MedicalId下图片所有图片，按照n/p分开
func ListImagesByMedicalID(medicalid string) (imgs []ImagesByMedicalID, e error) {
	selector1 := "SELECT c_image.type as type, c_image.CSVPATH as csvpath, c_image.MEDICALID as medicalid, c_image.BATCHID as batchid, c_image.IMGPATH as imgpath from c_label,c_image,c_category where c_image.MEDICALID=? AND c_label.IMGID=c_image.ID AND c_label.TYPE=c_category.ID AND c_category.P1N0=? GROUP BY c_image.CSVPATH;"
	ressN := []ImagesByMedicalID{}
	ressP := []ImagesByMedicalID{}
	ressAll := make([]ImagesByMedicalID, 0)
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

// ListImagesByMedicalID2 查找出MedicalId下图片所有图片，不管有没有标注
func ListImagesByMedicalID2(medicalid string) (totalnum int, imgs []Image, e error) {
	var _i []Image
	var total int = 0

	db.Model(&Image{}).Where("MEDICALID=?", medicalid).Count(&total)
	ret := db.Model(&Image{}).Where("MEDICALID=?", medicalid).Find(&_i)

	return total, _i, ret.Error
}

// Category 标注、细胞的分类信息
type Category struct {
	ID        int64     `json:"id"     gorm:"column:ID"`           //分类ID
	Name      string    `json:"name"   gorm:"column:NAME"`         //名字
	Other     string    `json:"other"  gorm:"column:OTHER"`        //描述
	P1N0      int       `json:"p1n0"     gorm:"column:P1N0"`       //是阴性还是阳性
	CreatedAt time.Time `json:"-"      gorm:"column:CREATED_TIME"` //创建时间
	UpdatedAt time.Time `json:"-"      gorm:"column:UPDATED_TIME"` //更新时间
}

// BeforeCreate insert 之前的hook
func (u *Category) BeforeCreate(scope *gorm.Scope) error {
	if u.CreatedAt.IsZero() {
		u.CreatedAt = time.Now()
	}
	if u.UpdatedAt.IsZero() {
		u.UpdatedAt = time.Now()
	}
	return nil
}

// ListCategory 依次列出分类信息
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

// GetCategoryByID 通过ID查找分类的信息
func GetCategoryByID(id int) (c Category, e error) {
	var _c Category

	ret := db.Model(&_c).Where("Id = ?", id).First(&_c)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return _c, ret.Error
}

// DatasetParameter 当前数据集的参数
type DatasetParameter struct {
	ParameterGray  int `json:"parameter_gray"  gorm:"column:parameter_gray"`  //数据处理时候颜色
	ParameterSize  int `json:"parameter_size"  gorm:"column:parameter_size"`  //切割的正方形边长
	ParameterType  int `json:"parameter_type"  gorm:"column:parameter_type"`  //切割类型
	ParameterMid   int `json:"parameter_mid"   gorm:"column:parameter_mid"`   //切割使用的模型
	ParameterCache int `json:"parameter_cache" gorm:"column:parameter_cache"` //是否使用裁剪过的cache
}

// Dataset 数据集的信息
type Dataset struct {
	ID             int64     `json:"id"              gorm:"column:id; primary_key"` //ID
	Desc           string    `json:"desc"            gorm:"column:description"`     //描述
	Status         int       `json:"status"          gorm:"column:status"`          //状态 0初始化 1送去处理 2开始处理 3处理出错 4处理完成 5目录不存在
	Dir            string    `json:"dir"             gorm:"column:dir"`             //文件夹名称
	ProcessTime    time.Time `json:"processtime"     gorm:"column:process_time"`    //开始处理数据时间
	ProcessEnd     time.Time `json:"processend"      gorm:"column:process_end"`     //处理数据结束时间
	ProcessPercent int       `json:"process_percent" gorm:"column:process_percent"` //处理数据的进度
	ETA            int       `json:"ETA"             gorm:"column:ETA"`             //预估还要多长时间结束,单位是秒

	DatasetParameter

	Types1      []int    `json:"types"          gorm:"-"`                 //当前数据集的细胞分类, 数组(传递给前端，数据库没有这个字段)
	Types2      string   `json:"-"              gorm:"column:types"`      //当前数据集的细胞分类, 字符串存储(存数据库，前端没有这个字段)
	BatchIDs1   []string `json:"batchids"       gorm:"-"`                 //当前数据集的批次, 数组(传递给前端，数据库没有这个字段)
	BatchIDs2   string   `json:"-"              gorm:"column:batchids"`   //当前数据集的批次, 字符串存储(存数据库，前端没有这个字段)
	MedicalIDs1 []string `json:"medicalids"     gorm:"-"`                 //当前数据集的病例, 数组(传递给前端，数据库没有这个字段)
	MedicalIDs2 string   `json:"-"              gorm:"column:medicalids"` //当前数据集的病例, 字符串存储(存数据库，前端没有这个字段)

	UserName string `json:"username" gorm:"-"` //创建者名字
	UserImg  string `json:"userimg"  gorm:"-"` //创建者头像

	CreatedBy int64     `json:"created_by"      gorm:"column:created_by"` //创建者
	CreatedAt time.Time `json:"created_at"      gorm:"column:created_at"` //创建时间
	UpdatedAt time.Time `json:"updated_at"      gorm:"column:updated_at"` //更新时间
}

// BeforeCreate insert 之前的hook
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
	if d.ETA == 0 {
		d.ETA = 60 //默认假设１分钟
	}

	d.BatchIDs1 = u.RemoveDuplicatesAndEmpty(d.BatchIDs1)
	d.MedicalIDs1 = u.RemoveDuplicatesAndEmpty(d.MedicalIDs1)

	str, err2 := u.IntArray2String(&d.Types1)
	if err2 == nil {
		d.Types2 = str
	}
	str, err2 = u.StrArray2String(&d.BatchIDs1)
	if err2 == nil {
		d.BatchIDs2 = str
	}
	str, err2 = u.StrArray2String(&d.MedicalIDs1)
	if err2 == nil {
		d.MedicalIDs2 = str
	}
	return nil
}

// AfterFind 把数据库里面存的字符串转成数组返回
func (d *Dataset) AfterFind(scope *gorm.Scope) error {
	if d.Types2 != "" {
		arr, err := u.String2IntArray(d.Types2)
		if err == nil {
			d.Types1 = arr
		}
	}
	if d.BatchIDs2 != "" {
		arr, err := u.String2StrArray(d.BatchIDs2)
		if err == nil {
			d.BatchIDs1 = arr
		}
	}
	if d.MedicalIDs2 != "" {
		arr, err := u.String2StrArray(d.MedicalIDs2)
		if err == nil {
			d.MedicalIDs1 = arr
		}
	}
	d.BatchIDs1 = u.RemoveDuplicatesAndEmpty(d.BatchIDs1)
	d.MedicalIDs1 = u.RemoveDuplicatesAndEmpty(d.MedicalIDs1)

	if d.CreatedBy > 0 {
		u, _ := FinduserbyID(d.CreatedBy)
		d.UserName = u.Name
		d.UserImg = u.Image
	}

	return nil
}

//CellTypesinfo 细胞类型和对应的个数
type CellTypesinfo struct {
	CellType int `json:"celltype" example:"7"`   //细胞的类型
	LabelCnt int `json:"labelcnt" example:"900"` //类型的个数
}

// UpdateDatasetsCellTypes 更新数据集的包含的细胞类型,在数据裁剪完之后更新
func UpdateDatasetsCellTypes(did int64, cti []CellTypesinfo) (e error) {
	d := Dataset{}
	ret2 := db.Model(&d).Where("id=?", did).First(&d)
	if ret2.Error != nil {
		return ret2.Error
	}

	typearr := make([]int, 0)
	for i := 0; i < len(cti); i++ {
		typearr = append(typearr, cti[i].CellType)
	}
	if d.Status == 4 {
		arr, err := u.IntArray2String(&typearr)
		if err == nil {
			d.Types2 = arr
		}
	} else {
		return nil
	}

	ret := db.Model(&d).Where("id=?", did).Updates(d)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return ret.Error
}

// ListDataset 依次列出数据集
func ListDataset(limit int, skip int, order int) (totalNum int64, c []Dataset, e error) {
	//type, default 1, 0未知 1训练 2预测 10全部类型
	var _d []Dataset
	var total int64 = 0
	ret := db.Model(&Dataset{}).Count(&total)

	orderStr := "created_at DESC"
	//order, default 1, 1倒序，0顺序
	if order == 0 {
		orderStr = "created_at ASC"
	}

	ret = db.Model(&Dataset{}).Order(orderStr).Limit(limit).Offset(skip).Find(&_d)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return total, _d, ret.Error
}

// CreateDatasets 新建一个数据集
func (d *Dataset) CreateDatasets() (e error) {
	d.ID = 0
	ret := db.Model(d).Save(d)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return ret.Error
}

// UpdateDatasetsStatus 更新数据集的状态, 0初始化 1送去处理 2开始处理 3处理出错 4处理完成 5目录不存在
func UpdateDatasetsStatus(did int64, status int) (e error) {
	d := Dataset{}
	ret2 := db.Model(&d).Where("id=?", did).First(&d)
	if ret2.Error != nil {
		return ret2.Error
	}

	if status == 2 && d.Status == 1 {
		d.ProcessTime = time.Now()
	} else if status == 4 && d.Status == 2 {
		d.ProcessEnd = time.Now()
	}
	d.Status = status

	ret := db.Model(&d).Where("id=?", did).Updates(d)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return ret.Error
}

// UpdateDatasetsPercent 更新任务完成的百分比以及预估还要多长时间结束
func UpdateDatasetsPercent(did int64, percent int, ETA int) (e error) {
	d := Dataset{}
	ret2 := db.Model(&d).Where("id=?", did).First(&d)
	if ret2.Error != nil {
		return ret2.Error
	}

	if d.Status < 6 { //处理数据集的进度, 0初始化 1送去处理 2开始处理 3处理出错 4处理完成 5目录不存在
		d.ProcessPercent = percent
		d.ETA = ETA
	}

	ret := db.Model(&d).Where("id=?", did).Updates(map[string]interface{}{"process_percent": d.ProcessPercent, "ETA": d.ETA})
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return ret.Error
}

// GetOneDatasetsToProcess 请求一个指定状态和类型的数据集去处理
func GetOneDatasetsToProcess(status int) (dt Dataset, e error) {
	d := Dataset{}
	ret2 := db.Model(&d).Where("status=?", status).First(&d)
	if ret2.Error != nil {
		return d, ret2.Error
	}
	return d, ret2.Error
}

// GetOneDatasetByID 通过ID查找数据集
func GetOneDatasetByID(id int) (dt Dataset, e error) {
	d := Dataset{}
	ret2 := db.Model(&d).Where("id=?", id).First(&d)
	if ret2.Error != nil {
		return d, ret2.Error
	}
	return d, ret2.Error
}
