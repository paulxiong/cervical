<template>
  <el-table :data="list" style="width: 100%;padding-top: 7px;">
    <el-table-column label="模型ID" min-width="150">
      <template slot-scope="scope">
        {{ scope.row.order_no | orderNoFilter }}
      </template>
    </el-table-column>
    <el-table-column label="描述" width="150" align="center">
      <template slot-scope="scope">
        {{ scope.row.describe |describeFilter }}
      </template>
    </el-table-column>
    <el-table-column label="类型" width="150" align="center">
      <template slot-scope="scope">
        {{ scope.row.modelType | dataIDFilter }}
      </template>
    </el-table-column>
    <el-table-column label="准确度" width="150" align="center">
      <template slot-scope="scope">
        {{ scope.row.precision }}
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
export default {
  name: 'BestModel',
  components: {},
  filters: {
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
      value: 'bestModel'
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.list = [
        {
          order_no: '1',
          modelType: 'AUTOKERAS',
          describe: '某某训练得到的模型',
          precision: '0.9'
        },
        {
          order_no: '2',
          modelType: 'MASKRCNN',
          describe: '系统默认自带的裁剪使用的模型',
          precision: '0'
        },
        {
          order_no: '3',
          modelType: 'AUTOKERAS',
          describe: '保存你个某某某训练的模型',
          precision: '0'
        },
        {
          order_no: '4',
          modelType: 'HOWTOMALA',
          describe: '系统默认自带的分类模型,howtoMala提供',
          precision: '0.6666667'
        }
      ]
    }
  }
}
</script>

<style lang="scss" scoped>
.bestModel {
    width: 100%;
    height: 341px;
    background: #fff;
    padding-top: 7px;
}
</style>
