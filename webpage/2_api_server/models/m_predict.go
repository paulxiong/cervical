package models

import (
	"fmt"
	"time"

	"github.com/jinzhu/gorm"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
)

// Predict 单个细胞的预测结果
type Predict struct {
	ID           int64     `json:"id"            gorm:"column:id; primary_key" example:"7"`   //预测信息ID
	ImgID        int64     `json:"imgid"         gorm:"column:imgid"           example:"7"`   //所属图片的ID
	PID          int64     `json:"pid"           gorm:"column:pid"             example:"7"`   //所属项目的ID
	X1           int       `json:"x1"            gorm:"column:x1"              example:"100"` //左上角X坐标 单位是像素
	Y1           int       `json:"y1"            gorm:"column:y1"              example:"100"` //左上角Y坐标 单位是像素
	X2           int       `json:"x2"            gorm:"column:x2"              example:"100"` //右下角X坐标 单位是像素
	Y2           int       `json:"y2"            gorm:"column:y2"              example:"100"` //预右下角Y坐标 单位是像素
	CellPath     string    `json:"cellpath"      gorm:"column:cellpath"        example:"100"` //上述坐标切割出来的细胞
	PredictScore int       `json:"predict_score" gorm:"column:predict_score"   example:"100"` //预测得分 50表示50%
	PredictType  int       `json:"predict_type"  gorm:"column:predict_type"    example:"100"` //预测的细胞类型,1到15是细胞类型, 50阴性 51阳性 100 未知, 200 不是细胞
	PredictP1n0  int       `json:"predict_p1n0"  gorm:"column:predict_p1n0"    example:"100"` //预测阴/阳性
	TrueType     int       `json:"true_type"     gorm:"column:true_type"       example:"100"` //医生标注的细胞类型 默认等于predict_type
	TrueP1n0     int       `json:"true_p1n0"     gorm:"column:true_p1n0"       example:"100"` //医生标注的阴/阳性 默认等于predict_p1n0
	VID          int64     `json:"vid"           gorm:"column:vid"             example:"7"`   //谁去做审核(verify)的用户ID
	Status       int       `json:"status"        gorm:"column:status"          example:"100"` //状态 0 未审核 1 已审核 2 移除 3 管理员确认
	CreatedBy    int64     `json:"created_by"    gorm:"column:created_by"`                    //创建者
	CreatedAt    time.Time `json:"created_at"    gorm:"column:created_at"`                    //创建时间
	UpdatedAt    time.Time `json:"updated_at"    gorm:"column:updated_at"`                    //更新时间
}

// BeforeCreate insert 之前的hook
func (p *Predict) BeforeCreate(scope *gorm.Scope) error {
	if p.CreatedAt.IsZero() {
		p.CreatedAt = time.Now()
	}
	if p.UpdatedAt.IsZero() {
		p.UpdatedAt = time.Now()
	}
	return nil
}

// FindPredictbyID 按照ID查询审核
func FindPredictbyID(id int64) (*Predict, error) {
	_p := &Predict{}
	ret := db.Model(_p).Where("id=?", id).First(_p)
	if ret.Error != nil {
		return _p, ret.Error
	}
	return _p, nil
}

// CreatePredicts 新建细胞预测结果，一个很长的数组
func CreatePredicts(predicts []*Predict, pid int64) (e error) {
	logger.Info.Println(len(predicts), time.Now())
	// 删除当前项目的所有预测结果
	db.Where("pid=?", pid).Delete(Predict{})
	sql1 := "INSERT  INTO `c_predict` (`imgid`,`pid`,`x1`,`y1`,`x2`,`y2`,`cellpath`,`predict_score`,`predict_type`,`predict_p1n0`,`true_type`,`true_p1n0`,`vid`,`status`) VALUES "
	sql := sql1
	// 新增预测结果
	_db := db.Begin()
	for index, v := range predicts {
		sql += fmt.Sprintf("(%d,%d,%d,%d,%d,%d,\"%s\",%d,%d,%d,%d,%d,%d,%d)",
			v.ImgID, pid, v.X1, v.Y1, v.X2, v.Y2, v.CellPath, v.PredictScore,
			v.PredictType, v.PredictP1n0, v.TrueType, v.TrueP1n0, v.VID, v.Status)

		if index > 0 && index%5000 == 0 || index == len(predicts)-1 {
			sql += ";"
			ret := _db.Exec(sql)
			if ret.Error != nil {
				logger.Info.Println(ret.Error)
				logger.Info.Println(sql)
			}
			sql = sql1
		} else {
			sql += ","
		}
	}
	_db.Commit()
	logger.Info.Println(time.Now(), len(sql))
	return nil
}

// ListPredict 通过图片ID查找预测
func ListPredict(limit int, skip int, pid int, imgid int, status int) (totalNum int64, p []Predict, e error) {
	var _p []Predict
	var total int64 = 0

	//0 未审核 1 已审核 2 移除 3 管理员已确认 4 未审核+已审核
	if status == 4 {
		var _p2 []Predict
		var total2 int64 = 0
		var _p3 []Predict
		var total3 int64 = 0
		db.Model(&Predict{}).Where("pid=? AND imgid=? AND status=?", pid, imgid, 0).Count(&total2)
		ret := db.Model(&Predict{}).Where("pid=? AND imgid=? AND status=?", pid, imgid, 0).Limit(limit).Offset(skip).Find(&_p2)
		if ret.Error != nil {
			logger.Info.Println(ret.Error)
		}
		db.Model(&Predict{}).Where("pid=? AND imgid=? AND status=?", pid, imgid, 1).Count(&total3)
		ret = db.Model(&Predict{}).Where("pid=? AND imgid=? AND status=?", pid, imgid, 1).Limit(limit).Offset(skip).Find(&_p3)
		if ret.Error != nil {
			logger.Info.Println(ret.Error)
		}
		_p = append(append(_p, _p2...), _p3...)
		total = total + total2 + total3

		return total, _p, ret.Error
	}

	db.Model(&Predict{}).Where("pid=? AND imgid=? AND status=?", pid, imgid, status).Count(&total)
	ret := db.Model(&Predict{}).Where("pid=? AND imgid=? AND status=?", pid, imgid, status).Limit(limit).Offset(skip).Find(&_p)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return total, _p, ret.Error
}

// UpdatePredict 更新审核信息
func UpdatePredict(id int64, trueType int, userid int64) (e error) {
	_, err := FindPredictbyID(id)
	if err != nil {
		return err
	}

	// 审核细胞类型,1到15是细胞类型, 50 阴性 51 阳性 100 未知, 200 不是细胞
	// TODO: 类型计算
	var trueP1n0 int = 0

	// 状态 0 未审核 1 已审核 2 移除 3 管理员确认
	var status int = 1

	ret := db.Model(&Predict{}).Where("id=?", id).Updates(map[string]interface{}{
		"true_type": trueType,
		"true_p1n0": trueP1n0,
		"status":    status,
		"vid":       userid})
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return ret.Error
}

// GetPredictPercentByImgID 根据图片ID返回当前图片以及当前项目的审核进度
func GetPredictPercentByImgID(imgid int64, pid int64, status int) (int, int, int, int) {
	// 项目所有细胞，　项目已经审核的细胞，　当前图片的所有细胞，当前图片已经审核的细胞，
	cntCellsAll, cntCellsVerified, cntImgCellsAll, cntImgCellsVerified := 0, 0, 0, 0
	db.Model(&Predict{}).Where("pid=?", pid).Count(&cntCellsAll)
	db.Model(&Predict{}).Where("pid=? AND status=?", pid, status).Count(&cntCellsVerified)
	db.Model(&Predict{}).Where("pid=? AND imgid=?", pid, imgid).Count(&cntImgCellsAll)
	db.Model(&Predict{}).Where("pid=? AND imgid=? AND status=?", pid, imgid, status).Count(&cntImgCellsVerified)
	return cntCellsAll, cntCellsVerified, cntImgCellsAll, cntImgCellsVerified
}

// GetPredictPercent 更新审核信息时候顺带返回当前图片以及当前项目的审核进度
func GetPredictPercent(id int64, status int) (int, int, int, int) {
	var _p Predict
	// 项目所有细胞，　项目已经审核的细胞，　当前图片的所有细胞，当前图片已经审核的细胞，
	ret := db.Model(&Predict{}).Where("id=?", id).First(&_p)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
		return 0, 0, 0, 0
	}
	return GetPredictPercentByImgID(_p.ImgID, _p.PID, status)
}

// ReviewPredict 管理员检查医生审核过后的信息
func ReviewPredict(id int64, status int) (e error) {
	_, err := FindPredictbyID(id)
	if err != nil {
		return err
	}

	ret := db.Model(&Predict{}).Where("id=?", id).Updates(map[string]interface{}{"status": status})
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return ret.Error
}

// GetPredictByImgID 通过图片ID获得所有的预测，不管审核状态,只看机器预测的结果
func GetPredictByImgID(pid int64, iid int64) (p []Predict, e error) {
	var _p []Predict
	ret := db.Model(&Predict{}).Where("pid=? AND imgid=?", pid, iid).Find(&_p)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	return _p, ret.Error
}

type _predictCount struct {
	ID      int64  `json:"id" `      //ID
	Name    string `json:"name"`     //用户名
	Image   string `json:"image"`    //用户头像的URL
	Status0 int64  `json:"status0" ` //分配给该用户，但是没有审核的细胞个数
	Status1 int64  `json:"status１" ` //用户已审核的细胞个数
}

// PredictCount 用户审核的统计
type PredictCount struct {
	UserInfo []_predictCount `json:"user"` //用户标注信息
}

// GetPredictCount 统计医生审核的总次数
func GetPredictCount() PredictCount {
	type res1 struct {
		Vid int64
	}
	type res2 struct {
		Total int64
	}

	// 检查都有谁做过审核
	vids := make([]res1, 0)
	selector1 := "SELECT vid FROM c_predict GROUP BY vid;"
	ret := db.Raw(selector1).Scan(&vids)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}
	// 依次统计出审核人员的信息,0 未审核 1 已审核 2 移除 3 管理员确认
	pcnt := PredictCount{}
	pcnt.UserInfo = make([]_predictCount, 0)
	for index, v := range vids {
		var total0 res2
		var total1 res2
		var cnt _predictCount
		selector1 := "SELECT count(1) AS total FROM c_predict WHERE vid=? AND status=?;"
		ret := db.Raw(selector1, v.Vid, 0).Scan(&total0)
		if ret.Error != nil {
			logger.Info.Println(ret.Error)
		}
		selector1 = "SELECT count(1) AS total FROM c_predict WHERE vid=? AND status=?;"
		ret = db.Raw(selector1, v.Vid, 1).Scan(&total1)
		if ret.Error != nil {
			logger.Info.Println(ret.Error)
		}
		u, err := FinduserbyID(v.Vid)
		if err != nil {
			cnt.ID = 0
			cnt.Name = fmt.Sprintf("系统%d", index)
			cnt.Image = ""
		} else {
			cnt.ID = u.ID
			cnt.Name = u.Name
			cnt.Image = u.Image
		}
		cnt.Status0 = total0.Total
		cnt.Status1 = total1.Total
		pcnt.UserInfo = append(pcnt.UserInfo, cnt)
	}
	return pcnt
}
