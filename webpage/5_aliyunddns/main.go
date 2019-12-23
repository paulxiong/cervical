package main

import (
	"encoding/json"
	"flag"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"path"
	"strings"

	"github.com/ahmetb/go-linq/v3"
	"github.com/aliyun/alibaba-cloud-sdk-go/services/alidns"
	"github.com/robfig/cron"
)

// GetPublicIPURL 公网 IP 查询站点的 URL 地址。
const GetPublicIPURL = "http://members.3322.org/dyndns/getip"

type commandModel struct {
	FilePath *string
	Interval *int
}

type configurationModel struct {
	AccessID   string            // 阿里云的 Access Id
	AccessKey  string            // 阿里云的 Access Key
	MainDomain string            // 需要更新的主域名，例如 sample.com
	SubDomains *[]subDomainModel // 需要更新的具体子域名。
	PublicIP   string            `json:"-"` // 公网IP
}

type subDomainModel struct {
	Type     string `json:"Type"`      // 子域名记录的类型。
	Name     string `json:"SubDomain"` // 子域名的名称，例如 sub1.sample.com
	Interval int    `json:"Interval"`  // 子域名记录的 TTL 时间，单位是秒
	UpdateAt int    `json:"-"`         // 上次更新域名的时间,ts
}

var commandmodel commandModel
var configmodel configurationModel

func initCommandModel() {
	commandmodel.FilePath = flag.String("f", "", "指定自定义的配置文件，请传入配置文件的路径。")
	commandmodel.Interval = flag.Int("i", 0, "指定程序的自动检测周期，单位是秒。")

	flag.Parse()
}

func loadConfig() {
	var configFile string
	if *commandmodel.FilePath == "" {
		dir, _ := os.Getwd()
		configFile = path.Join(dir, "settings.json")
	} else {
		configFile = *commandmodel.FilePath
	}

	// 打开配置文件，并进行反序列化。
	f, err := os.Open(configFile)
	if err != nil {
		log.Fatalf("无法打开文件：%s", err)
		os.Exit(-1)
	}
	defer f.Close()
	data, _ := ioutil.ReadAll(f)

	if err := json.Unmarshal(data, &configmodel); err != nil {
		log.Fatalf("数据反序列化失败：%s", err)
		os.Exit(-1)
	}
}

func getPublicIP() string {
	resp, err := http.Get(GetPublicIPURL)
	if err != nil {
		log.Printf("获取公网 IP 出现错误，错误信息：%s", err)
		return ""
	}
	defer resp.Body.Close()

	bytes, _ := ioutil.ReadAll(resp.Body)

	return strings.Replace(string(bytes), "\n", "", -1)
}

func getSubDomains() []alidns.Record {
	client, err := alidns.NewClientWithAccessKey("cn-hangzhou", configmodel.AccessID, configmodel.AccessKey)

	request := alidns.CreateDescribeDomainRecordsRequest()
	request.Scheme = "https"

	request.DomainName = configmodel.MainDomain

	response, err := client.DescribeDomainRecords(request)
	if err != nil {
		log.Println(err.Error())
	}

	// 过滤符合条件的子域名信息。
	var queryResult []alidns.Record
	linq.From(response.DomainRecords.Record).Where(func(c interface{}) bool {
		return linq.From(*configmodel.SubDomains).Select(func(x interface{}) interface{} {
			return x.(subDomainModel).Name
		}).Contains(c.(alidns.Record).RR)
	}).ToSlice(&queryResult)

	return queryResult
}

func updateSubDomain(subDomain *alidns.Record) {
	client, err := alidns.NewClientWithAccessKey("cn-shenzhen", configmodel.AccessID, configmodel.AccessKey)

	request := alidns.CreateUpdateDomainRecordRequest()
	request.Scheme = "https"
	request.RecordId = subDomain.RecordId
	request.RR = subDomain.RR
	request.Type = subDomain.Type
	request.Value = subDomain.Value

	_, err = client.UpdateDomainRecord(request)
	if err != nil {
		log.Print(err.Error())
	}
}
func timerhandler() {
	publicIP := getPublicIP()
	if len(publicIP) < 1 {
		log.Printf("获取公网IP失败")
		return
	}

	if configmodel.PublicIP == publicIP {
		return
	}
	log.Printf("公网IP变了，需要更新dns")
	configmodel.PublicIP = publicIP

	subDomains := getSubDomains()
	if len(subDomains) < 1 {
		log.Printf("没发现子域名，请修改配置文件")
		return
	}
	for _, sub := range subDomains {
		if sub.Value != configmodel.PublicIP {
			sub.Value = configmodel.PublicIP
			updateSubDomain(&sub)
			log.Printf("域名更新 %s  %s", sub.DomainName, configmodel.PublicIP)
		} else {
			log.Printf("阿里云记录的IP和本地相同，不需要更新 %s", sub.DomainName)
		}
	}
	return
}

func main() {
	initCommandModel()
	loadConfig()

	c := cron.New()
	spec := "*/5 * * * * ?" //每隔5秒扫描一次公网IP
	c.AddFunc(spec, timerhandler)
	c.Start()

	select {}
}
