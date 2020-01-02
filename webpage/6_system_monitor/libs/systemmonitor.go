package lib

import (
	smonitor "github.com/lambda-zhang/systemmonitor"
)

// NetIf 网卡信息
type NetIf struct {
	Iface            string `json:"if"`  // 网卡名字
	InKBps           uint64 `json:"ib"`  // 这个时间段网卡接收字节, Bps
	InPackages       uint64 `json:"ip"`  // 这个时间段网卡接收数据包，bpp
	TotalInBytes     uint64 `json:"tib"` // 网卡总共接收多少个字节
	TotalInPackages  uint64 `json:"tip"` // 网卡总共接收多少个数据包
	OutKBps          uint64 `json:"ob"`  // 这个时间段网卡发送字节, Bps
	OutPackages      uint64 `json:"op"`  // 这个时间段网卡发送数据包，bpp
	TotalOutBytes    uint64 `json:"tob"` // 网卡总共发送多少个字节
	TotalOutPackages uint64 `json:"top"` // 网卡总共发送多少个数据包
}

// TCPInfo tcp信息
type TCPInfo struct {
	TCPEstablished uint64 `json:"est"`   // 已经建立连接的TCP/UDP端口
	TCPListen      uint64 `json:"lis"`   // 等待连接的TCP/UDP端口
	TCPConnections uint64 `json:"total"` // TCP/UDP端口总个数
}

// DiskStates 磁盘状态
type DiskStates struct {
	FsSpec               string `json:"spec"`  // 分区设备节点，如/dev/sda1
	FsFile               string `json:"dir"`   // 分区挂载目录
	FsVfstype            string `json:"type"`  // 分区格式
	BytesAll             uint64 `json:"ball"`  // 分区大小(单位字节)
	BytesUsedPermillage  int    `json:"bperm"` // 分区使用率(千分之一, 字节计算)
	InodesAll            uint64 `json:"iall"`  // 分区大小(单位文件节点)
	InodesUsedPermillage int    `json:"iperm"` // 分区使用率(千分之一, 文件节点计算)
}

// ThermalStates 温度状态
type ThermalStates struct {
	Type string
	Temp int64
}

// SysStateInfo 被监控的系统信息
type SysStateInfo struct {
	CPUPermillage int     `json:"cpu"`    // CPU使用率(千分之一, 50 meas 5%)
	Avg1min       float32 `json:"avg1"`   // 1分钟之内CPU负载
	Avg5min       float32 `json:"avg5"`   // 5分钟之内CPU负载
	Avg15min      float32 `json:"avg15"`  // 15分钟之内CPU负载
	NumCPU        int     `json:"numcpu"` // CPU核心数

	MemTotal          uint64 `json:"mt"`    // 总内存大小(单位字节)
	MemAvailable      uint64 `json:"ma"`    // 可用存大小(单位字节)
	MemUsePermillage  int    `json:"mperm"` // 内存使用率(千分之一,50 meas 5%)
	SwapTotal         uint64 `json:"st"`    // 总交换分区大小(单位字节)
	SwapFree          uint64 `json:"sf"`    // 可用交换分区大小(单位字节)
	SwapUsePermillage int    `json:"sperm"` // 交换分区使用率(千分之一, 50 meas 5%)

	Disks map[string]*DiskStates `json:"disks"` // 硬盘分区信息

	Cards map[string]*NetIf `json:"cards"` // 网卡信息
	TCP   TCPInfo           `json:"tcp"`   // TCP/UDP
	TCP6  TCPInfo           `json:"tcp6"`  // TCP/UDP(IPV6)

	Thermal map[string]*ThermalStates `json:"thermal"` // 主板温度信息
}

func callback(sysinfo *smonitor.SysInfo) {
	o := sysinfo.OS
	c := sysinfo.CPU
	m := sysinfo.Mem
	n := sysinfo.Net
	f := sysinfo.Fs
	t := sysinfo.Thermal

	info := SysStateInfo{
		CPUPermillage:     c.CPUPermillage,
		Avg1min:           c.Avg1min,
		Avg5min:           c.Avg5min,
		Avg15min:          c.Avg15min,
		NumCPU:            o.NumCPU,
		MemTotal:          m.MemTotal,
		MemAvailable:      m.MemAvailable,
		MemUsePermillage:  m.MemUsePermillage,
		SwapTotal:         m.SwapTotal,
		SwapFree:          m.SwapFree,
		SwapUsePermillage: m.SwapUsePermillage,
		TCP: TCPInfo{
			TCPConnections: n.TCP.TCPConnections,
			TCPEstablished: n.TCP.TCPEstablished,
			TCPListen:      n.TCP.TCPListen,
		},
		TCP6: TCPInfo{
			TCPConnections: n.TCP6.TCPConnections,
			TCPEstablished: n.TCP6.TCPEstablished,
			TCPListen:      n.TCP6.TCPListen,
		},
	}

	info.Disks = make(map[string]*DiskStates, 0)
	info.Cards = make(map[string]*NetIf, 0)
	info.Thermal = make(map[string]*ThermalStates, 0)

	for _, v := range n.Cards {
		if _, ok := info.Cards[v.Iface]; !ok {
			info.Cards[v.Iface] = &NetIf{}
		}
		info.Cards[v.Iface].Iface = v.Iface
		info.Cards[v.Iface].InKBps = v.InBytes / uint64(sysinfo.PeriodSec) / 1024
		info.Cards[v.Iface].InPackages = v.InPackages
		info.Cards[v.Iface].TotalInBytes = v.TotalInBytes
		info.Cards[v.Iface].TotalInPackages = v.TotalInPackages
		info.Cards[v.Iface].OutKBps = v.OutBytes / uint64(sysinfo.PeriodSec) / 1024
		info.Cards[v.Iface].OutPackages = v.OutPackages
		info.Cards[v.Iface].TotalOutBytes = v.TotalOutBytes
		info.Cards[v.Iface].TotalOutPackages = v.TotalOutPackages
	}

	for _, v := range f.Disks {
		if _, ok := info.Disks[v.FsSpec]; !ok {
			info.Disks[v.FsSpec] = &DiskStates{}
		}
		info.Disks[v.FsSpec].FsSpec = v.FsSpec
		info.Disks[v.FsSpec].FsFile = v.FsFile
		info.Disks[v.FsSpec].FsVfstype = v.FsVfstype
		info.Disks[v.FsSpec].BytesAll = v.BytesAll
		info.Disks[v.FsSpec].BytesUsedPermillage = v.BytesUsedPermillage
		info.Disks[v.FsSpec].InodesAll = v.InodesAll
		info.Disks[v.FsSpec].InodesUsedPermillage = v.InodesUsedPermillage
	}

	for _, v := range t.Thermal {
		if _, ok := info.Thermal[v.Type]; !ok {
			info.Thermal[v.Type] = &ThermalStates{}
		}
		info.Thermal[v.Type].Type = v.Type
		info.Thermal[v.Type].Temp = v.Temp
	}
	httpPostJSON(info)
}

// NewSystemMonitor 新建系统监视器
func NewSystemMonitor() *smonitor.SysInfo {
	periodSec := 10
	sm := smonitor.New(periodSec, callback)
	sm.OSEn = true
	sm.CPUEn = true
	sm.MemEn = true
	sm.NetEn = true
	sm.FsEn = true
	sm.ThermalEn = true
	return sm
}
