<template>
  <div class="modelData">
    <keep-alive>
      <router-view v-if="$route.meta.keepAlive" />
    </keep-alive>
    <div class="filter-box">
      <el-button
        class="filter-btn"
        type="primary"
        :icon="loading?'el-icon-loading':'el-icon-refresh-left'"
        @click="filterSearch"
      >刷新</el-button>
      <el-button
        class="filter-btn"
        style="margin-left: 10px;"
        type="success"
        icon="el-icon-upload"
        @click="createModel"
      >新增模型</el-button>
    </div>
    <el-table
      v-loading="loading"
      element-loading-text="拼命加载中"
      :data="modelLists"
      style="width: 100%"
    >
      <el-table-column
        label="模型ID"
        prop="id"
        width="100"
      />
      <el-table-column
        label="描述"
        prop="desc"
      />
      <el-table-column
        label="模型类型"
        prop="modelType"
      />
      <el-table-column
        label="准确度"
        prop="precision"
      />
      <el-table-column
        label="创建时间"
        prop="created_at"
      />
      <el-table-column
        label="召回率"
        prop="recall"
      />
      <el-table-column
        label="损失"
        prop="loss"
      />
      <el-table-column
        label="训练用图数"
        prop="n_train"
      />
      <el-table-column
        label="类型"
        prop="types"
      />
    </el-table>
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
    <el-dialog
      :title="'上传模型(根据指定步骤上传模型)'"
      :visible.sync="dialogFormVisible"
      @closed="closedDialog"
    >
      <div slot="footer" class="dialog-footer">
        <uploadModel
          v-if="upload"
          ref="uploadModel"
          style="margin-top:-30px;"
          @checkUpload="checkUpload"
          @checkModel="checkModel"
        />
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getListmodel } from '@/api/cervical'
import { taskStatus, createdBy, taskType, modelType } from '@/const/const'
import { parseTime } from '@/utils/index'
import uploadModel from './uploadModel'

export default {
  name: 'ModelData',
  components: { uploadModel },
  data() {
    return {
      step: 1,
      currentPage: 1,
      currentPageSize: 10,
      loading: false,
      total: undefined,
      modelLists: [],
      dialogFormVisible: false,
      upload: false,
      listQuery: {
        desc: undefined,
        type: undefined
      },
      typeOptions: [
        {
          key: '0',
          name: '全部'
        },
        {
          key: '1',
          name: '训练'
        },
        {
          key: '2',
          name: '预测'
        }
      ]
    }
  },
  created() {
    this.getListmodel(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 52)
  },
  methods: {
    createModel() {
      this.dialogFormVisible = true
      this.upload = true
    },
    uploadModel() {
      this.dialogFormVisible = true
      this.upload = true
    },
    checkUpload(val) {
      this.$emit('checkUpload', val)
    },
    checkModel(val) {
      this.modelChecked = val
    },
    closedDialog() {
      this.$refs.uploadModel.step = 1
    },
    filterSearch() {
      this.getListmodel(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 52)
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.getListmodel(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 52)
    },
    handleSizeChange(val) {
      this.currentPageSize = val
      this.getListmodel(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 52)
    },
    goDetail(val) {
      localStorage.setItem('TAB', this.activename)
      localStorage.setItem('details_title', val.desc)
      localStorage.setItem('page_index', this.currentPage)
      localStorage.setItem('page_size', this.currentPageSize)
      this.$router.push({
        path: `/workSpace/details?did=${val.id}`
      })
    },
    getListmodel(limit, skip, type) {
      this.loading = true
      // 0未知 1UNET 2GAN 3SVM 4MASKRCNN 5AUTOKERAS 6MALA 50全部的裁剪模型(没做) 51全部的分类模型 52全部模型
      getListmodel({ 'limit': limit, 'skip': skip, 'type': type }).then(res => {
        res.data.data.models.map(v => {
          v.created_at = parseTime(v.created_at)
          v.created_by = createdBy[v.created_by] || '普通用户'
          v.statusType = taskType[v.status]
          v.statusTime = v.status === '开始' ? `${v.status}(${v.ETA}s)` : taskStatus[v.status]
          v.modelType = modelType[v.type]
          v.precision = parseFloat(v.precision).toFixed(2)
        })
        this.modelLists = res.data.data.models
        this.total = res.data.data.total
        this.loading = false
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.modelData {
  overflow: auto;
  height: 100%;
  padding-bottom: 30px;
  .filter-box {
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
    width: calc(100% / 4);
  }
}
</style>
