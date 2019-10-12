package main

import (
	configs "github.com/paulxiong/cervical/webpage/2_api_server/configs"
	f "github.com/paulxiong/cervical/webpage/2_api_server/functions"
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
	"github.com/paulxiong/cervical/webpage/2_api_server/routes"

	"fmt"
	"net"
	"net/http"
	"os"
	"syscall"
	"time"

	"github.com/fvbock/endless"

	_ "github.com/paulxiong/cervical/webpage/2_api_server/docs"
)

// @title API说明
// @version 1.0
// @description 这是API说明文档，开发服务器才有， 正式部署之后没有。
// @description 认证时候填 "token eyJhbGciOiJIU..." (注意token后面有个空格， token向管理员申请)
// @description 网络请求每次返回code比如200、404或者401。返回内容是JSON {status: 状态码, data: 具体内容}
// @termsOfService http://dev.medical.raidcdn.cn:3000
// @contact.name API Support
// @contact.url http://dev.medical.raidcdn.cn:3000
// @contact.email ggxxde@163.com
// @license.name Apache 2.0
// @license.url http://dev.medical.raidcdn.cn:3000
// @host dev.medical.raidcdn.cn:3000
// @BasePath /

// JWT 认证, 认证时候填 token eyJhbGciOiJIU...(注意token后面有个空格)
// @securityDefinitions.apikey ApiKeyAuth
// @in header
// @name Authorization

func atexit() {
	f.Region.Close()
}

func printlistenaddr(port string) {
	addrs, err := net.InterfaceAddrs()
	if err != nil {
		panic(err)
	}
	for _, address := range addrs {
		if ipnet, ok := address.(*net.IPNet); ok && !ipnet.IP.IsLoopback() {
			if ipnet.IP.To4() != nil {
				logger.Warning.Printf("http://%s%s", ipnet.IP.String(), port)
			}
		}
	}
}

func main() {
	release := os.Getenv("RELEASE")
	r := routes.Router()

	port := configs.Server.Port
	endPoint := fmt.Sprintf(":%d", port)
	printlistenaddr(endPoint)

	defer atexit()

	if release != "true" {
		logger.Info.Printf("port on ==> %d", port)
		if err := http.ListenAndServe(endPoint, r); err != nil {
			logger.Error.Fatal(err)
		}
	} else {
		endless.DefaultReadTimeOut = 1 * time.Second
		endless.DefaultWriteTimeOut = 1 * time.Second
		endless.DefaultMaxHeaderBytes = 1 << 20

		server := endless.NewServer(endPoint, r)
		server.BeforeBegin = func(add string) {
			logger.Info.Printf("Actual pid is %d", syscall.Getpid())
		}

		logger.Info.Printf("port on ==> %d", port)

		err := server.ListenAndServe()
		if err != nil {
			logger.Error.Fatal("Server err: ", err)
		}
	}
}
