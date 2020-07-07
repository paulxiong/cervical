<template>
  <div class="userList">
    <keep-alive>
      <router-view v-if="$route.meta.keepAlive" />
    </keep-alive>
    <router-view v-if="!$route.meta.keepAlive" />
    <el-table :data="userList.users" style="width: 100%">
      <el-table-column prop="id" :label="$t('system.usrID')" width="100" />
      <el-table-column :label="$t('system.usrAvatar')" width="200">
        <template slot-scope="scope">
          <el-image :src="scope.row.image" style="width:36px;height:36px;border-radius:6px;" />
        </template>
      </el-table-column>
      <el-table-column prop="name" :label="$t('system.usrName')" width="250" />
      <el-table-column prop="email" :label="$t('system.usrEmail')" width="250" />
      <el-table-column prop="type_id" :label="$t('system.usrType')" width="100" />
      <el-table-column prop="created_at" :label="$t('system.usrCreatedAt')" />
      <el-table-column prop="updated_at" :label="$t('system.usrUpdatedAt')" />
      <el-table-column fixed="right" :label="$t('system.usrOperation')" width="100">
        <template slot-scope="scope">
          <el-popover placement="right" trigger="click">
            <div>
              <table class="tftable" border="1">
                <tr><td class="td-1">{{ $t('system.usrID') }}:</td><td>{{ scope.row.id }}</td></tr>
                <tr><td class="td-1">{{ $t('system.usrName') }}:</td><td>{{ scope.row.name }}</td></tr>
                <tr><td class="td-1">{{ $t('system.usrType') }}:</td><td>{{ scope.row.type_id }}</td></tr>
                <tr><td class="td-1">{{ $t('system.usrEmail') }}:</td><td>{{ scope.row.email }}</td></tr>
                <tr><td class="td-1">{{ $t('system.usrPhone') }}:</td><td>{{ scope.row.mobile }}</td></tr>
                <tr><td class="td-1">{{ $t('system.usrIntroduce') }}:</td><td>{{ scope.row.introduction }}</td></tr>
                <tr><td class="td-1">{{ $t('system.usrPermission') }}:</td><td>{{ scope.row.roles }}</td></tr>

              </table>
            </div>
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
        :page-sizes="[10, 20, 30, 50]"
        :page-size="currentPageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="userList.total"
        @current-change="handleCurrentChange"
        @size-change="handleSizeChange"
      />
    </footer>
  </div>
</template>

<script>
import { getUserLists } from '@/api/user'
import { formatTime } from '@/utils/index'

export default {
  name: 'UserList',
  components: {},
  data() {
    return {
      currentPage: 1,
      currentPageSize: 10,
      loading: false,
      userList: {}
    }
  },
  created() {
    this.getUserLists(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
  },
  methods: {
    filterSearch() {
      this.getUserLists(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
    },
    handleClick(row) {
    },
    handleSizeChange(val) {
      this.currentPageSize = val
      this.getUserLists(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.getUserLists(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
    },
    getUserLists(limit, skip, order) {
      getUserLists({ 'limit': limit, 'skip': skip, 'order': order }).then(res => {
        res.data.data.users.map(v => {
          v.created_at = formatTime(v.created_at)
          v.updated_at = formatTime(v.updated_at)
        })
        this.userList = res.data.data
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.userList {
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
.tftable .td-1 {
  width: 100px;
}
</style>
