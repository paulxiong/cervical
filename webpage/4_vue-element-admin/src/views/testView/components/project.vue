<template>
  <div class="projectData">
    <div class="filter-box">
      <span>阳性判断标准：</span>

      <el-form label-width="auto" class="demo-dynamic">
        <el-form-item label-width="auto" label="A 阳性细胞在总细胞的占比大于%">
          <el-input-number v-model="threshold1" :precision="2" :step="0.1" :max="20" />
        </el-form-item>
        <el-form-item label-width="auto" label="C 平均每个FOV阳性细胞个数大于">
          <el-input-number v-model="threshold2" :precision="2" :step="0.1" :max="20" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="recheckpn">计算阴阳性</el-button>
        </el-form-item>
      </el-form>

      <el-dialog
        title="请填写病例的诊断结果以及备注"
        :visible.sync="dialogVisible"
        width="30%"
      >
        <div slot="title" class="header-title">
          <span class="title-age">{{ currentproject.id }} {{ currentproject.desc }}</span>
        </div>
        <div style="height: 60px;">
          <span>1 请选择实际诊断结果</span>
          <el-select v-model="value" placeholder="请选择">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </div>
        <div>
          <span>2 请填写备注</span>
          <el-input
            v-model="inputremark"
            autofocus
            placeholder="输入备注，可以为空"
            show-word-limit
            maxlength="60"
            class="input-name"
          />
        </div>
        <span slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="handleSaveResult()">录入</el-button>
        </span>
      </el-dialog>

      <el-table
        ref="multipleTable"
        :data="projects"
        tooltip-effect="dark"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="50" />
        <el-table-column label="id" width="70">
          <template slot-scope="scope">{{ scope.row.id }}</template>
        </el-table-column>
        <el-table-column prop="desc" label="描述" width="200" show-overflow-tooltip />
        <el-table-column prop="dir" label="dir" show-overflow-tooltip />
        <el-table-column prop="did" label="did" />
        <el-table-column prop="ddir" label="ddir" show-overflow-tooltip />
        <el-table-column prop="cnt50" label="阴性" />
        <el-table-column prop="cnt51" label="阳性" />
        <el-table-column prop="cnt200" label="杂质" />
        <el-table-column prop="fov" label="FOV个数" />
        <el-table-column prop="cellstotal" label="细胞总数" />
        <el-table-column prop="ppercent" label="阳性占比%" />
        <el-table-column prop="cellspfov" label="阳性/FOV" />
        <el-table-column prop="p1n0name" label="结果" />
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button v-if="scope.row.saved === 1" size="mini" type="success" @click="handleBeforeSaveResult(scope.$index, scope.row)">更新记录</el-button>
            <el-button v-else size="mini" type="danger" @click="handleBeforeSaveResult(scope.$index, scope.row)">录入记录</el-button>
          </template>
        </el-table-column>

      </el-table>
      <div style="margin-top: 20px;" class="selectAll">
        <el-button @click="toggleSelection()">取消选择</el-button>
      </div>
      <div class="tools flex">
        <el-pagination
          class="page"
          :current-page.sync="currentPage"
          :page-sizes="[10, 20, 50, 100, 200]"
          :page-size="currentPageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @current-change="handleCurrentChange"
          @size-change="handleSizeChange"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { getAllPredictResult, createProjectResult } from '@/api/cervical'

export default {
  name: 'ProjectLists',
  data() {
    return {
      projects: [],
      total: 0,
      currentPage: 1,
      currentPageSize: 10,
      multipleSelection: [],
      threshold1: 5.0, // 5%
      threshold2: 2.0,
      dialogVisible: false,
      options: [{
        value: 51,
        label: '阳性'
      }, {
        value: 50,
        label: '阴性'
      }, {
        value: 100,
        label: '未知'
      }],
      value: 100,
      inputremark: '',
      currentproject: { 'id': 0, 'desc': '' }
    }
  },
  mounted() {
    this.getAllPredictResult(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize)
  },
  methods: {
    handleBeforeSaveResult(index, val) {
      this.currentproject = val
      this.dialogVisible = true
    },
    handleSaveResult() {
      this.createProjectResult()
    },
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
    handleCurrentChange(val) {
      this.currentPage = val
      this.getAllPredictResult(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize)
    },
    handleSizeChange(val) {
      this.currentPageSize = val
      this.getAllPredictResult(val, (this.currentPage - 1) * this.currentPageSize)
    },
    makeprojectlists(projectdata) {
      projectdata.map(v => {
        if (!v.result || v.result.length < 1) {
          return
        }
        const projects = { 'id': v.id, 'did': v.did, 'cnt50': 0, 'cnt51': 0,
          'cnt200': 0, 'fov': v.fovcnt, 'dir': v.dir, 'desc': v.desc, 'saved': v.saved,
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
      this.getAllPredictResult(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize)
    },
    checkpn() {
      if (!this.projects || this.projects.length < 1) {
        return
      }
      this.projects.map(v => {
        if (v.ppercent > this.threshold1 && v.cellspfov > this.threshold2) {
          v.p1n0 = 51
          v.p1n0name = '阳性'
        } else {
          v.p1n0 = 50
          v.p1n0name = '阴性'
        }
      })
    },
    getAllPredictResult(limit, skip) {
      this.loading = true
      getAllPredictResult({ 'limit': limit, 'skip': skip, 'order': 1, 'status': 5 }).then(res => {
        this.projects = []
        if (!res.data.data || !res.data.data.projects || res.data.data.projects.length < 1) {
          return
        }
        this.total = res.data.data.total
        this.makeprojectlists(res.data.data.projects)
        this.checkpn()
      })
    },
    createProjectResult() {
      this.loading = true
      const postdata = {
        'desc': this.currentproject.desc,
        'did': this.currentproject.did,
        'pid': this.currentproject.id,
        'fovcnt': this.currentproject.fov,
        'ncnt': this.currentproject.cnt50,
        'pcnt': this.currentproject.cnt51,
        'ucnt': this.currentproject.cnt200,
        'p1n0': this.currentproject.p1n0,
        'remark': this.inputremark,
        'truep1n0': this.value
      }
      createProjectResult(postdata).then(res => {
        this.loading = false
        this.dialogVisible = false
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.projectData {
  overflow: auto;
  height: 100%;
  padding-bottom: 30px;
  .selectAll {
    margin-bottom: 5px;
  }
  .tools {
    background: #fff;
    justify-content: space-around;
    bottom: 0px;
    position: fixed;
    left: 0;
    right: 0;
    margin-left: auto;
    margin-right: auto;
  }
}
</style>
