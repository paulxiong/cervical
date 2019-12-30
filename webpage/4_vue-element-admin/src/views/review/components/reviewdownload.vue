<template>
  <div class="reviewDownload">
    <el-table
      ref="multipleTable"
      :data="reviews"
      tooltip-effect="dark"
      style="width: 50%"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55" />
      <el-table-column label="ID" prop="id" width="50" />
      <el-table-column label="项目ID" prop="pid" width="50" />
      <el-table-column label="预测结果" prop="predict_str" width="150" />
      <el-table-column label="审核结果" prop="true_str" width="150" show-overflow-tooltip />
      <el-table-column label="审核用户" prop="username" width="100" />
      <el-table-column label="审核时间" prop="updated_at" width="150" />
    </el-table>
    <el-button type="primary" @click="downloadReviews">下载选中细胞</el-button>
    <div class="tools flex">
      <el-pagination
        class="page"
        :current-page.sync="currentPage"
        :page-sizes="[10, 20, 30, 50]"
        :page-size="currentPageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @current-change="handleCurrentChange"
        @size-change="handleSizeChange"
      />
    </div>
  </div>
</template>

<script>
import { APIUrl } from '@/const/config'
import { getLabelReviews, downloadReviews } from '@/api/cervical'
import { parseTime } from '@/utils/index'
import { cellsType } from '@/const/const'

export default {
  name: 'ReviewDownload',
  components: {},
  data() {
    return {
      hosturlpath64: APIUrl + '/imgs/',
      reviews: [],
      selectedList: [],
      total: 0,
      currentPage: 1,
      currentPageSize: 30,
      loading: false
    }
  },
  created() {
    this.getLabelReviews(this.currentPageSize, 1)
  },
  methods: {
    handleSizeChange(val) {
      this.currentPageSize = val
      this.getLabelReviews(this.currentPageSize, 1)
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.getLabelReviews(this.currentPageSize, 1)
    },
    handleSelectionChange(val) {
      this.selectedList = []
      val.map(v => {
        this.selectedList.push(v.id)
      })
    },
    getLabelReviews(limit, status) {
      this.loading = true
      getLabelReviews({ limit: limit, skip: 0, status: status, owner: 1 }).then(res => {
        this.reviews = []
        if (res.data.data.reviews.length) {
          this.reviews = res.data.data.reviews
        }
        this.reviews.map(v => {
          v.updated_at = parseTime(v.updated_at)
          v.verified_by = v.username || '普通用户'
          v.predict_str = cellsType[v.predict_type]
          v.true_str = cellsType[v.true_type]
        })
        this.total = res.data.data.total
        this.loading = false
      })
    },
    downloadReviews() {
      this.loading = true
      const postData = { 'reviews': this.selectedList }
      downloadReviews(postData).then(res => {
        const blob = new Blob([res.data])
        if (window.navigator.msSaveOrOpenBlob) {
          navigator.msSaveBlob(blob, 'nb')
        } else {
          const link = document.createElement('a')
          const evt = document.createEvent('HTMLEvents')
          evt.initEvent('click', false, false)
          link.href = URL.createObjectURL(blob)
          link.download = '已审核细胞图.zip'
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
.reviewAssignment2 {
  overflow: auto;
  height: 100%;
  padding-bottom: 30px;
  .temp-box {
    justify-content: flex-start;
    align-items: flex-start;
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
    width: calc(100% / 2);
  }
}
</style>
