#### 1 安装 golang

#### 2 本地运行源码
```
$ go run main.go
```

#### 3 编译二进制
```
$ go build -o main.exe main.go
```

#### 4 前台执行二进制
```
$ ./main.exe
2020/01/03 09:14:06 开始服务
```

#### 5 ubuntu上安装为后台服务
```
$ sudo ./main.exe install
安装成功

$ ls /etc/systemd/system/SystemMonitor.service -h
/etc/systemd/system/SystemMonitor.service
```

#### 6 服务启动，停止，状态
```
$ systemctl status SystemMonitor
● SystemMonitor.service - System monitor service description
   Loaded: loaded (/etc/systemd/system/SystemMonitor.service; enabled; vendor preset: enabled)
   Active: inactive (dead)

$ systemctl start SystemMonitor
$ systemctl status SystemMonitor
● SystemMonitor.service - System monitor service description
   Loaded: loaded (/etc/systemd/system/SystemMonitor.service; enabled; vendor preset: enabled)
   Active: active (running) since 五 2020-01-03 09:17:24 CST; 3s ago
 Main PID: 7100 (main.exe)
    Tasks: 9
   Memory: 1.2M
      CPU: 3ms
   CGroup: /system.slice/SystemMonitor.service
           └─7100 /data2/ai/cervical.git/webpage/6_system_monitor/main.exe

1月 03 09:17:24 pc systemd[1]: Started System monitor service description.
1月 03 09:17:24 pc main.exe[7100]: 2020/01/03 09:17:24 开始服务

$ systemctl stop SystemMonitor
$ systemctl status SystemMonitor
● SystemMonitor.service - System monitor service description
   Loaded: loaded (/etc/systemd/system/SystemMonitor.service; enabled; vendor preset: enabled)
   Active: inactive (dead) since 五 2020-01-03 09:18:03 CST; 6s ago
  Process: 7100 ExecStart=/data2/ai/cervical.git/webpage/6_system_monitor/main.exe (code=exited, status=0/SUCCESS)
 Main PID: 7100 (code=exited, status=0/SUCCESS)

1月 03 09:17:24 pc systemd[1]: Started System monitor service description.
1月 03 09:17:24 pc main.exe[7100]: 2020/01/03 09:17:24 开始服务
1月 03 09:18:03 pc systemd[1]: Stopping System monitor service description...
1月 03 09:18:03 pc main.exe[7100]: 2020/01/03 09:18:03 停止服务
1月 03 09:18:03 pc systemd[1]: Stopped System monitor service description.
```

#### 7 卸载
```
$ sudo ./main.exe uninstall
卸载成功
```

---
