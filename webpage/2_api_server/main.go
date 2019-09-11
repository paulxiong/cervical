package main

import (
	configs "github.com/paulxiong/cervical/webpage/2_api_server/configs"
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
// @description 这是API说明文档，开发服务器才有， 正式部署之后没有.
// @termsOfService http://9200.gpu.raidcdn.cn:9700
// @contact.name API Support
// @contact.url http://9200.gpu.raidcdn.cn:9700
// @contact.email ggxxde@163.com
// @license.name Apache 2.0
// @license.url http://9200.gpu.raidcdn.cn:9700
// @host 9200.gpu.raidcdn.cn:9700
// @BasePath /

func atexit() {
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
			logger.Error.Fatal("Server err: %v", err)
		}
	}
}
