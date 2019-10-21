<template>
  <div class="userLog">
    <el-table :data="userLog.accesslog" style="width: 100%">
      <el-table-column prop="id" label="ID" width="100" />
      <el-table-column prop="user_id" label="用户ID" width="100" />
      <el-table-column prop="ip" label="IP" width="180" />
      <el-table-column prop="region.isp" width="100" label="运营商" />
      <el-table-column prop="region.city" label="城市" width="100" />
      <el-table-column prop="path" label="路径" />
      <el-table-column prop="created_at" label="时间" />
      <el-table-column prop="ua.device.type" label="硬件" width="100" />
      <el-table-column prop="ua.os.name" label="操作系统" width="100" />
      <el-table-column prop="ua.browser.name" label="浏览器" width="100" />
      <el-table-column prop="cost" label="耗时(us)" width="100" />
      <el-table-column fixed="right" label="操作" width="100">
        <template slot-scope="scope">
          <el-popover placement="right" width="400" trigger="click">
            <div>{{ scope.row }}</div>
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
</style>
