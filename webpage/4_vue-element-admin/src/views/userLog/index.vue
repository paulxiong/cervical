<template>
  <div class='userLog'>
    <el-table
      :data="userLog"
      style="width: 100%">
      <el-table-column
        prop="id"
        label="ID"
        width="180">
      </el-table-column>
      <el-table-column
        prop="user_id"
        label="用户ID"
        width="180">
      </el-table-column>
      <el-table-column
        prop="ip"
        label="IP"
        width="180">
      </el-table-column>
      <el-table-column
        prop="path"
        label="路径">
      </el-table-column>
      <el-table-column
        prop="region.city"
        label="地址">
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getUserLog } from '@/api/user'

export default {
  name: 'UserLog',
  components: {},
  data() {
    return {
      userLog: []
    }
  },
  methods: {
    getUserLog() {
      getUserLog({ 'limit': 100, 'skip': 0, 'order': 1 }).then(res => {
        this.userLog = res.data.data.accesslog
      })
    }
  },
  mounted() {
   this.getUserLog() 
  }
}
</script>

<style lang="scss" scoped>
.userLog {
}
</style>
