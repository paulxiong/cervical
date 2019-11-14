<template>
  <div class="userList">
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
    </div>
    <el-table :data="userList" height="850px" style="width: 100%">
      <el-table-column prop="id" label="用户ID" width="100" />
      <el-table-column prop="name" label="用户名" width="180" />
      <el-table-column prop="type_id" label="用户类型" width="100" />
      <el-table-column prop="city" label="城市" />
      <el-table-column fixed="right" label="操作" width="100">
        <template slot-scope="scope">
          <el-popover placement="right" trigger="click">
            <div>
              <table class="tftable" border="1">
                <tr><td class="td-1">用户ID:</td><td>{{ scope.row.id }}</td></tr>
                <tr><td class="td-1">用户名:</td><td>{{ scope.row.name }}</td></tr>
                <tr><td class="td-1">类型:</td><td>{{ scope.row.type_id }}</td></tr>
                <tr><td class="td-1">邮箱:</td><td>{{ scope.row.email }}</td></tr>
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
        :page-sizes="[10, 20, 30, 50]"
        :page-size="10"
        layout="total, sizes, prev, pager, next, jumper"
        :total="1000"
        @current-change="handleCurrentChange"
      />
    </footer>
  </div>
</template>

<script>
import { getUserLists } from '@/api/user'

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
      userList: []
    }
  },
  created() {
    this.getUserLists(10, 0, 1)
  },
  methods: {
    handleClick(row) {
      console.log(row)
    },
    handleSizeChange(val) {
      this.currentPageSize = val
      this.getUserLists(val, (this.currentPage - 1) * val, 1)
      // console.log(`每页 ${val} 条`)
    },
    handleCurrentChange(val) {
      this.getUserLists(this.currentPageSize, (this.currentPage - 1) * val, 1)
      // console.log(val)
    },
    getUserLists(limit, skip, order) {
      getUserLists({ 'limit': limit, 'skip': skip, 'order': order }).then(res => {
        this.userList = res.data.data
        console.log(res.data.data)
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.userList {
  .tools {
    background: #fff;
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
.tftable .td-1 {
  width: 100px;
}
</style>
