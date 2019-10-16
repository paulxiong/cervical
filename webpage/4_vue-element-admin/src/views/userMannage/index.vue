<template>
  <div class="userLog">
    <el-table
      :data="gridData"
      style="width: 100%">
      <el-table-column
        prop="date"
        label="状态"
        width="180">
      </el-table-column>
      <el-table-column
        prop="name"
        label="性别"
        width="180">
      </el-table-column>
      <el-table-column
        prop="address"
        label="地址">
      </el-table-column>
      <el-table-column
        prop="address"
        label="身份证">
      </el-table-column>
      <el-table-column
        prop="address"
        label="id">
      </el-table-column>
    </el-table>
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page.sync="currentPage3"
      :page-size="100"
      layout="prev, pager, next, jumper"
      :total="1000">
    </el-pagination>
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
      currentPage3: 5,
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
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`);
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
