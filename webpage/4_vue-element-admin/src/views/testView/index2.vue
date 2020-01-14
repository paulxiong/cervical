<template>
  <div class="testData2">
    <el-tabs type="border-card">
      <el-tab-pane>
        <span slot="label"><i class="el-icon-date" /> CPU</span>
        <table class="tftable" border="1">
          <tr>
            <th class="td-1">CPU使用千分率</th>
            <th>{{ systeminfo.cpu }}</th>
          </tr>
          <tr>
            <td class="td-1">CPU核心数</td>
            <td>{{ systeminfo.numcpu }}</td>
          </tr>
          <tr>
            <td class="td-1">1分钟之内CPU负载</td>
            <td>{{ systeminfo.avg1 }}</td>
          </tr>
          <tr>
            <td class="td-1">5分钟之内CPU负载</td>
            <td>{{ systeminfo.avg5 }}</td>
          </tr>
          <tr>
            <td class="td-1">15分钟之内CPU负载</td>
            <td>{{ systeminfo.avg15 }}</td>
          </tr>
        </table>
      </el-tab-pane>
      <el-tab-pane label="内存">
        <span slot="label"><i class="el-icon-date" /> 内存</span>
        <table class="tftable" border="1">
          <tr>
            <th class="td-1">总内存大小(单位字节)</th>
            <th>{{ systeminfo.mt }}</th>
          </tr>
          <tr>
            <td class="td-1">可用存大小(单位字节)</td>
            <td>{{ systeminfo.ma }}</td>
          </tr>
          <tr>
            <td class="td-1">内存使用千分率</td>
            <td>{{ systeminfo.mperm }}</td>
          </tr>
          <tr>
            <td class="td-1">总交换分区大小</td>
            <td>{{ systeminfo.st }}</td>
          </tr>
          <tr>
            <td class="td-1">可用交换分区大小</td>
            <td>{{ systeminfo.sf }}</td>
          </tr>
          <tr>
            <td class="td-1">交换分区使用千分率</td>
            <td>{{ systeminfo.sperm }}</td>
          </tr>
        </table>
      </el-tab-pane>
      <el-tab-pane label="磁盘">磁盘</el-tab-pane>
      <el-tab-pane label="网卡">网卡</el-tab-pane>
    </el-tabs>
    <ul>
      <li>系统信息更新时间 {{ systeminfo.updatedat }}</li>
      <li />
      <li>CPU使用千分率 {{ systeminfo.cpu }}</li>
      <li>CPU核心数 {{ systeminfo.numcpu }}</li>
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
      v-loading="loading"
      :data="projectlist"
      style="width: 100%"
      class="content"
      element-loading-text="正在删除项目请稍等, 请不要刷新页面 不要关闭页面 ！！"
      element-loading-spinner="el-icon-loading"
      element-loading-background="rgba(0, 0, 0, 0.8)"
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
import { getListprojects, removeProject } from '@/api/cervical'
import { taskStatus, createdBy, taskType, projectType } from '@/const/const'
import { parseTime } from '@/utils/index'
import { WSURL } from '@/const/config'

export default {
  data() {
    return {
      path: WSURL + '/api1/ws',
      socket: null,
      systeminfo: [],
      projectlist: [],
      currentPageSize: 20,
      currentPage: 1,
      total: 0,
      loading: false,
      nowDate: null,
      nowTime: null,
      nowWeek: null
    }
  },
  created() {
    this.getListprojects(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
  },
  mounted() {
    // 初始化
    this.init()
    this.currentTime()
  },
  destroyed() {
    // 销毁监听
    this.socket.onclose = this.close
    this.socket.close()
  },
  beforeDestroy: function() {
    if (this.getDate) {
      console.log('销毁定时器')
      clearInterval(this.getDate)
    }
  },
  methods: {
    handleDelete(index, row) {
      console.log(index, row)
      const pid = row.id
      const dropdataset = (row.dropdataset === true) ? 1 : 0
      const content = (row.dropdataset === true) ? '此操作将永久删除该项目及相应数据集' : '此操作将永久删除该项目'
      this.$confirm(content + ', 是否继续?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message({ type: 'success', message: '开始删除' })
        this.removeProject(pid, dropdataset)
      }).catch(() => {
        this.$message({ type: 'info', message: '已取消删除' })
      })
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
    },
    removeProject(pid, dropdt) {
      this.loading = true
      removeProject({ 'pid': pid, 'dropdt': dropdt }).then(res => {
        this.loading = false
        this.getListprojects(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
      })
    },
    currentTime() {
      setInterval(this.getDate, 500)
    },
    getDate: function() {
      var _this = this
      const yy = new Date().getFullYear()
      const mm = new Date().getMonth() + 1
      const dd = new Date().getDate()
      const week = new Date().getDay()
      const hh = new Date().getHours()
      const mf =
          new Date().getMinutes() < 10
            ? '0' + new Date().getMinutes()
            : new Date().getMinutes()
      const ss =
          new Date().getSeconds() < 10
            ? '0' + new Date().getSeconds()
            : new Date().getSeconds()
      if (week === 1) {
        this.nowWeek = '星期一'
      } else if (week === 2) {
        this.nowWeek = '星期二'
      } else if (week === 3) {
        this.nowWeek = '星期三'
      } else if (week === 4) {
        this.nowWeek = '星期四'
      } else if (week === 5) {
        this.nowWeek = '星期五'
      } else if (week === 6) {
        this.nowWeek = '星期六'
      } else {
        this.nowWeek = '星期日'
      }
      _this.nowTime = hh + ':' + mf + ':' + ss
      _this.nowDate = yy + '/' + mm + '/' + dd
    }
  }
}
</script>

<style lang="scss" scoped>
.testData2 {
  overflow: auto;
  height: 100%;
  padding-bottom: 3px;
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
  .content {
    padding-bottom: 30px;
  }
}
</style>
