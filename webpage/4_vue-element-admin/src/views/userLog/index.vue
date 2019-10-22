<template>
  <div class="userLog">
    <el-table :data="userLog.accesslog" style="width: 100%">
      <el-table-column prop="user_id" label="用户ID" width="100" />
      <el-table-column prop="ip" label="IP" width="180" />
      <el-table-column prop="region.city" label="城市" width="100" />
      <el-table-column prop="created_at" label="时间">
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.created_at }}</span>
        </template>
      </el-table-column>
      <el-table-column label="硬件" width="100">
        <template slot-scope="scope">
          <svg-icon style="width:20px;height:20px;" :icon-class="scope.row.ua.device.type" />
          <!-- <span>{{scope.row.ua.device.type}}</span> -->
        </template>
      </el-table-column>
      <el-table-column label="操作系统" width="100">
        <template slot-scope="scope">
          <svg-icon style="width:20px;height:20px;" :icon-class="scope.row.ua.os.name" />
          <!-- <span>{{scope.row.ua.os.name}}</span> -->
        </template>
      </el-table-column>
      <el-table-column prop="cost" label="耗时(ms)" width="100" />
      <el-table-column fixed="right" label="操作" width="100">
        <template slot-scope="scope">
          <el-popover placement="right" width="400" trigger="click">
            <div>
              <table id="tfhover" class="tftable" border="1">
                <tr><th>ID:</th><th>{{ scope.row.id }}</th></tr>
                <tr><td>用户ID:</td><td>{{ scope.row.user_id }}</td></tr>
                <tr><td>请求大小:</td><td>{{ scope.row.bodysize }}</td></tr>
                <tr><td>状态码:</td><td>{{ scope.row.code }}</td></tr>
                <tr><td>耗时(ms):</td><td>{{ scope.row.cost }}</td></tr>
                <tr><td>创建时间:</td><td>{{ scope.row.created_at }}</td></tr>
                <tr><td>请求方式:</td><td>{{ scope.row.method }}</td></tr>
                <tr><td>路径:</td><td>{{ scope.row.path }}</td></tr>
                <tr><td>参数:</td><td>{{ scope.row.query }}</td></tr>
                <tr><td>来源:</td><td>{{ scope.row.referer }}</td></tr>
                <tr><td>地域ID:</td><td>{{ scope.row.region_id }}</td></tr>
                <tr><td>国家:</td><td>{{ scope.row.region.country }}</td></tr>
                <tr><td>省份:</td><td>{{ scope.row.region.province }}</td></tr>
                <tr><td>城市:</td><td>{{ scope.row.region.city }}</td></tr>
                <tr><td>运营商:</td><td>{{ scope.row.region.isp }}</td></tr>
                <tr><td>硬件:</td><td>{{ scope.row.ua.device.type }}</td></tr>
                <tr><td>操作系统:</td><td>{{ scope.row.ua.os.name }} {{ scope.row.ua.os.version.original }}</td></tr>
                <tr><td>浏览器:</td><td>{{ scope.row.ua.browser.name }} {{ scope.row.ua.browser.version.original }}</td></tr>
                <tr><td>浏览器内核:</td><td>{{ scope.row.ua.engine.name }} {{ scope.row.ua.engine.version.original }}</td></tr>
              </table>
            </div>
            <el-button slot="reference" type="text" size="small" @click="handleClick(scope.row)">查看</el-button>
          </el-popover>
          <el-button type="text" size="small">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <footer class="tools flex">
      <el-pagination
        class="page"
        :current-page.sync="currentPage"
        :page-size="10"
        layout="prev, pager, next, jumper"
        :total="userLog.total"
        @current-change="handleCurrentChange"
      />
    </footer>
  </div>
</template>

<script>
import { getUserLog } from '@/api/user'
import { formatTime } from '@/utils/index'
import UA from 'ua-device'

export default {
  name: 'UserLog',
  components: {},
  data() {
    return {
      currentPage: 1,
      userLog: []
    }
  },
  mounted() {
    this.getUserLog(10, 0, 1)
  },
  methods: {
    handleClick(row) {
      console.log(row)
    },
    handleCurrentChange(val) {
      this.getUserLog(10, val * 10, 1)
    },
    getUserLog(limit, skip, order) {
      getUserLog({ 'limit': limit, 'skip': skip, 'order': order }).then(res => {
        res.data.data.accesslog.map(v => {
          v.ua = new UA(v.ua)
          v.cost = (v.cost / 1000).toFixed(2)
          v.created_at = formatTime(v.created_at)
        })
        this.userLog = res.data.data
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.userLog {
  padding-top: 10px;
  overflow: auto;
  height: 100%;
  .tools {
    margin-top: 10px;
    justify-content: space-around;
  }
}
table.tftable {
  font-size:12px;
  color:#333333;
  border-width: 1px;
  border-color: #729ea5;
  border-collapse: collapse;
}
table.tftable th {
  font-size:12px;
  background-color:#acc8cc;
  border-width: 1px;
  padding: 8px;
  border-style: solid;
  border-color: #729ea5;
  text-align:left;
}
table.tftable tr {
  background-color:#d4e3e5;
}
table.tftable td {
  font-size:12px;
  border-width: 1px;
  padding: 8px;
  border-style: solid;
  border-color: #729ea5;
}
</style>
