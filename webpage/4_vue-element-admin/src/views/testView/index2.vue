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

    <el-table
      :data="projectlist"
      style="width: 100%"
    >
      <el-table-column
        label="id"
        width="80"
      >
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="类型"
        width="80"
      >
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.projectType }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="描述"
        width="180"
      >
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.desc }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="详细信息"
        width="180"
      >
        <template slot-scope="scope">
          <el-popover trigger="hover" placement="top">
            <p>创建时间: {{ scope.row.created_at }}</p>
            <p>创建者: {{ scope.row.username }}</p>
            <div slot="reference" class="name-wrapper">
              <el-tag size="medium">{{ scope.row.statusTime }}</el-tag>
            </div>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-switch v-model="scope.row.dropdataset" active-text="删数据集" inactive-text="不删数据集" />
          <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="tools flex">
      <el-pagination
        class="page"
        :current-page.sync="currentPage"
        :page-sizes="[10, 20, 30, 50]"
        :page-size="currentPageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @current-change="handleCurrentChange"
        @size-change="handleSizeChange"
      />
    </div>
  </div>
</template>

<script>
import { getListprojects } from '@/api/cervical'
import { taskStatus, createdBy, taskType, projectType } from '@/const/const'
import { parseTime } from '@/utils/index'

export default {
  data() {
    return {
      path: 'ws://192.168.1.100:9000/api1/ws',
      socket: null,
      systeminfo: {},
      projectlist: [],
      currentPageSize: 20,
      currentPage: 0,
      total: 0,
      loading: false
    }
  },
  created() {
    this.getListprojects(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
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
    handleDelete(index, row) {
      console.log(index, row)
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.getListprojects(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
    },
    handleSizeChange(val) {
      this.currentPageSize = val
      this.getListprojects(val, (this.currentPage - 1) * this.currentPageSize, 1)
    },
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
    },
    getListprojects(limit, skip, order) {
      this.loading = true
      getListprojects({ 'limit': limit, 'skip': skip, 'order': order }).then(res => {
        res.data.data.projects.map(v => {
          v.created_at = parseTime(v.created_at)
          v.updated_at = parseTime(v.updated_at)
          v.starttime = parseTime(v.starttime)
          v.endtime = parseTime(v.endtime)
          v.created_by = createdBy[v.created_by] || '普通用户'
          v.statusType = taskType[v.status]
          v.statusTime = v.status === '开始' ? `${v.status}(${v.ETA}s)` : taskStatus[v.status]
          v.projectType = projectType[v.type]
          v.dropdataset = true
        })
        this.projectlist = res.data.data.projects
        this.total = res.data.data.total
        this.loading = false
      })
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
