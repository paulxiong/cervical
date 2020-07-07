<template>
  <div class="userLog">
    <keep-alive>
      <router-view v-if="$route.meta.keepAlive" />
    </keep-alive>
    <router-view v-if="!$route.meta.keepAlive" />
    <el-table :data="userLog.accesslog" style="width: 100%">
      <el-table-column prop="name" :label="$t('system.usrName')" width="200" />
      <el-table-column prop="ip" label="IP" width="180" />
      <el-table-column prop="region.isp" :label="$t('system.errorOperators')" width="100" />
      <el-table-column prop="region.city" :label="$t('system.errorCity')" width="100" />
      <el-table-column prop="path" :label="$t('system.errorPath')" />
      <el-table-column prop="created_at" :label="$t('system.usrCreatedAt')">
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.created_at }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('system.usrHW')" width="100">
        <template slot-scope="scope">
          <svg-icon style="width:20px;height:20px;" :icon-class="scope.row.ua.device.type" />
          <!-- <span>{{scope.row.ua.device.type}}</span> -->
        </template>
      </el-table-column>
      <el-table-column :label="$t('system.errorOS')" width="100">
        <template slot-scope="scope">
          <svg-icon style="width:20px;height:20px;" :icon-class="scope.row.ua.os.name" />
          <!-- <span>{{scope.row.ua.os.name}}</span> -->
        </template>
      </el-table-column>
      <el-table-column prop="cost" :label="$t('system.errorTime')" width="100" />
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
                <td>{{ scope.row.user_id }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorUserName') }}:</td>
                <td>{{ scope.row.name }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorPhone') }}:</td>
                <td>{{ scope.row.mobile }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorReqSize') }}:</td>
                <td>{{ scope.row.bodysize }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorState') }}:</td>
                <td>{{ scope.row.code }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorTime') }}:</td>
                <td>{{ scope.row.cost }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorOperationTime2') }}:</td>
                <td>{{ scope.row.created_at }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorRequestMethod') }}:</td>
                <td>{{ scope.row.method }}</td>
              </tr>
              <tr>
                <td class="td-1">IP:</td>
                <td>{{ scope.row.ip }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorPath') }}:</td>
                <td>{{ scope.row.path }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorFrom') }}:</td>
                <td>{{ scope.row.referer }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.usrRegionID') }}:</td>
                <td>{{ scope.row.region_id }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorCountry') }}:</td>
                <td>{{ scope.row.region.country }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorProvince') }}:</td>
                <td>{{ scope.row.region.province }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorCity') }}:</td>
                <td>{{ scope.row.region.city }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.errorOperators') }}:</td>
                <td>{{ scope.row.region.isp }}</td>
              </tr>
              <tr>
                <td class="td-1">{{ $t('system.usrHW') }}:</td>
                <td>{{ scope.row.ua.device.type }}</td>
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
                <td class="td-1">{{ $t('system.usrBrowserEngine') }}:</td>
                <td>{{ scope.row.ua.engine.name }}</td>
              </tr>
            </table>
            <el-button slot="reference" type="primary" size="mini" @click="handleClick(scope.row)">{{ $t('system.usrDetails') }}</el-button>
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
        :total="userLog.total"
        @current-change="handleCurrentChange"
        @size-change="handleSizeChange"
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
      currentPageSize: 10,
      userLog: [],
      loading: false
    }
  },
  created() {
    this.getUserLog(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
  },
  methods: {
    refreshData() {
      this.getUserLog(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
    },
    filterSearch() {
      this.refreshData()
    },
    handleClick(row) {
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.refreshData()
    },
    handleSizeChange(val) {
      this.currentPageSize = val
      this.refreshData()
    },
    getUserLog(limit, skip, order) {
      this.loading = true
      getUserLog({ 'limit': limit, 'skip': skip, 'order': order }).then(res => {
        res.data.data.accesslog.map(v => {
          v.ua = new UA(v.ua)
          v.cost = (v.cost / 1000).toFixed(2)
          v.created_at = formatTime(v.created_at)
          v.updated_at = formatTime(v.created_at)
          v.processtime = formatTime(v.processtime)
          v.processend = formatTime(v.processtime)
          v.region.city = v.region.city ? v.region.city : v.region.province ? v.region.province : v.region.country
        })
        this.userLog = res.data.data
        this.loading = false
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.userLog {
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
