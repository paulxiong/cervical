<template>
  <div class="dataSets">
    <el-table :data="datasetsList" style="width: 100%;padding-top: 7px;">
      <el-table-column label="数据ID" min-width="50">
        <template slot-scope="scope">
          {{ scope.row.id }}
        </template>
      </el-table-column>
      <el-table-column label="描述" width="200" align="center">
        <template slot-scope="scope">
          {{ scope.row.desc }}
        </template>
      </el-table-column>
      <el-table-column label="裁剪模型" width="100" align="center">
        <template slot-scope="scope">
          {{ scope.row.parameter_mid }}
        </template>
      </el-table-column>
      <el-table-column label="创建时间" width="250" align="center">
        <template slot-scope="scope">
          {{ scope.row.created_at }}
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { listdatasets } from '@/api/cervical'
import { parseTime } from '@/utils/index'

export default {
  name: 'DataSets',
  components: {},
  data() {
    return {
      datasetsList: [],
      total: undefined,
      dialogFormVisible: false,
      upload: false,
      uploadServer: false,
      imgChecked: false,
      loading: false,
      listQuery: {
        desc: undefined,
        type: undefined
      },
      typeOptions: [
        {
          key: '0',
          name: '未知'
        },
        {
          key: '1',
          name: '保留'
        },
        {
          key: '2',
          name: '训练'
        },
        {
          key: '3',
          name: '预测'
        }
      ]
    }
  },
  created() {
    this.listdatasets(7, 0, 1)
  },
  methods: {
    listdatasets(limit, skip, order) {
      this.loading = true
      listdatasets({ 'limit': limit, 'skip': skip, 'order': order }).then(res => {
        if (res.data.data.total > 0) {
          res.data.data.datasets.map(v => {
            v.created_at = parseTime(v.created_at)
          })
          this.datasetsList = res.data.data.datasets
          this.total = res.data.data.total
          this.loading = false
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.dataSets {
    // width: 100%;
    // height: 336px;
    // background: #fff;
    // padding-top: 7px;
}
</style>
