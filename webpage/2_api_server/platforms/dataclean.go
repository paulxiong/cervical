package platforms

/*整理数据库才用，平时不用*/

import (
	configs "github.com/paulxiong/cervical/webpage/2_api_server/configs"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"

	"crypto/sha1"
	"fmt"
	"io"
	"strings"

	"github.com/qiniu/api.v7/auth/qbox"
	"github.com/qiniu/api.v7/storage"
)

var (
	bucket        string = configs.Qiniu.Bucket
	ossHost       string = "http://km.raidcdn.cn/"
	prefix        string = "img/"
	bucketManager *storage.BucketManager
)

// getSHA1StringOfUrl 计算字符串的SHA
func getSHA1StringOfURL(data string) string {
	t := sha1.New()
	io.WriteString(t, data)
	return fmt.Sprintf("%x", t.Sum(nil))
}

// QiniuInit 初始化七牛云的配置
func QiniuInit() {
	if len(configs.Qiniu.AccessKey) != 40 || len(configs.Qiniu.SecretKey) != 40 {
		logger.Error.Println("invalied Qiniu.AccessKey/Qiniu.SecretKey")
		return
	}
	mac := qbox.NewMac(configs.Qiniu.AccessKey, configs.Qiniu.SecretKey)
	cfg := storage.Config{UseHTTPS: false}
	bucketManager = storage.NewBucketManager(mac, &cfg)

	//测试一下是否可用
	prefix, delimiter, marker, limit := "", "", "", 1
	_, _, _, _, err := bucketManager.ListFiles(bucket, prefix, delimiter, marker, limit)
	if err != nil {
		logger.Error.Println("list error,", err)
	}

	// dataCleanChoiceQuestion()
}

// UploadImageByURL 直接传入url，七牛下级下载之后返回key
func UploadImageByURL(url string) (newurl string, e error) {
	key := prefix + getSHA1StringOfURL(url)
	fetchRet, err := bucketManager.Fetch(url, bucket, key)
	if err != nil {
		logger.Error.Println("fetch error,", err, fetchRet)
		return "", err
	}
	return (ossHost + key), err
}

// findURLLists 拿出所有的img标签
func findURLLists(content string, originsite string) ([]string, int) {
	var start, end int = 0, 0
	var ret []string = make([]string, 0)
	var str string = content

	// 这个字符串的img url 必须是原网站的
	start = strings.Index(content, originsite)
	if start < 0 {
		return ret, len(ret)
	}
	for {
		start = strings.Index(str, "<img src")
		if start < 0 {
			break
		}
		end = strings.Index(str[start:], "/>")
		if end < 0 {
			break
		}
		end = start + end
		if start >= end {
			logger.Info.Println(str, start, end)
			break
		}
		ret = append(ret, str[start:end+2])
		str = str[end+2:]
	}
	return ret, len(ret)
}

// getUrlfromString 拿出标签里面的url
func getUrlfromString(content string) string {
	var start int = 0
	var ret string
	start = strings.Index(content, "http")
	if start < 0 {
		return ret
	}
	s := strings.Split(content[start:], " ")
	s1 := strings.Replace(s[0], `"`, "", -1)
	s1 = strings.Replace(s1, `/>`, "", -1)
	return s1
}

func replaceWithQiniuURL(old string) (string, int) {
	var retstr string = old
	var originsite string = "21cnjy"
	arr, cnt := findURLLists(old, originsite)
	if cnt > 0 {
		for _, img := range arr {
			oldurl := getUrlfromString(img)
			newurl, err := UploadImageByURL(oldurl)
			if err != nil {
				logger.Info.Println(old, oldurl)
				continue
			}
			retstr = strings.Replace(retstr, oldurl, newurl, -1)
		}
	}
	return retstr, cnt
}

/*
func dataCleanChoiceQuestion() {
	var limit int = 200
	var skip int64 = 0
	var count int64 = 0
	for {
		var cqs []ChoiceQuestion
		ret := db.Model(&ChoiceQuestion{}).Order("id").Limit(limit).Offset(skip).Find(&cqs)
		if ret.Error != nil || len(cqs) < 1 {
			logger.Info.Println(ret.Error, count)
			break
		}

		var updatecqs []ChoiceQuestion = make([]ChoiceQuestion, 0)
		for _, cq := range cqs {
			count++
			Question, cnt1 := replaceWithQiniuUrl(cq.Question)
			OptionA, cnt2 := replaceWithQiniuUrl(cq.OptionA)
			OptionB, cnt3 := replaceWithQiniuUrl(cq.OptionB)
			OptionC, cnt4 := replaceWithQiniuUrl(cq.OptionC)
			OptionD, cnt5 := replaceWithQiniuUrl(cq.OptionD)
			OptionE, cnt6 := replaceWithQiniuUrl(cq.OptionE)
			OptionF, cnt7 := replaceWithQiniuUrl(cq.OptionF)
			OptionG, cnt8 := replaceWithQiniuUrl(cq.OptionG)
			OptionH, cnt9 := replaceWithQiniuUrl(cq.OptionH)
			Answer, cnt10 := replaceWithQiniuUrl(cq.Answer)
			Analysis, cnt11 := replaceWithQiniuUrl(cq.Analysis)
			SubQuestion, cnt12 := replaceWithQiniuUrl(cq.SubQuestion)

			changed := cnt1 + cnt2 + cnt3 + cnt4 + cnt5 + cnt6 + cnt7 + cnt8 + cnt9 + cnt10 + cnt11 + cnt12
			if changed == 0 {
				continue
			}
			cq.Question = Question
			cq.OptionA = OptionA
			cq.OptionB = OptionB
			cq.OptionC = OptionC
			cq.OptionD = OptionD
			cq.OptionE = OptionE
			cq.OptionF = OptionF
			cq.OptionG = OptionG
			cq.OptionH = OptionH
			cq.Answer = Answer
			cq.Analysis = Analysis
			cq.SubQuestion = SubQuestion
			cq.Type = 1
			logger.Info.Println("updated:", cq.Id, changed, skip)
			updatecqs = append(updatecqs, cq)
		}

		if len(updatecqs) > 0 {
			UpdateChoiceQuestions(updatecqs)
		}

		skip = count
	}
}
*/
