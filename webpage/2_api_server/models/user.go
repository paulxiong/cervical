package models

import (
	e "github.com/paulxiong/cervical/webpage/2_api_server/error"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"

	"time"

	"github.com/gin-gonic/gin"
	"github.com/jinzhu/gorm"
	"github.com/pkg/errors"
	"golang.org/x/crypto/bcrypt"
)

// UserType 用户类型 gorm 用 tag 的方式来标识 mysql 里面的约束
type UserType struct {
	ID          int       `json:"id"           gorm:"column:id"`          //"ID"
	Name        string    `json:"name"         gorm:"column:name"`        //"类型名称"
	Description string    `json:"description"  gorm:"column:description"` //"描述"
	Image       string    `json:"image"        gorm:"column:image"`       //"类型图片"
	CreatedAt   time.Time `json:"created_at"   gorm:"column:created_at"`  //"创建时间"
	UpdatedAt   time.Time `json:"updated_at"   gorm:"column:updated_at"`  //"更新时间"
}

// BeforeCreate insert 之前的hook
func (u *UserType) BeforeCreate(scope *gorm.Scope) error {
	if u.CreatedAt.IsZero() {
		u.CreatedAt = time.Now()
	}
	if u.UpdatedAt.IsZero() {
		u.UpdatedAt = time.Now()
	}
	return nil
}

// NewUserType 新建用户类型
func NewUserType(nut *UserType) error {
	ut := UserType{}
	ret := db.Model(&UserType{}).Where("name = ?", nut.Name).First(&ut)
	if ret.Error != nil {
		ret2 := db.Model(&UserType{}).Create(nut)
		return ret2.Error
	}
	return ret.Error
}

// UserTypeInit 初始化时候默认新建的用户类型
func UserTypeInit() error {
	uts := [...]UserType{
		UserType{ID: 1, Name: "超级管理员", Description: "拥有所有权限", Image: ""},
		UserType{ID: 1000, Name: "普通用户", Description: "使用者", Image: ""},
	}
	for _, ut := range uts {
		err := NewUserType(&ut)
		if err != nil {
			logger.Info.Println(err)
		}
	}
	return nil
}

// User 用户信息
type User struct {
	ID           int64     `json:"id"           gorm:"column:id"`           //ID
	Mobile       string    `json:"mobile"       gorm:"column:mobile"`       //手机号
	Email        string    `json:"email"        gorm:"column:email"`        //邮箱
	Name         string    `json:"name"         gorm:"column:name"`         //用户名
	Image        string    `json:"image"        gorm:"column:image"`        //用户头像的URL
	TypeID       int       `json:"type_id"      gorm:"column:type_id"`      //用户类型ID
	Password     string    `json:"-"            gorm:"column:password"`     //密码
	Introduction string    `json:"introduction" gorm:"column:introduction"` //简介
	Roles        []string  `json:"roles"        gorm:"-"`                   //密码
	CreatedAt    time.Time `json:"created_at"   gorm:"column:created_at"`   //创建时间
	UpdatedAt    time.Time `json:"updated_at"   gorm:"column:updated_at"`   //更新时间
}

// BeforeCreate insert之前的hook
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

// AfterFind 返回用户角色, 1 超级管理员 1000 普通用户
func (u *User) AfterFind(scope *gorm.Scope) error {
	if u.TypeID == 1 {
		u.Roles = []string{"admin"}
	} else if u.TypeID == 1000 {
		u.Roles = []string{"user"}
	}

	return nil
}

// FinduserbyID 通过用户ID查找用户
func FinduserbyID(uid int64) (*User, error) {
	user := User{}
	ret := db.Model(&user).Where("id=?", uid).First(&user)
	if ret.Error != nil {
		return &user, ret.Error
	}
	return &user, nil
}

// FinduserbyMobile 通过手机号查找用户
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

// Finduserbyname 通过用户名查找用户
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

// Finduserbyemail 通过邮箱查找用户
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

// Newuser 新建用户
func (u *User) Newuser() error {
	ret := db.Create(u)
	if ret.Error != nil {
		return ret.Error
	}
	return nil
}

// UserLogined 用户登录之后更新信息
func (u *User) UserLogined() error {
	lu := &User{UpdatedAt: time.Now()}
	db.Model(&u).Updates(lu)

	ret := db.Model(u).Where("id=?", u.ID).First(u)
	u.Password = ""
	return ret.Error
}

// CheckUserExist 检查这个用户是否存在
func (u *User) CheckUserExist() (user *User, errcode int) {
	user, err := u.Finduserbyname()
	if err == nil && user != nil {
		logger.Warning.Println("UserExisted " + u.Name)
		return user, e.StatusRegisterUserExisted70
	}
	user, err = u.FinduserbyMobile()
	if err == nil && user != nil {
		logger.Warning.Println("MobileExisted " + u.Mobile)
		return user, e.StatusRegisterMobileExisted76
	}
	user, err = u.Finduserbyemail()
	if err == nil && user != nil {
		logger.Warning.Println("checkUserExist " + u.Email)
		return user, e.StatusRegisterEmailExisted71
	}
	return nil, e.StatusSucceed
}

// CheckUserExist2 检查这个用户是否存在
func CheckUserExist2(name string, email string, mobile string) (user *User, errcode int) {
	u := &User{Name: name}
	user, err := u.Finduserbyname()
	if err == nil && user != nil {
		return user, e.StatusRegisterUserExisted70
	}

	u = &User{Mobile: mobile}
	user, err = u.FinduserbyMobile()
	if err == nil && user != nil {
		logger.Warning.Println("MobileExisted " + u.Mobile)
		return user, e.StatusRegisterMobileExisted76
	}

	u = &User{Email: email}
	user, err = u.Finduserbyemail()
	if err == nil && user != nil {
		logger.Warning.Println("EmailExisted " + u.Email)
		return user, e.StatusRegisterEmailExisted71
	}
	return nil, e.StatusSucceed
}

// GetUserFromContext 从请求上下文获得用户信息
func GetUserFromContext(c *gin.Context) (*User, bool) {
	userTmp, exists := c.Get("user")
	if exists == true && userTmp != nil {
		userTmp2 := userTmp.(*User)
		return userTmp2, exists
	}
	return &User{}, exists
}

// SaveUsertoContext 把用户信息存到请求上下文
func SaveUsertoContext(c *gin.Context, u *User) {
	user, err := FinduserbyID(u.ID)
	if err == nil {
		user.Password = ""
		c.Set("user", user)
	} else {
		c.Set("user", u)
	}
}

// UserLists 按顺序列出所有用户的信息
func UserLists(limit int, skip int, order int) (users []User, t int, err error) {
	var us []User
	var total int = 0
	db.Model(&User{}).Count(&total)

	orderStr := "created_at DESC"
	if order == 0 { //order, default 1, 1倒序，0顺序
		orderStr = "created_at ASC"
	}
	ret := db.Model(&User{}).Order(orderStr).Limit(limit).Offset(skip).Find(&us)
	if ret.Error != nil {
		logger.Info.Println(users)
	}
	return us, total, ret.Error
}

// UpdateUserInfo 更新用户的信息
func (u *User) UpdateUserInfo() (err error) {
	var updateu map[string]interface{}
	updateu = make(map[string]interface{})

	if u.Mobile != "" {
		updateu["mobile"] = u.Mobile
	}
	if u.Email != "" {
		updateu["email"] = u.Email
	}
	if u.Name != "" {
		updateu["name"] = u.Name
	}
	if u.Image != "" {
		updateu["image"] = u.Image
	}
	if u.Introduction != "" {
		updateu["introduction"] = u.Introduction
	}
	if len(updateu) < 1 {
		return nil
	}

	ret := db.Model(u).Where("id=?", u.ID).Updates(updateu)
	if ret.Error != nil {
		logger.Info.Println(ret.Error)
	}

	return ret.Error
}
