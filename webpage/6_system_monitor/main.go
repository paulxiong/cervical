package main

import (
	"fmt"
	"log"
	"os"

	"github.com/kardianos/service"
	smonitor "github.com/lambda-zhang/systemmonitor"
	lib "github.com/paulxiong/cervical/webpage/6_system_monitor/libs"
)

var sm *smonitor.SysInfo = nil

var serviceConfig = &service.Config{
	Name:        "SystemMonitor",
	DisplayName: "System monitor service Display Name",
	Description: "System monitor service description",
}

// Program 服务的启动和停止
type Program struct{}

// Start 开始服务
func (p *Program) Start(s service.Service) error {
	sm = lib.NewSystemMonitor()
	log.Println("开始服务")
	go p.run()
	return nil
}

// Stop 停止服务
func (p *Program) Stop(s service.Service) error {
	if sm != nil {
		sm.Stop()
	}
	log.Println("停止服务")
	return nil
}

func (p *Program) run() {
	// 此处编写具体的服务代码
	if sm != nil {
		sm.Start()
	}
}

func main() {
	// 构建服务对象
	prog := &Program{}
	s, err := service.New(prog, serviceConfig)
	if err != nil {
		log.Fatal(err)
	}

	// 用于记录系统日志
	logger, err := s.Logger(nil)
	if err != nil {
		log.Fatal(err)
	}

	if len(os.Args) < 2 {
		err = s.Run()
		if err != nil {
			logger.Error(err)
		}
		return
	}

	cmd := os.Args[1]

	if cmd == "install" {
		err = s.Install()
		if err != nil {
			log.Fatal(err)
		}
		fmt.Println("安装成功")
	}
	if cmd == "uninstall" {
		err = s.Uninstall()
		if err != nil {
			log.Fatal(err)
		}
		fmt.Println("卸载成功")
	}
}
