<template>
  <div class="datasetsData">
    <div class="filter-box">
      <el-button
        class="filter-btn"
        type="primary"
        :icon="loading?'el-icon-loading':'el-icon-refresh-left'"
        @click="filterSearch"
      >{{ $t('workspace.projectDataRefresh') }}</el-button>
      <el-button
        class="filter-btn"
        style="margin-left: 10px;"
        type="success"
        icon="el-icon-edit"
        @click="newData"
      >{{ $t('workspace.projectDataAdd') }}</el-button>
      <el-button
        class="filter-btn"
        style="margin-left: 10px;"
        type="success"
        icon="el-icon-upload"
        @click="uploadImgs"
      >{{ $t('workspace.projectDataUpload') }}</el-button>
    </div>
    <el-table
      v-loading="loading"
      :element-loading-text="$t('workspace.projectDataLoading')"
      :data="datasetsList"
      style="width: 100%"
    >
      <el-table-column type="expand">
        <template slot-scope="props">
          <el-form label-position="left" inline class="table-expand">
            <el-form-item :label="$t('workspace.projectDataDir')">
              <span>{{ props.row.dir }}</span>
            </el-form-item>
            <el-form-item :label="$t('workspace.projectDataCreator')">
              <span>{{ props.row.username }}</span>
            </el-form-item>
            <el-form-item :label="$t('workspace.projectDataModel')">
              <span>{{ props.row.parameter_mid }}</span>
            </el-form-item>
            <el-form-item :label="$t('workspace.projectDataCache')">
              <span>{{ props.row.parameter_cache }}</span>
            </el-form-item>
            <el-form-item :label="$t('workspace.projectDataColor')">
              <span>{{ props.row.parameter_gray }}</span>
            </el-form-item>
            <el-form-item :label="$t('workspace.projectDataSize')">
              <span>{{ props.row.parameter_size }}</span>
            </el-form-item>
            <el-form-item :label="$t('workspace.projectDataStartTime')">
              <span>{{ props.row.processtime }}</span>
            </el-form-item>
            <el-form-item :label="$t('workspace.projectDataEndTime')">
              <span>{{ props.row.processend }}</span>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column :label="$t('workspace.projectDataID')" width="60" prop="id" />
      <el-table-column :label="$t('workspace.projectDataDescription')" prop="desc" />
      <el-table-column :label="$t('workspace.projectDataCreator2')">
        <template slot-scope="scope">
          <el-tooltip v-if="scope.row.username" :content="scope.row.username" placement="right">
            <el-image
              :src="scope.row.userimg"
              style="width:36px;height:36px;border-radius:7px;"
            />
            <div slot="error" class="image-slot">
              <i class="el-icon-picture-outline" />
            </div>
          </el-tooltip>
          <el-image
            v-else
            style="width:36px;height:36px;border-radius:7px;"
            :src="scope.row.userimg"
            lazy
          >
            <div slot="error" class="image-slot">
              <i class="el-icon-picture-outline" />
            </div>
          </el-image>
        </template>
      </el-table-column>
      <el-table-column :label="$t('workspace.projectDataModel2')" prop="parameter_mid" />
      <el-table-column :label="$t('workspace.projectDataCreateTime')" prop="created_at" />
      <el-table-column :label="$t('workspace.projectDataStatus')" prop="statusTime">
        <template slot-scope="scope">
          <el-tag :type="scope.row.statusType" effect="light">{{ $t(scope.row.statusTime) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column fixed="right" :label="$t('workspace.projectDataOP')" width="100">
        <template slot-scope="scope">
          <el-button type="primary" size="mini" @click="goDetail(scope.row)">{{ $t('workspace.projectDataDetails') }}</el-button>
        </template>
      </el-table-column>
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
      :title="upload ? $t('workspace.projectDataUpload2') : $t('workspace.projectDataAdd2')"
      :visible.sync="dialogFormVisible"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :show-close="false"
      @closed="closedDialog"
    >
      <newDatasets
        ref="newDatasets"
        :upload="upload"
        style="margin-top:-30px;"
        @checkUpload="checkUpload"
        @checkImg="checkImg"
        @checkModel="checkModel"
      />
      <div slot="footer" class="dialog-footer">
        <el-button v-show="step===3 || step===2" size="mini" @click="stepBack">{{ $t('workspace.projectDataPrevious') }}</el-button>
        <el-button
          v-show="step===1 || step===2"
          size="mini"
          :disabled="!uploadServer && !imgChecked && !modelChecked"
          type="primary"
          @click="stepNext"
        >{{ $t('workspace.projectDataNext') }}</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { listdatasets } from '@/api/cervical'
import { taskStatus, createdBy, taskType } from '@/const/const'
import { parseTime } from '@/utils/index'
import newDatasets from './newDatasets'

export default {
  name: 'DatasetsData',
  components: { newDatasets },
  props: {
    activename: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      datasetsList: [],
      step: 1,
      total: undefined,
      dialogFormVisible: false,
      upload: false,
      uploadServer: false,
      imgChecked: false,
      currentPage: 1,
      currentPageSize: 10,
      loading: false,
      modelChecked: false,
      listQuery: {
        desc: undefined,
        type: undefined
      }
    }
  },
  created() {
    this.listdatasets(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
  },
  methods: {
    uploadImgs() {
      this.dialogFormVisible = true
      this.upload = true
    },
    newData() {
      this.dialogFormVisible = true
      this.upload = false
    },
    stepNext() {
      this.$refs.newDatasets.stepNext()
      this.step = this.$refs.newDatasets.step
      this.uploadServer = true
    },
    stepBack() {
      this.$refs.newDatasets.stepBack()
      this.step = this.$refs.newDatasets.step
      this.uploadServer = false
    },
    closedDialog() {
      this.$refs.newDatasets.step = 1
    },
    checkUpload(val) {
      this.uploadServer = val
    },
    checkImg(val) {
      this.imgChecked = val
    },
    checkModel(val) {
      this.modelChecked = val
    },
    filterSearch() {
      this.listdatasets(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.listdatasets(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
    },
    handleSizeChange(val) {
      this.currentPageSize = val
      this.listdatasets(val, (this.currentPage - 1) * this.currentPageSize, 1)
    },
    goDetail(val) {
      this.$router.push({
        path: `/workSpace/details?did=${val.id}`
      })
    },
    listdatasets(limit, skip, order) {
      this.loading = true
      listdatasets({ 'limit': limit, 'skip': skip, 'order': order }).then(res => {
        if (res.data.data.total > 0) {
          res.data.data.datasets.map(v => {
            v.created_at = parseTime(v.created_at)
            v.updated_at = parseTime(v.updated_at)
            v.processtime = parseTime(v.processtime)
            v.processend = parseTime(v.processend)
            v.created_by = createdBy[v.created_by] || this.$t('workspace.projectNewUser')
            v.statusType = taskType[v.status]
            v.statusTime = v.status === '开始' ? `${v.status}(${v.ETA}s)` : taskStatus[v.status]
            v.parameter_cache = v.parameter_cache === 1 ? this.$t('workspace.projectNewCache') : this.$t('workspace.projectNewNoCache')
            v.parameter_gray = v.parameter_gray === 1 ? this.$t('workspace.projectNewGray') : this.$t('workspace.projectNewColor')
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

<style lang="scss" scoped>
.datasetsData {
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
    width: calc(100% / 4);
  }
}
</style>
