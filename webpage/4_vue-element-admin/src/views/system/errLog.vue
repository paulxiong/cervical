<template>
  <div class="errLog">
    <div class="filter-box">
      <el-input
        v-model="listQuery.desc"
        placeholder="请输入描述搜索"
        style="width:200px;"
        class="filter-input"
        @keyup.enter.native="filterSearch"
      />
      <el-select
        v-model="listQuery.type"
        placeholder="类型"
        clearable
        class="filter-type"
        style="width: 130px"
      >
        <el-option
          v-for="item in typeOptions"
          :key="item.key"
          :label="item.name"
          :value="item.key"
        />
      </el-select>
      <el-button class="filter-btn" type="primary" :icon="loading?'el-icon-loading':'el-icon-refresh-left'" @click="filterSearch">刷新</el-button>
    </div>
    <el-table :data="errLog" height="850px" style="width: 100%">
      <el-table-column prop="operationlog.name" label="用户" />
      <el-table-column prop="created_time" label="操作时间" width="150" />
      <el-table-column prop="errlog" label="错误日志" width="800" />
      <el-table-column prop="operationlog.referer" label="访问域名" />
      <el-table-column prop="operationlog.path" label="错误路径" />
      <el-table-column fixed="right" label="操作" width="100">
        <template slot-scope="scope">
          <el-popover placement="right" trigger="click">
            <table class="tftable" border="1">
              <tr>
                <th class="td-1">ID:</th>
                <th>{{ scope.row.id }}</th>
              </tr>
              <tr>
                <td class="td-1">用户ID:</td>
                <td>{{ scope.row.operationlog.user_id }}</td>
              </tr>
              <tr>
                <td class="td-1">用户名:</td>
                <td>{{ scope.row.operationlog.name }}</td>
              </tr>
              <tr>
                <td class="td-1">电话:</td>
                <td>{{ scope.row.operationlog.mobile }}</td>
              </tr>
              <tr>
                <td class="td-1">请求大小:</td>
                <td>{{ scope.row.operationlog.bodysize }}</td>
              </tr>
              <tr>
                <td class="td-1">状态码:</td>
                <td>{{ scope.row.operationlog.code }}</td>
              </tr>
              <tr>
                <td class="td-1">耗时(ms):</td>
                <td>{{ scope.row.operationlog.cost }}</td>
              </tr>
              <tr>
                <td class="td-1">操作时间:</td>
                <td>{{ scope.row.operationlog.created_at }}</td>
              </tr>
              <tr>
                <td class="td-1">请求方式:</td>
                <td>{{ scope.row.operationlog.method }}</td>
              </tr>
              <tr>
                <td class="td-1">IP:</td>
                <td>{{ scope.row.operationlog.ip }}</td>
              </tr>
              <tr>
                <td class="td-1">路径:</td>
                <td>{{ scope.row.operationlog.path }}</td>
              </tr>
              <tr>
                <td class="td-1">来源:</td>
                <td>{{ scope.row.operationlog.referer }}</td>
              </tr>
              <tr>
                <td class="td-1">地域ID:</td>
                <td>{{ scope.row.operationlog.region_id }}</td>
              </tr>
              <tr>
                <td class="td-1">国家:</td>
                <td>{{ scope.row.operationlog.region.country }}</td>
              </tr>
              <tr>
                <td class="td-1">省份(州):</td>
                <td>{{ scope.row.operationlog.region.province }}</td>
              </tr>
              <tr>
                <td class="td-1">城市:</td>
                <td>{{ scope.row.operationlog.region.city }}</td>
              </tr>
              <tr>
                <td class="td-1">运营商:</td>
                <td>{{ scope.row.operationlog.region.isp }}</td>
              </tr>
              <tr>
                <td class="td-1">操作ID:</td>
                <td>{{ scope.row.opid }}</td>
              </tr>
              <tr>
                <td class="td-1">操作者:</td>
                <td>{{ scope.row.created_by }}</td>
              </tr>
              <tr>
                <td class="td-1">邮箱:</td>
                <td>{{ scope.row.operationlog.email }}</td>
              </tr>
              <tr>
                <td class="td-1">类型:</td>
                <td>{{ scope.row.type }}</td>
              </tr>
            </table>
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
        :page-sizes="[10, 20, 50, 100, 200]"
        :page-size="10"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @current-change="handleCurrentChange"
        @size-change="handleSizeChange"
      />
    </footer>
  </div>
</template>

<script>
import { getErrLog } from '@/api/cervical'
// import { formatTime } from '@/utils/index'
// import UA from 'ua-device'
export default {
  name: 'ErrLog',
  components: {},
  data() {
    return {
      currentPage: 1,
      currentPageSize: 10,
      errLog: [],
      total: 1,
      loading: false,
      listQuery: {
        desc: undefined,
        type: undefined
      },
      typeOptions: [
        {
          key: '0',
          name: '创建者'
        },
        {
          key: '1',
          name: '类型'
        },
        {
          key: '2',
          name: '错误日志'
        },
        {
          key: '3',
          name: '时间'
        }
      ]
    }
  },
  created() {
    this.getErrLog(10, 0, 1)
  },
  methods: {
    handleClick(row) {
      console.log(row)
    },
    filterSearch() {
      this.getErrLog(10, (this.currentPage - 1) * this.currentPageSize, 1)
    },
    handleCurrentChange(val) {
      // this.currentSkip = (val - 1) * this.currentPageSize
      this.getErrLog(this.currentPageSize, (this.currentPage - 1) * val, 1)
      // console.log(`这是第 ${val} 页 `)
    },
    handleSizeChange(val) {
      this.currentPageSize = val
      this.getErrLog(val, (this.currentPage - 1) * val, 1)
      // console.log(`每页 ${val} 条`)
    },
    data() {
      return {
        currentSkip: 0, // 当前记录的位置
        currentPageSize: 10 // 每页显示多少条
      }
    },
    getErrLog(limit, skip, order) {
      this.loading = true
      getErrLog({ 'limit': limit, 'skip': skip, 'order': order }).then(res => {
        res.data.data.map(v => {
          // v.ua = new UA(v.ua)
          // v.cost = (v.cost / 1000).toFixed(2)
          // v.created_at = formatTime(v.created_at)
          // v.updated_at = formatTime(v.created_at)
          // v.processtime = formatTime(v.processtime)
          // v.processend = formatTime(v.processtime)
          // v.region.city = v.region.city ? v.region.city : v.region.province ? v.region.province : v.region.country
        })
        this.errLog = res.data.data
        this.total = res.data.total
        this.loading = false
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.errLog {
  overflow: auto;
  height: 100%;
  .tools {
    background: #fff;
    justify-content: space-around;
  }
}
table.tftable {
  font-size: 12px;
  color: #333333;
  border-width: 1px;
  border-color: #729ea5;
  border-collapse: collapse;
}
table.tftable th {
  font-size: 12px;
  background-color: #acc8cc;
  border-width: 1px;
  padding: 8px;
  border-style: solid;
  border-color: #729ea5;
  text-align: left;
}
table.tftable tr {
  background-color: #d4e3e5;
}
table.tftable td {
  font-size: 12px;
  border-width: 1px;
  padding: 8px;
  border-style: solid;
  border-color: #729ea5;
}
.tftable .td-1 {
  width: 100px;
}
</style>
