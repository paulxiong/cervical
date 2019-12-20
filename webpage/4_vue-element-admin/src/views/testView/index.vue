<template>
  <div class="temps">
    <h2>资源管理</h2>
    <el-table
      :data="tableData"
      border
      style="width: 100%"
    >
      <el-table-column
        fixed
        prop="date"
        label="日期"
      />
      <el-table-column
        prop="name"
        label="用户名"
      />
      <el-table-column
        prop="city"
        label="城市"
      />
      <el-table-column
        prop="desc"
        label="描述"
      />
      <el-table-column
        prop="dataid"
        label="数据集"
      />
      <el-table-column
        prop="type"
        label="类型"
      />
      <el-table-column
        fixed="right"
        label="操作"
        width="100"
      >
        <template slot-scope="scope">
          <el-button type="text" size="small" @click="handleClick(scope.row)">查看</el-button>
          <el-button type="text" size="small">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: 'Temps',
  components: {},
  data() {
    return {
      tableData: [{
        date: '2019-12-02',
        name: '717138552@qq.com',
        city: '昆明',
        desc: '数据集下载',
        dataid: '10000',
        type: 'HOWTOMALA'
      }, {
        date: '2019-12-12',
        name: 'xundong',
        city: '昆明',
        desc: '数据集下载',
        dataid: '10001',
        type: 'MASKRCNN'
      }, {
        date: '2019-12-20',
        name: '123456789@qq.com',
        city: '昆明',
        desc: '数据集下载',
        dataid: '10002',
        type: 'HOWTOMALA'
      }, {
        date: '2019-12-02',
        name: 'xundong',
        city: '昆明',
        desc: '数据集下载',
        dataid: '10003',
        type: 'HOWTOMALA'
      }]
    }
  },
  methods: {
    handleClick(row) {
      console.log(row)
    }
  }
}
</script>

<style lang="scss" scoped>
.temps {
  padding: 10px;
}
</style>
