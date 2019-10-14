<template>
  <div class="userLog">
    <header class="tools flex">
      <el-pagination
        class="page"
        @current-change="handleCurrentChange"
        :current-page.sync="currentPage"
        :page-size="100"
        layout="prev, pager, next, jumper"
        :total="1000"
      ></el-pagination>
    </header>
    <el-table :data="userLog" style="width: 100%">
      <el-table-column prop="id" label="ID" width="100"></el-table-column>
      <el-table-column prop="user_id" label="用户ID" width="100"></el-table-column>
      <el-table-column prop="ip" label="IP" width="180"></el-table-column>
      <el-table-column prop="region.isp" width="100" label="运营商"></el-table-column>
      <el-table-column prop="region.city" label="城市" width="100"></el-table-column>
      <el-table-column prop="path" label="路径" width="180"></el-table-column>
      <el-table-column prop="ua.device.type" label="硬件" width="150"></el-table-column>
      <el-table-column prop="ua.os.name" label="操作系统" width="150"></el-table-column>
      <el-table-column prop="ua.browser.name" label="浏览器" width="150"></el-table-column>
      <el-table-column prop="cost" label="耗时(ms)" width="100"></el-table-column>
      <el-table-column fixed="right" label="操作" width="100">
        <template slot-scope="scope">
          <el-popover placement="right" width="400" trigger="click">
            <div>{{scope.row}}</div>
            <el-button slot="reference" @click="handleClick(scope.row)" type="text" size="small">查看</el-button>
          </el-popover>
          <el-button type="text" size="small">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getUserLog } from '@/api/user'
import UA from 'ua-device'

export default {
  name: 'UserLog',
  components: {},
  data() {
    return {
      gridData: [{
        date: '2016-05-02',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }, {
        date: '2016-05-04',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }, {
        date: '2016-05-01',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }, {
        date: '2016-05-03',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }],
      currentPage: 1,
      userLog: []
    }
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
        })
        this.userLog = res.data.data.accesslog
      })
    }
  },
  mounted() {
    this.getUserLog(10, 0, 1)
  }
}
</script>

<style lang="scss" scoped>
.userLog {
  padding-top: 10px;
  .tools {
    justify-content: space-around;
  }
}
</style>
