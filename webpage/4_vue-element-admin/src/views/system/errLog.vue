<template>
  <div class="errLog">
    <!-- <div class="filter-box">
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
    </div> -->
    <keep-alive>
      <router-view v-if="$route.meta.keepAlive" />
    </keep-alive>
    <router-view v-if="!$route.meta.keepAlive" />
    <el-table :data="errLog" style="width: 100%">
      <el-table-column prop="operationlog.name" label="用户" width="200" />
      <el-table-column prop="created_time" label="操作时间" width="250" />
      <el-table-column prop="version" label="版本" width="150" />
      <el-table-column prop="url" label="访问域名" />
      <el-table-column label="错误日志">
        <template slot-scope="scope">
          <p>{{ scope.row.err }}</p>
        </template>
      </el-table-column>
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
                <td>{{ scope.row.url }}</td>
              </tr>
              <tr>
                <td class="td-1">来源:</td>
                <td>{{ scope.row.operationlog.referer }}</td>
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
                <td class="td-1">操作系统:</td>
                <td>{{ scope.row.ua.os.name }}</td>
              </tr>
              <tr>
                <td class="td-1">浏览器:</td>
                <td>{{ scope.row.ua.browser.name }}</td>
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
            <el-button slot="reference" type="primary" size="mini" @click="handleClick(scope.row)">查看</el-button>
          </el-popover>
          <!-- <el-button type="primary" size="mini">删除</el-button> -->
        </template>
      </el-table-column>
    </el-table>
    <footer class="tools flex">
      <el-pagination
        class="page"
        :current-page.sync="currentPage"
        :page-sizes="[10, 20, 50, 100, 200]"
        :page-size="currentPageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @current-change="handleCurrentChange"
        @size-change="handleSizeChange"
      />
    </footer>
  </div>
</template>

<script>
import { getErrLog } from '@/api/system'
import { parseTime } from '@/utils/index'
import UA from 'ua-device'

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
    this.getErrLog(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
  },
  methods: {
    handleClick(row) {
    },
    filterSearch() {
      this.getErrLog(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.getErrLog(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
    },
    handleSizeChange(val) {
      this.currentPageSize = val
      this.getErrLog(val, (this.currentPage - 1) * this.currentPageSize, 1)
    },
    getErrLog(limit, skip, order) {
      this.loading = true
      getErrLog({ 'limit': limit, 'skip': skip, 'order': order }).then(res => {
        res.data.data.Logs.map(v => {
          v.operationlog.cost = (v.cost / 1000).toFixed(2)
          v.created_time = parseTime(v.created_time)
          v.operationlog.created_at = parseTime(v.operationlog.created_at)
          v.ua = new UA(v.operationlog.ua)
          v.err = JSON.parse(v.errlog)[0].err || ''
          v.stack = JSON.parse(v.errlog)[0].stack || ''
          v.url = JSON.parse(v.errlog)[0].url || ''
          v.version = JSON.parse(v.errlog)[0].version || ''
        })
        this.errLog = res.data.data.Logs
        this.total = res.data.data.total
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
