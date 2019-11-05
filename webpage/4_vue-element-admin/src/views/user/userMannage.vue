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
      <el-table-column prop="id" label="ID" width="100" />
      <el-table-column prop="user_id" label="用户ID" width="100" />
      <el-table-column prop="name" label="用户名" width="180" />
      <el-table-column prop="type" label="类型" width="100" />
      <el-table-column prop="city" label="城市" />
      <el-table-column fixed="right" label="操作" width="100">
        <template slot-scope="scope">
          <el-popover placement="right" trigger="click">
            <div>
              <table class="tftable" border="1">
                <tr><th class="td-1">ID:</th><th>{{ scope.row.id }}</th></tr>
                <tr><td class="td-1">用户ID:</td><td>{{ scope.row.user_id }}</td></tr>
                <tr><td class="td-1">城市:</td><td>{{ scope.row.city }}</td></tr>
                <tr><td class="td-1">用户名:</td><td>{{ scope.row.name }}</td></tr>
                <tr><td class="td-1">类型:</td><td>{{ scope.row.type }}</td></tr>
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

export default {
  name: 'UserList',
  components: {},
  data() {
    return {
      currentPage: 1,
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
      userList: [
        {
          'id': 0,
          'user_id': 12,
          'name': 'github_cy@163.com',
          'type': '管理员',
          'city': '昆明市'
        },
        {
          'id': 1,
          'user_id': 13,
          'name': 'ggxxde@163.com',
          'type': '管理员',
          'city': '昆明市'
        },
        {
          'id': 2,
          'user_id': 14,
          'name': '717138552@qq.com',
          'type': '管理员',
          'city': '昆明市'
        },
        {
          'id': 3,
          'user_id': 15,
          'name': 'paulxiong_2007@gmail.com',
          'type': '管理员',
          'city': '加利福利亚'
        }
      ]
    }
  },
  methods: {
    handleClick(row) {
      console.log(row)
    },
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`)
    },
    handleCurrentChange(val) {
      console.log(val)
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
