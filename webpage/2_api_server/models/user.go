package models

import (
	e "../error"
	logger "../log"

	"time"

	"github.com/gin-gonic/gin"
	"github.com/jinzhu/gorm"
	"github.com/pkg/errors"
	"golang.org/x/crypto/bcrypt"
)

// gorm 用 tag 的方式来标识 mysql 里面的约束
type UserType struct {
	Id          int       `json:"id"           gorm:"column:id"           "ID"`
	Name        string    `json:"name"         gorm:"column:name"         "类型名称"`
	Description string    `json:"description"  gorm:"column:description"  "描述"`
	Image       string    `json:"image"        gorm:"column:image"        "类型图片"`
	CreatedAt   time.Time `json:"created_at"   gorm:"column:created_at"   "创建时间"`
	UpdatedAt   time.Time `json:"updated_at"   gorm:"column:updated_at"   "更新时间"`
}

func (u *UserType) BeforeCreate(scope *gorm.Scope) error {
	if u.CreatedAt.IsZero() {
		u.CreatedAt = time.Now()
	}
	if u.UpdatedAt.IsZero() {
		u.UpdatedAt = time.Now()
	}
	return nil
}

func NewUserType(nut *UserType) error {
	ut := UserType{}
	ret := db.Model(&UserType{}).Where("name = ?", nut.Name).First(&ut)
	if ret.Error != nil {
		ret2 := db.Model(&UserType{}).Create(nut)
		return ret2.Error
	}
	return ret.Error
}

func UserTypeInit() error {
	uts := [...]UserType{
		UserType{Id: 1, Name: "超级管理员", Description: "拥有所有权限", Image: ""},
		UserType{Id: 1000, Name: "普通用户", Description: "使用者", Image: ""},
	}
	for _, ut := range uts {
		err := NewUserType(&ut)
		if err != nil {
			logger.Info.Println(err)
		}
	}
	return nil
}

type User struct {
	Id        int64     `json:"id"                 gorm:"column:id"          "ID"`
	Mobile    string    `json:"mobile"             gorm:"column:mobile"      "手机号"`
	Email     string    `json:"email"              gorm:"column:email"       "邮箱"`
	Name      string    `json:"name"               gorm:"column:name"        "用户名"`
	Image     string    `json:"image"              gorm:"column:image"       "用户头像"`
	TypeId    int       `json:"type_id"            gorm:"column:type_id"     "用户类型"`
	Password  string    `json:"-"                  gorm:"column:password"    "密码"`
	CreatedAt time.Time `json:"created_at"         gorm:"column:created_at"  "创建时间"`
	UpdatedAt time.Time `json:"updated_at"         gorm:"column:updated_at"  "更新时间"`
}

func (u *User) BeforeCreate(scope *gorm.Scope) error {
	if u.CreatedAt.IsZero() {
		u.CreatedAt = time.Now()
	}
	if u.UpdatedAt.IsZero() {
		u.UpdatedAt = time.Now()
	}
	hash, err := bcrypt.GenerateFromPassword([]byte(u.Password), bcrypt.DefaultCost)
	if err != nil {
		return err
	}
	u.Password = string(hash)
	return nil
}

func Getallusers() {
	var limit int = 10
	var users []User
	ret := db.Order("id desc").Limit(limit).Find(&users)
	if ret.Error != nil {
		logger.Info.Println(users)
	}
}

func (u *User) FinduserbyId() (*User, error) {
	user := &User{}
	ret := db.First(user, u.Id)
	if ret.Error != nil {
		return user, ret.Error
	}
	return user, nil
}

func (u *User) FinduserbyMobile() (*User, error) {
	mobile := u.Mobile
	if mobile == "" {
		return nil, errors.Wrap(nil, "query error, mobile: "+mobile)
	}
	user := new(User)
	ret := db.Where("Mobile = ?", mobile).First(&user)
	if ret.Error != nil {
		return user, ret.Error
	}
	return user, nil
}

func (u *User) Finduserbyname() (*User, error) {
	name := u.Name
	if name == "" {
		return nil, errors.Wrap(nil, "query error, name: "+name)
	}
	user := new(User)
	ret := db.Where("Name = ?", name).First(&user)
	if ret.Error != nil {
		return user, ret.Error
	}
	return user, nil
}

func (u *User) Finduserbyemail() (*User, error) {
	email := u.Email
	if email == "" {
		return nil, errors.Wrap(nil, "query error, email: "+email)
	}
	user := new(User)
	ret := db.Where("Email = ?", email).First(&user)
	if ret.Error != nil {
		return user, ret.Error
	}
	return user, nil
}

func (u *User) Newuser() error {
	ret := db.Create(u)
	if ret.Error != nil {
		return ret.Error
	}
	return nil
}

func (u *User) UserLogined() error {
	lu := &User{UpdatedAt: time.Now()}
	db.Model(&u).Updates(lu)

	ret := db.First(u, u.Id)
	u.Password = ""
	return ret.Error
}

func (u *User) CheckUserExist() (user *User, errcode int) {
	user, err := u.Finduserbyname()
	if err == nil && user != nil {
		logger.Warning.Println("UserExisted " + u.Name)
		return user, e.StatusRegisterUserExisted
	}
	user, err = u.FinduserbyMobile()
	if err == nil && user != nil {
		logger.Warning.Println("MobileExisted " + u.Mobile)
		return user, e.StatusRegisterMobileExisted
	}
	user, err = u.Finduserbyemail()
	if err == nil && user != nil {
		logger.Warning.Println("checkUserExist " + u.Email)
		return user, e.StatusRegisterEmailExisted
	}
	return nil, e.StatusSucceed
}

func CheckUserExist2(name string, email string, mobile string) (user *User, errcode int) {
	u := &User{Name: name}
	user, err := u.Finduserbyname()
	if err == nil && user != nil {
		logger.Warning.Println("UserExisted " + u.Name)
		return user, e.StatusRegisterUserExisted
	}

	u = &User{Mobile: mobile}
	user, err = u.FinduserbyMobile()
	if err == nil && user != nil {
		logger.Warning.Println("MobileExisted " + u.Mobile)
		return user, e.StatusRegisterMobileExisted
	}

	u = &User{Email: email}
	user, err = u.Finduserbyemail()
	if err == nil && user != nil {
		logger.Warning.Println("EmailExisted " + u.Email)
		return user, e.StatusRegisterEmailExisted
	}
	return nil, e.StatusSucceed
}

func GetUserFromContext(c *gin.Context) (*User, bool) {
	user_tmp, exists := c.Get("user")
	if exists == true && user_tmp != nil {
		user_tmp2 := user_tmp.(*User)
		user, err := user_tmp2.FinduserbyId()
		user.Password = ""
		if err == nil {
			return user, exists
		}
		return &User{}, false
	}
	return &User{}, exists
}
func SaveUsertoContext(c *gin.Context, u *User) {
	c.Set("user", u)
}

type UserHistory struct {
	Id        int64     `json:"id"           gorm:"column:id"           "ID"`
	UserId    int64     `json:"uid"          gorm:"column:uid"          "用户ID"`
	Path      string    `json:"path"         gorm:"column:path"         "访问的页面路径"`
	CreatedAt time.Time `json:"created_at"   gorm:"column:updated_at"   "创建时间"`
}
