<template>
  <div class="userList">
    <el-table :data="userList" style="width: 100%">
      <el-table-column prop="id" label="ID" width="100"></el-table-column>
      <el-table-column prop="user_id" label="用户ID" width="100"></el-table-column>
      <el-table-column prop="name" label="用户名" width="180"></el-table-column>
      <el-table-column prop="type" label="类型" width="100"></el-table-column>
      <el-table-column prop="city" label="城市"></el-table-column>
      <el-table-column fixed="right" label="操作" width="100">
        <template slot-scope="scope">
          <el-popover placement="right" width="400" trigger="click">
            <div>{{scope.row}}</div>
            <el-button slot="reference" @click="handleClick(scope.row)" type="text" size="small">编辑</el-button>
          </el-popover>
          <el-button type="text" size="small">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <footer class="tools flex">
      <el-pagination
        class="page"
        @current-change="handleCurrentChange"
        :current-page.sync="currentPage"
        :page-size="100"
        layout="prev, pager, next, jumper"
        :total="1000"
      ></el-pagination>
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
          'name': '7171823@qq.com',
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
    handleCurrentChange(val) {
      console.log(val)
    }
  }
}
</script>

<style lang="scss" scoped>
.userList {
  padding-top: 10px;
  .tools {
    margin-top: 10px;
    justify-content: space-around;
  }
}
</style>
