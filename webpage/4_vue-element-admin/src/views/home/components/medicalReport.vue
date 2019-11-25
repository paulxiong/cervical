<template>
  <div class="medicalReport">
    <el-table :data="projectlist">
      <el-table-column width="100" label="报告ID" prop="id" />
      <el-table-column label="描述" prop="desc" />
      <el-table-column width="100" label="数据集" prop="did" />
      <el-table-column label="创建时间" prop="created_at" />
      <el-table-column label="状态/剩余时间(秒)" prop="statusTime">
        <template slot-scope="scope">
          <el-tag :type="scope.row.statusType" effect="dark">{{ scope.row.statusTime }}</el-tag>
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
      dialogFormVisible: false,
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
