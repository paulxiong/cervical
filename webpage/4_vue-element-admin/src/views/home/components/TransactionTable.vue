<template>
  <el-table :data="list" style="width: 100%;padding-top: 15px;">
    <el-table-column label="任务编号" min-width="200">
      <template slot-scope="scope">
        {{ scope.row.order_no | orderNoFilter }}
      </template>
    </el-table-column>
    <el-table-column label="剩余时间" width="195" align="center">
      <template slot-scope="scope">
        {{ scope.row.price | toThousandFilter }}(分钟)
      </template>
    </el-table-column>
    <el-table-column label="状态" width="100" align="center">
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
          order_no: '201910011200',
          price: '30',
          status: 'success'
        },
        {
          order_no: '201910051100',
          price: '60',
          status: 'success'
        },
        {
          order_no: '201910101400',
          price: '90',
          status: 'pending'
        },
        {
          order_no: '201910150200',
          price: '120',
          status: 'success'
        },
        {
          order_no: '201910200100',
          price: '150',
          status: 'pending'
        },
        {
          order_no: '201910220400',
          price: '180',
          status: 'pending'
        },
        {
          order_no: '201910250800',
          price: '210',
          status: 'success'
        },
        {
          order_no: '201910300000',
          price: '240',
          status: 'pending'
        }
      ]
    }
  }
}
</script>
