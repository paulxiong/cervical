<template>
  <div>
    <span>阳性判断标准：</span>

    <el-form label-width="auto" class="demo-dynamic">
      <el-form-item label-width="auto" label="A 阳性细胞在总细胞的占比大于">
        <el-input-number v-model="threshold1" :precision="2" :step="0.1" :max="20" />
      </el-form-item>
      <el-form-item label-width="auto" label="C 平均每个FOV阳性细胞个数大于">
        <el-input-number v-model="threshold2" :precision="2" :step="0.1" :max="20" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="recheckpn">计算阴阳性</el-button>
      </el-form-item>
    </el-form>

    <el-table
      ref="multipleTable"
      :data="projects"
      tooltip-effect="dark"
      style="width: 100%"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55" />
      <el-table-column label="id" width="50">
        <template slot-scope="scope">{{ scope.row.id }}</template>
      </el-table-column>
      <el-table-column prop="desc" label="描述" width="120" show-overflow-tooltip />
      <el-table-column prop="dir" label="dir" width="100" show-overflow-tooltip />
      <el-table-column prop="did" label="did" width="50" />
      <el-table-column prop="ddir" label="ddir" width="100" show-overflow-tooltip />
      <el-table-column prop="cnt50" label="阴性" width="80" />
      <el-table-column prop="cnt51" label="阳性" width="80" />
      <el-table-column prop="cnt200" label="杂质" width="80" />
      <el-table-column prop="fov" label="FOV个数" width="80" />
      <el-table-column prop="cellstotal" label="细胞总数" width="80" />
      <el-table-column prop="ppercent" label="阳性占比" width="80" />
      <el-table-column prop="cellspfov" label="阳性/FOV" width="80" />
      <el-table-column prop="p1n0" label="结果" width="80" />

    </el-table>
    <div style="margin-top: 20px">
      <el-button @click="toggleSelection([tableData[1], tableData[2]])">切换第二、第三行的选中状态</el-button>
      <el-button @click="toggleSelection()">取消选择</el-button>
    </div>
  </div>
</template>

<script>
import { getAllPredictResult } from '@/api/cervical'

export default {
  data() {
    return {
      projects: [],
      multipleSelection: [],
      threshold1: 5.0, // 5%
      threshold2: 2.0
    }
  },
  mounted() {
    this.getAllPredictResult(100, 0, 1)
  },
  methods: {
    toggleSelection(rows) {
      if (rows) {
        rows.forEach(row => {
          this.$refs.multipleTable.toggleRowSelection(row)
        })
      } else {
        this.$refs.multipleTable.clearSelection()
      }
    },
    handleSelectionChange(val) {
      this.multipleSelection = val
    },
    makeprojectlists(projectdata) {
      projectdata.map(v => {
        if (!v.result || v.result.length < 1) {
          return
        }
        const projects = { 'id': v.id, 'did': v.did, 'cnt50': 0, 'cnt51': 0,
          'cnt200': 0, 'fov': v.fovcnt, 'dir': v.dir, 'desc': v.desc,
          'ddir': v.ddir, 'cellstotal': 0, 'ppercent': 0.00, 'cellspfov': 0.00 }
        v.result.map(v2 => {
          if (v2.type === 50) {
            projects.cnt50 = v2.total
          } else if (v2.type === 51) {
            projects.cnt51 = v2.total
          } else if (v2.type === 200) {
            projects.cnt200 = v2.total
          }
        })
        projects.cellstotal = projects.cnt50 + projects.cnt51
        if (projects.cellstotal > 0) {
          projects.ppercent = (projects.cnt51 / projects.cellstotal * 100).toFixed(2)
        }
        if (projects.fov > 0) {
          projects.cellspfov = (projects.cnt51 / projects.fov).toFixed(2)
        }
        this.projects.push(projects)
      })
    },
    recheckpn() {
      this.getAllPredictResult(100, 0, 1)
    },
    checkpn() {
      if (!this.projects || this.projects.length < 1) {
        return
      }
      this.projects.map(v => {
        if (v.ppercent > this.threshold1 && v.cellspfov > this.threshold2) {
          v.p1n0 = '阳性'
        } else {
          v.p1n0 = '阴性'
        }
      })
    },
    getAllPredictResult(limit, skip, order) {
      this.loading = true
      getAllPredictResult({ 'limit': limit, 'skip': skip, 'order': order }).then(res => {
        this.projects = []
        if (!res.data.data || !res.data.data.projects || res.data.data.projects.length < 1) {
          return
        }
        this.makeprojectlists(res.data.data.projects)
        this.checkpn()
      })
    }
  }
}
</script>
