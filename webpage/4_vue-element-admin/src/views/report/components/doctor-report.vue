<template>
  <div class="doctor-report">
    <el-table
      v-loading="loading"
      :element-loading-text="$t('report.loading')"
      :data="reportlist"
      style="width: 100%"
    >
      <el-table-column type="expand">
        <template slot-scope="props">
          <el-form label-position="left" inline class="table-expand">
            <el-form-item :label="$t('report.results')">
              <span>{{ $t(props.row.predictType) }}</span>
            </el-form-item>
            <el-form-item :label="$t('report.directory')">
              <span>{{ props.row.dir }}</span>
            </el-form-item>
            <el-form-item :label="$t('report.creator')">
              <span>{{ props.row.username }}</span>
            </el-form-item>
            <el-form-item :label="$t('report.modelID')">
              <span>{{ props.row.parameter_mid }}</span>
            </el-form-item>
            <el-form-item :label="$t('report.modelType')">
              <span>{{ props.row.parameter_mtype }}</span>
            </el-form-item>
            <el-form-item :label="$t('report.Size')">
              <span>{{ props.row.parameter_resize }}</span>
            </el-form-item>
            <el-form-item :label="$t('report.MaxTime')">
              <span>{{ props.row.parameter_time }}</span>
            </el-form-item>
            <el-form-item :label="$t('report.predictType')">
              <span>{{ props.row.parameter_type === 0 ? $t('report.noLabel') : $t('report.labeled') }}</span>
            </el-form-item>
            <el-form-item :label="$t('report.progress')">
              <span>{{ props.row.percent }}</span>
            </el-form-item>
            <el-form-item :label="$t('report.ETA')">
              <span>{{ props.row.ETA }}</span>
            </el-form-item>
            <el-form-item :label="$t('report.status')">
              <span>{{ $t(props.row.status) }}</span>
            </el-form-item>
            <el-form-item :label="$t('report.startTime')">
              <span>{{ props.row.starttime }}</span>
            </el-form-item>
            <el-form-item :label="$t('report.endTime')">
              <span>{{ props.row.endtime }}</span>
            </el-form-item>
            <el-form-item :label="$t('report.cellTypes')">
              <el-table :data="props.row.cellstype" stripe border style="width: 100%">
                <el-table-column prop="type" width="300" :label="$t('report.type')" />
                <el-table-column prop="total" :label="$t('report.number')" />
                <el-table-column width="110" :label="$t('report.operation')">
                  <template slot-scope="scope">
                    <el-button size="mini" type="success" @click="downloadCells(scope.row)">
                      {{ $t('report.download') }}
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column width="60" label="ID" prop="id" />
      <el-table-column width="360" :label="$t('report.description')" prop="desc" />
      <el-table-column width="150" :label="$t('report.datasetID')" prop="did" />
      <el-table-column :label="$t('report.creator1')">
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
      <el-table-column :label="$t('report.type1')" prop="projectType" />
      <el-table-column :label="$t('report.createdAt')" prop="created_at" />
      <el-table-column width="200" :label="$t('report.ETA1')" prop="statusTime">
        <template slot-scope="scope">
          <el-tag :type="scope.row.statusType" effect="light">{{ scope.row.statusTime }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column fixed="right" :label="$t('report.operation1')" width="100">
        <template slot-scope="scope">
          <el-button type="primary" size="mini" @click="goDetail(scope.row)">{{ $t('report.review') }}</el-button>
          <!-- <el-button type="primary" style="color: #ff3c43;" size="mini">删除</el-button> -->
        </template>
      </el-table-column>
    </el-table>
    <div class="tools flex">
      <pagination
        v-show="total>0"
        class="page"
        :subpath="subpath"
        :total="total"
        :page-sizes="[10, 20, 30, 50]"
        layout="total, sizes, prev, pager, next, jumper"
        @pagination="getList"
      />
    </div>
  </div>
</template>

<script>
import { getListprojects, downloadCellsURL } from '@/api/cervical'
import { taskStatus, createdBy, taskType, projectType, cellsType, medicalType } from '@/const/const'
import { parseTime } from '@/utils/index'
import { APIUrl } from '@/const/config'
import { getToken } from '@/utils/auth'
import Pagination from '@/components/Pagination2'

export default {
  name: 'DoctorReport',
  components: { Pagination },
  data() {
    return {
      reportlist: [],
      loading: false,
      downloadLoading: false,
      total: 0,
      subpath: 'DoctorReport'
    }
  },
  created() {
  },
  methods: {
    getList(val) {
      this.getListreport(val.limit, (val.page - 1) * val.limit, 5, 1)
    },
    goDetail(val) {
      this.$router.push({
        path: `/report/details?pid=${val.id}&did=${val.did}&type=${val.type}&report=doctor`
      })
    },
    // 判断当前病例的阴性阳性
    PNJudgement(cellstotal, posativetotal) {
      let positiveRate = 0
      let predictType = medicalType[100]
      if (cellstotal > 0 && posativetotal > 0) {
        positiveRate = posativetotal * 100 / cellstotal
      }
      // console.log(positiveRate)
      if (positiveRate === 0) {
        predictType = medicalType[100]
      } else if (positiveRate <= 5) {
        predictType = medicalType[50]
      } else if (positiveRate > 5) {
        predictType = medicalType[51]
      }
      return predictType
    },
    getListreport(limit, skip, status, order) {
      this.loading = true
      // status 0初始化 1送去处理 2开始处理 3处理出错 4处理完成 5 送去审核预测结果 6 预测结果审核完成 100 全部 101 送去审核以及核完成的预测结果
      getListprojects({ 'limit': limit, 'skip': skip, 'status': status, 'order': order }).then(res => {
        res.data.data.projects.map(v => {
          v.created_at = parseTime(v.created_at)
          v.updated_at = parseTime(v.updated_at)
          v.starttime = parseTime(v.starttime)
          v.endtime = parseTime(v.endtime)
          v.created_by = createdBy[v.created_by] || '普通用户'
          v.statusType = taskType[v.status]
          v.status = taskStatus[v.status]
          v.statusTime = v.status === '开始' ? `${v.status}(${v.ETA}s)` : this.$t(v.status)
          v.projectType = this.$t(projectType[v.type])
          v.cellstotal = 0
          v.posativetotal = 0
          if (v.cellstype.length) {
            v.cellstype.map(cells => {
              if (cells.type === 50 || cells.type === 51) {
                v.cellstotal += cells.total
              }
              if (cells.type === 51) {
                v.posativetotal += cells.total
              }
              cells['pid'] = v.id
              cells['_type'] = cells.type
              cells['type'] = this.$t(cellsType[cells.type])
            })
          }
          v.predictType = this.PNJudgement(v.cellstotal, v.posativetotal)
        })
        this.reportlist = res.data.data.projects
        this.total = res.data.data.total
        this.loading = false
      })
    },
    downloadCells(cell) {
      if (!cell || !cell._type || !cell.pid) {
        this.$message.error('下载失败，请刷新网页然后重试')
        return
      }
      this.$message({ type: 'success', message: '开始下载' })

      const token = getToken().replace('token ', '')
      // 直接跳转下载页面
      window.location.href = APIUrl + downloadCellsURL + '?pid=' + cell.pid + '&celltype=' + cell._type + '&token=' + token
    }
  }
}
</script>

<style lang="scss" scoped>
.doctor-report {
  overflow: auto;
  height: 100%;
  padding-bottom: 30px;
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
