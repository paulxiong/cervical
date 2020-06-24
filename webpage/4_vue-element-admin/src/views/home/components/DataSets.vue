<template>
  <div class="dataSets">
    <el-table :data="datasetsList" max-height="300">
      <el-table-column :label="$t('dashboard.datasetID')" width="100" prop="id" />
      <el-table-column :label="$t('dashboard.datasetDesc')" prop="desc" />
      <el-table-column :label="$t('dashboard.datasetTS')" prop="created_at" />
      <el-table-column :label="$t('dashboard.datasetETA')" prop="statusTime">
        <template slot-scope="scope">
          <el-tag :type="scope.row.statusType" effect="light">{{ $t(scope.row.statusTime) }}</el-tag>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { listdatasets } from '@/api/cervical'
import { taskStatus, taskType } from '@/const/const'
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
      }
    }
  },
  created() {
    this.listdatasets(5, 0, 1)
  },
  methods: {
    listdatasets(limit, skip, order) {
      this.loading = true
      listdatasets({ 'limit': limit, 'skip': skip, 'order': order }).then(res => {
        if (res.data.data.total > 0) {
          res.data.data.datasets.map(v => {
            v.created_at = parseTime(v.created_at)
            v.statusType = taskType[v.status]
            v.statusTime = v.status === '开始' ? `${v.status}(${v.ETA}s)` : taskStatus[v.status]
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

