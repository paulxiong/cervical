<template>
  <div class="testData">
    <ul>
      <li>系统信息更新时间 {{ systeminfo.updatedat }}</li>
      <li />
      <li>CPU使用千分率 {{ systeminfo.cpu }}</li>
      <li>1分钟之内CPU负载 {{ systeminfo.avg1 }}</li>
      <li>5分钟之内CPU负载 {{ systeminfo.avg5 }}</li>
      <li>15分钟之内CPU负载 {{ systeminfo.avg15 }}</li>
      <li />
      <li>总内存大小(单位字节) {{ systeminfo.mt }}</li>
      <li>可用存大小(单位字节) {{ systeminfo.ma }}</li>
      <li>内存使用千分率 {{ systeminfo.mperm }}</li>
      <li>总交换分区大小 {{ systeminfo.st }}</li>
      <li>可用交换分区大小 {{ systeminfo.sf }}</li>
      <li>交换分区使用千分率 {{ systeminfo.sperm }}</li>
      <li />
      <li>TCP/UDP已连接端口数 {{ systeminfo.tcp.est }}</li>
      <li>TCP/UDP监听端口数 {{ systeminfo.tcp.lis }}</li>
      <li>TCP/UDP端口总数 {{ systeminfo.tcp.total }}</li>
      <li />
      <li>IPV6 TCP/UDP已连接端口数 {{ systeminfo.tcp6.est }}</li>
      <li>IPV6 TCP/UDP监听端口数 {{ systeminfo.tcp6.lis }}</li>
      <li>IPV6 TCP/UDP端口总数 {{ systeminfo.tcp6.total }}</li>
      <li />
      <li v-for="item in systeminfo.thermal" :key="item.Type">主板温度:{{ item.Type }}   温度值:{{ item.Temp }} </li>
      <li />
      <li v-for="item in systeminfo.cards" :key="item.Type">网卡:{{ item.if }} InKBps:{{ item.ib }} OutKBps:{{ item.ob }} 总接收字节数:{{ item.tib }} 总发送字节数:{{ item.tob }}</li>
      <li />
      <li v-for="item in systeminfo.disks" :key="item.Type">分区:{{ item.spec }} 格式:{{ item.type }} 挂载目录:{{ item.dir }} 总大小(字节):{{ item.ball }} 使用千分率:{{ item.bperm }}</li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      path: 'ws://192.168.1.100:9000/api1/ws',
      socket: null,
      systeminfo: {}
    }
  },
  mounted() {
    // 初始化
    this.init()
  },
  destroyed() {
    // 销毁监听
    this.socket.onclose = this.close
    this.socket.close()
  },
  methods: {
    init: function() {
      if (typeof (WebSocket) === 'undefined') {
        alert('您的浏览器不支持socket')
      } else {
        if (this.socket != null) {
          this.socket.close()
          this.socket = null
        }
        // 实例化socket
        this.socket = new WebSocket(this.path)
        // 监听socket连接
        this.socket.onopen = this.open
        // 监听socket错误信息
        this.socket.onerror = this.error
        // 监听socket消息
        this.socket.onmessage = this.getMessage
      }
    },
    open: function() {
      console.log('socket连接成功')
      this.send('getsm')
    },
    error: function() {
      console.log('连接错误')
    },
    getMessage: function(msg) {
      this.systeminfo = {}
      const data = JSON.parse(msg.data)
      if (data.numcpu > 0) {
        this.systeminfo = data
        this.systeminfo.updatedat = new Date()
      }
    },
    send: function(params) {
      this.socket.send(params)
    },
    close: function() {
      console.log('socket已经关闭')
    }
  }
}
</script>

<style lang="scss" scoped>
.testData {
  overflow: auto;
  height: 100%;
  padding-bottom: 30px;
  .tools {
    background: #fff;
    justify-content: space-around;
    bottom: 0px;
    position: fixed;
    left: 0;
    right: 0;
    margin-left: auto;
    margin-right: auto;
  }
}
</style>
