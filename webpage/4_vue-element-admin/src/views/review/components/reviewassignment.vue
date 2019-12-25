<template>
  <div class="reviewAssignment">
    <el-radio-group v-model="pid" @change="handlepidchange">
      <el-radio-button v-for="item in projectlist" :key="item.id" :label="item.id" />
    </el-radio-group>
    <div class="tools flex">
      <el-pagination
        class="page"
        :current-page.sync="projectcurrentPage"
        :page-sizes="[20, 30, 50, 100]"
        :page-size="10"
        layout="total, sizes, prev, pager, next, jumper"
        :total="projecttotal"
        @current-change="handleprojectCurrentChange"
        @size-change="handleprojectSizeChange"
      />
    </div>

    <el-table
      ref="multipleTable"
      :data="predicts"
      tooltip-effect="dark"
      style="width: 100%"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55" />
      <el-table-column label="id" width="100">
        <template slot-scope="scope">{{ scope.row.id }}</template>
      </el-table-column>
      <el-table-column prop="predict_str" label="预测结果" width="200" />
      <el-table-column prop="true_str" label="初审核结果" width="200" />

    </el-table>
    <div style="margin-top: 20px">
      <el-button type="primary" @click="setPredictsReview()">生成细胞审核任务</el-button>
    </div>
    <div class="tools flex">
      <el-pagination
        class="page"
        :current-page.sync="currentPage"
        :page-sizes="[10, 20, 30, 50]"
        :page-size="10"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @current-change="handleCurrentChange"
        @size-change="handleSizeChange"
      />
    </div>
  </div>
</template>

<script>
import { getPredictsByPID, getListprojects, setPredictsReview } from '@/api/cervical'
import { cellsType } from '@/const/const'

export default {
  name: 'ReviewAssignment',
  components: {},
  data() {
    return {
      currentPageSize: 10,
      currentPage: 0,
      predicts: [],
      multipleSelection: [],
      pid: 0,
      total: 0,
      projectlist: [],
      projecttotal: 0,
      projectcurrentPageSize: 20,
      projectcurrentPage: 0
    }
  },
  mounted() {
    this.getPredictsByPID(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, this.pid)
    this.getListprojects(this.projectcurrentPageSize, (this.projectcurrentPage - 1) * this.projectcurrentPageSize)
  },
  methods: {
    filterSearch() {
    },
    handlepidchange(val) {
      this.getPredictsByPID(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, this.pid)
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.getPredictsByPID(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, this.pid)
    },
    handleSizeChange(val) {
      this.currentPageSize = val
      this.getPredictsByPID(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, this.pid)
    },
    handleSelectionChange(val) {
      this.multipleSelection = []
      val.map(v => {
        this.multipleSelection.push(v.id)
      })
    },
    handleprojectCurrentChange(val) {
      this.projectcurrentPage = val
      this.getListprojects(this.projectcurrentPageSize, (this.projectcurrentPage - 1) * this.projectcurrentPageSize)
    },
    handleprojectSizeChange(val) {
      this.projectcurrentPageSize = val
      this.getListprojects(this.projectcurrentPageSize, (this.projectcurrentPage - 1) * this.projectcurrentPageSize)
    },
    getPredictsByPID(limit, skip, pid) {
      this.loading = true
      getPredictsByPID({ 'limit': limit, 'skip': skip, 'pid': pid, 'status': 1 }).then(res => {
        this.predicts = []
        this.total = 0
        if (!res.data.data || !res.data.data.predicts || res.data.data.predicts.length < 1) {
          return
        }
        this.total = res.data.data.total
        this.predicts = res.data.data.predicts
        this.predicts.map(v => {
          v.predict_str = cellsType[v.predict_type]
          v.true_str = cellsType[v.true_type]
        })
      })
    },
    getListprojects(limit, skip, order) {
      this.loading = true
      getListprojects({ 'limit': limit, 'skip': skip, 'order': order }).then(res => {
        this.projectlist = res.data.data.projects
        this.projecttotal = res.data.data.total
        this.loading = false
      })
    },
    setPredictsReview() {
      this.loading = true
      const postData = {
        'pid': this.pid,
        'predicts': this.multipleSelection,
        'vid': 0
      }
      setPredictsReview(postData).then(res => {
        this.loading = false
        this.getPredictsByPID(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, this.pid)
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.recycleData {
  overflow: auto;
  height: 100%;
  padding-bottom: 30px;
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
  .table-expand {
    font-size: 0;
  }
  .table-expand label {
    width: 90px;
    color: #99a9bf;
  }
  .table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
  }
}
</style>
