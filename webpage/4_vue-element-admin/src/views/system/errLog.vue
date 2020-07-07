<template>
  <div class="errLog">
    <keep-alive>
      <router-view v-if="$route.meta.keepAlive" />
    </keep-alive>
    <router-view v-if="!$route.meta.keepAlive" />
    <el-table :data="errLog" style="width: 100%">
      <el-table-column prop="operationlog.name" :label="$t('system.errorUser')" width="200" />
      <el-table-column prop="created_time" :label="$t('system.errorOperationTime')" width="250" />
      <el-table-column prop="version" :label="$t('system.errorVersion')" width="150" />
      <el-table-column prop="url" :label="$t('system.errorDomain')" />
      <el-table-column :label="$t('system.errorLog')">
        <template slot-scope="scope">
          <p>{{ scope.row.err }}</p>
        </template>
      </el-table-column>
      <el-table-column fixed="right" :label="$t('system.errorOperation')" width="100">
        <template slot-scope="scope">
          <el-popover placement="right" trigger="click">
            <table class="tftable" border="1">
              <tr>
                <th class="td-1">ID:</th>
                <th>{{ scope.row.id }}</th>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorUserID') }}:</td>
                <td>{{ scope.row.operationlog.user_id }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorUserName') }}:</td>
                <td>{{ scope.row.operationlog.name }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorPhone') }}:</td>
                <td>{{ scope.row.operationlog.mobile }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorReqSize') }}:</td>
                <td>{{ scope.row.operationlog.bodysize }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorState') }}:</td>
                <td>{{ scope.row.operationlog.code }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorTime') }}:</td>
                <td>{{ scope.row.operationlog.cost }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorOperationTime2') }}:</td>
                <td>{{ scope.row.operationlog.created_at }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorRequestMethod') }}:</td>
                <td>{{ scope.row.operationlog.method }}</td>
              </tr>
              <tr>
                <td class="td-1">IP:</td>
                <td>{{ scope.row.operationlog.ip }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorPath') }}:</td>
                <td>{{ scope.row.url }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorFrom') }}:</td>
                <td>{{ scope.row.operationlog.referer }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorCountry') }}:</td>
                <td>{{ scope.row.operationlog.region.country }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorProvince') }}:</td>
                <td>{{ scope.row.operationlog.region.province }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorCity') }}:</td>
                <td>{{ scope.row.operationlog.region.city }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorOperators') }}:</td>
                <td>{{ scope.row.operationlog.region.isp }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorOS') }}:</td>
                <td>{{ scope.row.ua.os.name }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorBrowser') }}:</td>
                <td>{{ scope.row.ua.browser.name }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorEMail') }}:</td>
                <td>{{ scope.row.operationlog.email }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorType') }}:</td>
                <td>{{ scope.row.type }}</td>
              </tr>
            </table>
            <el-button slot="reference" type="primary" size="mini" @click="handleClick(scope.row)">{{ $t('system.errorDetails') }}</el-button>
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
      }
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
