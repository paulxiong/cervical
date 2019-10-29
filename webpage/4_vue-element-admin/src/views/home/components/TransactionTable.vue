<template>
  <el-table :data="list" style="width: 100%;padding-top: 15px;">
    <el-table-column label="订单号" min-width="200">
      <template slot-scope="scope">
        {{ scope.row.order_no | orderNoFilter }}
      </template>
    </el-table-column>
    <el-table-column label="价格" width="195" align="center">
      <template slot-scope="scope">
        ¥{{ scope.row.price | toThousandFilter }}
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
          order_no: 'effDBce2-2E8C-4148-66e9-CBD1Ae',
          price: '213',
          status: 'success'
        },
        {
          order_no: 'effDBce2-2E8C-4148-66e9-CBD1Ae',
          price: '213',
          status: 'success'
        },
        {
          order_no: 'effDBce2-2E8C-4148-66e9-CBD1Ae',
          price: '213',
          status: 'pending'
        },
        {
          order_no: 'effDBce2-2E8C-4148-66e9-CBD1Ae',
          price: '213',
          status: 'success'
        },
        {
          order_no: 'effDBce2-2E8C-4148-66e9-CBD1Ae',
          price: '213',
          status: 'pending'
        },
        {
          order_no: 'effDBce2-2E8C-4148-66e9-CBD1Ae',
          price: '213',
          status: 'pending'
        },
        {
          order_no: 'effDBce2-2E8C-4148-66e9-CBD1Ae',
          price: '213',
          status: 'success'
        },
        {
          order_no: 'effDBce2-2E8C-4148-66e9-CBD1Ae',
          price: '213',
          status: 'pending'
        }
      ]
    }
  }
}
</script>
