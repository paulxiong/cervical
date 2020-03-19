<template>
  <div class="resultData">
    <div class="filter-box">
      <el-table
        ref="multipleTable"
        :data="results"
        tooltip-effect="dark"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column label="id" width="50">
          <template slot-scope="scope">{{ scope.row.id }}</template>
        </el-table-column>
        <el-table-column prop="desc" label="描述" width="150" show-overflow-tooltip />
        <el-table-column prop="pid" label="pid" width="50" />
        <el-table-column prop="did" label="did" width="50" />
        <el-table-column prop="ncnt" label="阴性" width="80" />
        <el-table-column prop="pcnt" label="阳性" width="80" />
        <el-table-column prop="ucnt" label="杂质" width="80" />
        <el-table-column prop="fovcnt" label="FOV个数" width="80" />
        <el-table-column prop="p1n0" label="机器预测结果" width="80" />
        <el-table-column prop="truep1n0" label="医生诊断结果" width="80" />
        <el-table-column prop="remark" label="备注" width="150" />
      </el-table>
      <div style="margin-top: 20px">
        <el-button @click="toggleSelection()">取消选择</el-button>
        <el-button type="primary" @click="downloadResults">下载选中记录</el-button>
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
import { listProjectResult, downloadResults } from '@/api/cervical'

export default {
  name: 'ResultLists',
  data() {
    return {
      results: [],
      total: 0,
      currentPageSize: 200,
      currentPage: 0,
      selectedList: []
    }
  },
  mounted() {
    this.listProjectResult(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize)
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
      this.selectedList = []
      val.map(v => {
        this.selectedList.push(v.id)
      })
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.listProjectResult(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize)
    },
    handleSizeChange(val) {
      this.currentPageSize = val
      this.listProjectResult(val, (this.currentPage - 1) * this.currentPageSize)
    },
    listProjectResult(limit, skip) {
      this.loading = true
      listProjectResult({ 'limit': limit, 'skip': skip }).then(res => {
        this.results = []
        if (!res.data.data || !res.data.data.results || res.data.data.results.length < 1) {
          return
        }
        this.results = res.data.data.results
        this.total = res.data.data.total
      })
    },
    downloadResults() {
      this.loading = true
      const postData = { 'ids': this.selectedList }
      downloadResults(postData).then(res => {
        const blob = new Blob([res.data])
        if (window.navigator.msSaveOrOpenBlob) {
          navigator.msSaveBlob(blob, 'nb')
        } else {
          const link = document.createElement('a')
          const evt = document.createEvent('HTMLEvents')
          evt.initEvent('click', false, false)
          link.href = URL.createObjectURL(blob)
          link.download = 'result.csv'
          link.style.display = 'none'
          document.body.appendChild(link)
          link.click()
          window.URL.revokeObjectURL(link.href)
        }
        this.$message({
          message: '下载成功',
          type: 'success'
        })
        this.downloadLoading = false
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.resultData {
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
}
</style>
