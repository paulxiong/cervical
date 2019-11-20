<template>
  <div class="projectData">
    <el-table :data="projectlist" style="width: 100%;padding-top: 7px;">
      <el-table-column label="近期项目ID" min-width="150">
        <template slot-scope="scope">
          {{ scope.row.id }}
        </template>
      </el-table-column>
      <el-table-column label="描述" width="150" align="center">
        <template slot-scope="scope">
          {{ scope.row.desc }}
        </template>
      </el-table-column>
      <el-table-column label="数据集ID" width="150" align="center">
        <template slot-scope="scope">
          {{ scope.row.did }}
        </template>
      </el-table-column>
      <el-table-column label="创建时间" width="150" align="center">
        <template slot-scope="scope">
          {{ scope.row.starttime }}
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getListprojects } from '@/api/cervical'
import { parseTime } from '@/utils/index'

export default {
  name: 'ProjectData',
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
          v.starttime = parseTime(v.starttime)
          v.statusTime = v.status === '开始' ? `${v.status}(${v.ETA}s)` : v.status
        })
        this.projectlist = res.data.data.projects
        this.total = res.data.data.total
        this.loading = false
      })
    }
  }
}
</script>
