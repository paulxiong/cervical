<template>
  <div class="datasetsData">
    <div class="filter-box">
      <el-table
        v-loading="loading"
        element-loading-text="拼命加载中"
        :data="datasetsList"
        style="width: 100%"
      >
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="table-expand">
              <el-form-item label="目录">
                <span>{{ props.row.dir }}</span>
              </el-form-item>
              <el-form-item label="创建者">
                <span>{{ props.row.username }}</span>
              </el-form-item>
              <el-form-item label="裁剪模型">
                <span>{{ props.row.parameter_mid }}</span>
              </el-form-item>
              <el-form-item label="裁剪是否用缓存">
                <span>{{ props.row.parameter_cache }}</span>
              </el-form-item>
              <el-form-item label="裁剪采用颜色">
                <span>{{ props.row.parameter_gray }}</span>
              </el-form-item>
              <el-form-item label="裁剪采用大小">
                <span>{{ props.row.parameter_size }}</span>
              </el-form-item>
              <el-form-item label="裁剪开始时间">
                <span>{{ props.row.processtime }}</span>
              </el-form-item>
              <el-form-item label="裁剪结束">
                <span>{{ props.row.processend }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column label="ID" width="60" prop="id" />
        <el-table-column label="描述" prop="desc" />
        <el-table-column label="创建者">
          <template slot-scope="scope">
            <el-tooltip v-if="scope.row.username" :content="scope.row.username" placement="right">
              <el-image
                style="width:36px;height:36px;border-radius:7px;"
                :src="scope.row.userimg"
                lazy
              >
                <div slot="error" class="image-slot">
                  <i class="el-icon-picture-outline" />
                </div>
              </el-image>
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
        <el-table-column label="裁剪模型" prop="parameter_mid" />
        <el-table-column label="创建时间" prop="created_at" />
        <el-table-column label="状态/剩余时间(秒)" prop="statusTime">
          <template slot-scope="scope">
            <el-tag :type="scope.row.statusType" effect="light">{{ scope.row.statusTime }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column fixed="right" label="操作" width="100">
          <template slot-scope="scope">
            <!-- <el-button type="primary" size="mini" @click="goDetail(scope.row)">查看</el-button> -->
            <!-- <el-button type="warning" style="color: red;" size="mini">删除</el-button> -->
            <!-- <el-button type="danger" icon="el-icon-delete" circle>删除</el-button> -->
            <el-button size="small" type="danger" icon="el-icon-delete" @click="handleDelete(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-dialog title="提示" :visible.sync="delVisible" width="300px" center>
        <div class="del-dialog-cnt">删除不可恢复，是否确定删除？</div>
        <span slot="footer" class="dialog-footer">
          <el-button @click="delVisible = false">取 消</el-button>
          <el-button type="primary" @click="deleteRow">确 定</el-button>
        </span>
      </el-dialog>

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
        :title="upload ? '上传数据' : '新建数据集'"
        :visible.sync="dialogFormVisible"
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
          <el-button v-show="step===3 || step===2" size="mini" @click="stepBack">上一步</el-button>
          <el-button
            v-show="step===1 || step===2"
            size="mini"
            :disabled="!uploadServer && !imgChecked && !modelChecked"
            type="primary"
            @click="stepNext"
          >下一步</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import { listdatasets, removeDataSet } from '@/api/cervical'
import { taskStatus, createdBy, taskType } from '@/const/const'
import { parseTime } from '@/utils/index'

export default {
  name: 'DatasetsData',
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
      currentPage: parseInt(localStorage.getItem('page_index')) ? parseInt(localStorage.getItem('page_index')) : 1,
      currentPageSize: parseInt(localStorage.getItem('page_size')) ? parseInt(localStorage.getItem('page_size')) : 10,
      loading: false,
      modelChecked: false,
      removedataset: [],
      delVisible: false,
      msg: '',
      did: '',
      delarr: [],
      listQuery: {
        desc: undefined,
        type: undefined
      },
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
    this.listdatasets(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
  },
  methods: {
    handleDelete(did) {
      this.did = did
      this.delVisible = true
    },
    deleteRow() {
      removeDataSet({ did: this.did }).then(res => {
        if (res.data && res.data.status === 0) {
          this.$message.success('删除成功')
        }
        this.listdatasets(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
        this.delVisible = false
      })
    },

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
      this.listdatasets(10, (this.currentPage - 1) * this.currentPageSize, 1)
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
      localStorage.setItem('TAB', this.activename)
      localStorage.setItem('details_title', val.desc)
      localStorage.setItem('page_index', this.currentPage)
      localStorage.setItem('page_size', this.currentPageSize)
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
            v.created_by = createdBy[v.created_by] || '普通用户'
            v.statusType = taskType[v.status]
            v.statusTime = v.status === '开始' ? `${v.status}(${v.ETA}s)` : taskStatus[v.status]
            v.parameter_cache = v.parameter_cache === 1 ? '使用' : '不使用'
            v.parameter_gray = v.parameter_gray === 1 ? '灰色' : '彩色'
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
