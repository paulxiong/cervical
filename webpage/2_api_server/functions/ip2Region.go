package function

import (
	"errors"
	"fmt"

	"github.com/lionsoul2014/ip2region/binding/golang/ip2region"
	m "github.com/paulxiong/cervical/webpage/2_api_server/models"
)

//Region ip地址转位置信息
var Region *ip2region.Ip2Region

//IP2Region ip地址转位置信息
func IP2Region(ip string) (m.Region, error) {
	var r m.Region
	if Region == nil {
		return r, errors.New("Ip2Region not inited")
	}

	if len(ip) < 7 || len(ip) > 15 {
		return r, errors.New("invalied ip")
	}

	city, err := Region.MemorySearch(ip)
	if err != nil {
		return r, err
	}
	r.ID = city.CityId
	r.Country = city.Country
	r.Region = city.Region
	r.Province = city.Province
	r.City = city.City
	r.ISP = city.ISP

	if r.ID == 0 { //局域网
		r.ID = -1
	}
	if r.Country == "0" {
		r.Country = ""
	}
	if r.Region == "0" {
		r.Region = ""
	}
	if r.Province == "0" {
		r.Province = ""
	}
	if r.City == "0" {
		r.City = ""
	}
	if r.ISP == "0" {
		r.ISP = ""
	}
	return r, nil
}

func init() {
	var err error
	Region, err = ip2region.New("ip2region.db")
	if err != nil {
		fmt.Println(err)
		//return
	}
}
