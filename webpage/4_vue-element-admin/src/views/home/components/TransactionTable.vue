<template>
  <el-table :data="list" style="width: 100%;padding-top: 15px;">
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
        {{ scope.row.data | dataIDFilter }}
      </template>
    </el-table-column>
    <el-table-column label="状态" width="150" align="center">
      <template slot-scope="{row}">
        <el-tag :type="row.status | statusFilter">
          {{ row.status }}
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
          data: '47',
          describe: '123ad',
          status: '送去处理'
        },
        {
          order_no: '35',
          data: '47',
          describe: 'bh',
          status: '送去处理'
        },
        {
          order_no: '34',
          data: '47',
          describe: 'sdfx',
          status: '送去处理'
        },
        {
          order_no: '33',
          data: '47',
          describe: '31231',
          status: '送去处理'
        },
        {
          order_no: '32',
          data: '47',
          describe: '123',
          status: '送去处理'
        },
        {
          order_no: '31',
          data: '47',
          describe: '4',
          status: '送去处理'
        },
        {
          order_no: '23',
          data: '42',
          describe: '1234',
          status: '开始(0s)'
        },
        {
          order_no: '30',
          data: '47',
          describe: '123ad',
          status: '完成'
        }
      ]
    }
  }
}
</script>
