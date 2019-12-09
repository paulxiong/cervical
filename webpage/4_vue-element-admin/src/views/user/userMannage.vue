<template>
  <div class="userList">
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
    <el-table :data="userList.users" style="width: 100%">
      <el-table-column prop="id" label="用户ID" width="100" />
      <el-table-column label="头像" width="200">
        <template slot-scope="scope">
          <el-image :src="scope.row.image" style="width:36px;height:36px;border-radius:6px;" />
        </template>
      </el-table-column>
      <el-table-column prop="name" label="用户名" width="250" />
      <el-table-column prop="email" label="邮箱" width="250" />
      <el-table-column prop="type_id" label="用户类型" width="100" />
      <el-table-column prop="created_at" label="创建时间" />
      <el-table-column prop="updated_at" label="最近操作" />
      <el-table-column fixed="right" label="操作" width="100">
        <template slot-scope="scope">
          <el-popover placement="right" trigger="click">
            <div>
              <table class="tftable" border="1">
                <tr><td class="td-1">用户ID:</td><td>{{ scope.row.id }}</td></tr>
                <tr><td class="td-1">用户名:</td><td>{{ scope.row.name }}</td></tr>
                <tr><td class="td-1">用户类型:</td><td>{{ scope.row.type_id }}</td></tr>
                <tr><td class="td-1">邮箱:</td><td>{{ scope.row.email }}</td></tr>
                <tr><td class="td-1">手机号码:</td><td>{{ scope.row.mobile }}</td></tr>
                <tr><td class="td-1">介绍:</td><td>{{ scope.row.introduction }}</td></tr>
                <tr><td class="td-1">权限:</td><td>{{ scope.row.roles }}</td></tr>

              </table>
            </div>
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
      listQuery: {
        desc: undefined,
        type: undefined
      },
      typeOptions: [
        {
          key: '0',
          name: '类型'
        },
        {
          key: '1',
          name: '用户名'
        },
        {
          key: '2',
          name: '城市'
        }
      ],
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
      this.getUserLists(this.currentPageSize, (this.currentPage - 1) * val, 1)
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.getUserLists(this.currentPageSize, (val - 1) * this.currentPageSize, 1)
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
