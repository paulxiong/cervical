<template>
  <div class="medicalReport">
    <el-table :data="projectlist" max-height="300">
      <el-table-column width="100" :label="$t('dashboard.medicalID')" prop="id" />
      <el-table-column :label="$t('dashboard.medicalDesc')" prop="desc" />
      <el-table-column width="100" :label="$t('dashboard.medicalDataset')" prop="did" />
      <el-table-column :label="$t('dashboard.medicalTS')" prop="created_at" width="180" />
      <el-table-column :label="$t('dashboard.medicalETA')" prop="statusTime" width="150">
        <template slot-scope="scope">
          <el-tag :type="scope.row.statusType" effect="light">{{ $t(scope.row.statusTime) }}</el-tag>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getListprojects } from '@/api/cervical'
import { taskStatus, taskType } from '@/const/const'
import { parseTime } from '@/utils/index'

export default {
  name: 'MedicalReport',
  components: {},
  data() {
    return {
      projectlist: [],
      total: undefined,
      dialogFormVisible: false
    }
  },
  created() {
    this.getListprojects(5, 0, 1)
  },
  methods: {
    getListprojects(limit, skip, order) {
      this.loading = true
      getListprojects({ 'limit': limit, 'skip': skip, 'order': order }).then(res => {
        res.data.data.projects.map(v => {
          v.created_at = parseTime(v.created_at)
          v.statusTime = v.status === '开始' ? `${v.status}(${v.ETA}s)` : taskStatus[v.status]
          v.statusType = taskType[v.status]
        })
        this.projectlist = res.data.data.projects
        this.total = res.data.data.total
        this.loading = false
      })
    }
  }
}
</script>
