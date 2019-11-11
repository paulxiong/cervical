<template>
  <el-table :data="list" style="width: 100%;padding-top: 7px;">
    <el-table-column label="近期项目ID" min-width="150">
      <template slot-scope="scope">
        {{ scope.row.order_no | orderNoFilter }}
      </template>
    </el-table-column>
    <el-table-column label="描述" width="150" align="center">
      <template slot-scope="scope">
        {{ scope.row.describe |describeFilter }}
      </template>
    </el-table-column>
    <el-table-column label="数据集ID" width="150" align="center">
      <template slot-scope="scope">
        {{ scope.row.did | dataIDFilter }}
      </template>
    </el-table-column>
    <el-table-column label="状态" width="150" align="center">
      <template slot-scope="scope">
        <el-tag :type="scope.row.status | statusFilter">
          {{ scope.row.status }}
        </el-tag>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        success: 'success',
        pending: 'danger'
      }
      return statusMap[status]
    },
    orderNoFilter(str) {
      return str.substring(0, 30)
    },
    dataIDFilter(str) {
      return str.substring(0, 50)
    },
    describeFilter(str) {
      return str.substring(0, 100)
    }
  },
  data() {
    return {
      projectlist: [],
      list: null
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.list = [
        {
          order_no: '36',
          did: '47',
          describe: '123ad',
          status: 'pending'
        },
        {
          order_no: '35',
          did: '47',
          describe: 'bh',
          status: 'pending'
        },
        {
          order_no: '34',
          did: '47',
          describe: 'sdfx',
          status: 'pending'
        },
        {
          order_no: '33',
          did: '47',
          describe: '31231',
          status: 'pending'
        },
        {
          order_no: '32',
          did: '47',
          describe: '123',
          status: 'pending'
        }
      ]
    }
  }
}
</script>
