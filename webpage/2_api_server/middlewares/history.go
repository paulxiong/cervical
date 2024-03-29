package middlewares

import (
	"strings"
	"time"

	"github.com/gin-gonic/gin"

	f "github.com/paulxiong/cervical/webpage/2_api_server/functions"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	m "github.com/paulxiong/cervical/webpage/2_api_server/models"
)

//History 用户访问记录的中间件
func History() gin.HandlerFunc {
	return func(c *gin.Context) {
		path := c.Request.URL.Path
		skippath := [...]string{
			"/user/accesslog",
			"/swagger/index.html",
			"/api1/ping",
			"/api1/job",
			"/api1/jobresult",
			"/api1/jobpercent",
			"/api1/upload",
			"/imgs",
			"/api1/smonitor",
			"/api1/uploaddir",
		}
		skippath2 := [...]string{
			"/imgs",
		}
		var skip map[string]struct{}

		if length := len(skippath); length > 0 {
			skip = make(map[string]struct{}, length)
			for _, _path := range skippath {
				skip[_path] = struct{}{}
			}
		}
		//判断哪些API访问不记录,固定路由
		if _, ok := skip[path]; ok {
			return
		}
		//判断哪些API访问不记录,动态路由
		for _, _path := range skippath2 {
			if strings.HasPrefix(path, _path) {
				return
			}
		}

		// Start timer
		start := time.Now().UnixNano()
		raw := c.Request.URL.RawQuery

		// Process request
		c.Next()

		clientIP := c.ClientIP()
		method := c.Request.Method
		statusCode := c.Writer.Status()
		bodySize := c.Writer.Size()
		end := time.Now().UnixNano()

		u, _ := m.GetUserFromContext(c)
		operationlog := m.Operationlog{
			ID:       0,
			UserID:   u.ID,
			Path:     path,
			Query:    raw,
			Method:   method,
			IP:       clientIP,
			RegionID: "",
			ISP:      "",
			Input:    c.Request.PostForm.Encode(),
			UA:       c.Request.UserAgent(),
			Code:     statusCode,
			Cost:     (end - start) / 1000,
			BodySize: bodySize,
			Referer:  c.Request.Referer(),
		}

		region, err := f.IP2Region(clientIP)
		if err == nil {
			err2 := region.NewRegion()
			if err2 == nil {
				operationlog.RegionID = region.ID
				operationlog.ISP = region.ISP
			} else {
				logger.Info(err2)
			}
		} else {
			logger.Info(err)
		}

		err3 := operationlog.NewOperationlog()
		if err3 != nil {
			logger.Info(err3)
		}

		// 注意： 这里只有记录错误日志的时候需要
		if path == "/api1/errorlog" && method == "POST" {
			elid, _ := m.GetErrorlogIDFromContext(c)
			m.UpdateErrorlog(elid, operationlog.ID)
		}
	}
}
