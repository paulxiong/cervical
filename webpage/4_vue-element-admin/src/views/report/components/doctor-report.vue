<template>
  <div class="doctor-report">
    <el-table
      v-loading="loading"
      element-loading-text="拼命加载中"
      :data="reportlist"
      style="width: 100%"
    >
      <el-table-column type="expand">
        <template slot-scope="props">
          <el-form label-position="left" inline class="table-expand">
            <el-form-item label="病例预测结果">
              <span>{{ props.row.predictType }}</span>
            </el-form-item>
            <el-form-item label="工作目录">
              <span>{{ props.row.dir }}</span>
            </el-form-item>
            <el-form-item label="创建者">
              <span>{{ props.row.username }}</span>
            </el-form-item>
            <el-form-item label="预测模型 ID">
              <span>{{ props.row.parameter_mid }}</span>
            </el-form-item>
            <el-form-item label="预测模型类型">
              <span>{{ props.row.parameter_mtype }}</span>
            </el-form-item>
            <el-form-item label="训练之前统一的尺寸">
              <span>{{ props.row.parameter_resize }}</span>
            </el-form-item>
            <el-form-item label="训练使用的最长时间">
              <span>{{ props.row.parameter_time }}</span>
            </el-form-item>
            <el-form-item label="预测方式">
              <span>{{ props.row.parameter_type === 0 ? '没标注的图' : '有标注的图' }}</span>
            </el-form-item>
            <el-form-item label="进度">
              <span>{{ props.row.percent }}</span>
            </el-form-item>
            <el-form-item label="剩余时间(秒)">
              <span>{{ props.row.ETA }}</span>
            </el-form-item>
            <el-form-item label="状态">
              <span>{{ props.row.status }}</span>
            </el-form-item>
            <el-form-item label="开始处理">
              <span>{{ props.row.starttime }}</span>
            </el-form-item>
            <el-form-item label="结束时间">
              <span>{{ props.row.endtime }}</span>
            </el-form-item>
            <el-form-item label="细胞类型">
              <el-table :data="props.row.cellstype" stripe border style="width: 100%">
                <el-table-column prop="type" width="300" label="类型" />
                <el-table-column prop="total" label="个数" />
                <el-table-column label="操作">
                  <template slot-scope="scope">
                    <el-button size="mini" type="success" @click="downloadCells(scope.row)">
                      下载
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column width="60" label="ID" prop="id" />
      <el-table-column width="360" label="描述" prop="desc" />
      <el-table-column width="150" label="数据集 ID" prop="did" />
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
      <el-table-column label="类型" prop="projectType" />
      <el-table-column label="创建时间" prop="created_at" />
      <el-table-column label="状态/剩余时间(秒)" prop="statusTime">
        <template slot-scope="scope">
          <el-tag :type="scope.row.statusType" effect="light">{{ scope.row.statusTime }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="操作" width="100">
        <template slot-scope="scope">
          <el-button type="primary" size="mini" @click="goDetail(scope.row)">查看</el-button>
          <!-- <el-button type="primary" style="color: #ff3c43;" size="mini">删除</el-button> -->
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
  </div>
</template>

<script>
import { getListprojects, downloadCellsURL } from '@/api/cervical'
import { taskStatus, createdBy, taskType, projectType, cellsType } from '@/const/const'
import { parseTime } from '@/utils/index'
import { APIUrl } from '@/const/config'
import { getToken } from '@/utils/auth'

export default {
  name: 'DoctorReport',
  components: {},
  data() {
    return {
      reportlist: [],
      currentPage: parseInt(localStorage.getItem('page_index')) ? parseInt(localStorage.getItem('page_index')) : 1,
      currentPageSize: parseInt(localStorage.getItem('page_size')) ? parseInt(localStorage.getItem('page_size')) : 10,
      loading: false,
      downloadLoading: false,
      total: undefined
    }
  },
  created() {
    this.getListreport(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 5, 1)
  },
  methods: {
    handleCurrentChange(val) {
      this.currentPage = val
      this.getListreport(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 5, 1)
    },
    handleSizeChange(val) {
      this.currentPageSize = val
      this.getListreport(val, (this.currentPage - 1) * this.currentPageSize, 5, 1)
    },
    goDetail(val) {
      localStorage.setItem('details_title', val.desc)
      localStorage.setItem('page_index', this.currentPage)
      localStorage.setItem('page_size', this.currentPageSize)
      this.$router.push({
        path: `/report/details?pid=${val.id}&did=${val.did}&type=${val.type}&report=doctor`
      })
    },
    // 判断当前病例的阴性阳性
    PNJudgement(cellstotal, posativetotal) {
      let positiveRate = 0
      let predictType = '未知'
      if (cellstotal > 0 && posativetotal > 0) {
        positiveRate = posativetotal * 100 / cellstotal
      }
      // console.log(positiveRate)
      if (positiveRate === 0) {
        predictType = '未知'
      } else if (positiveRate <= 5) {
        predictType = '阴性'
      } else if (positiveRate > 5) {
        predictType = '阳性'
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
          v.statusTime = v.status === '开始' ? `${v.status}(${v.ETA}s)` : v.status
          v.projectType = projectType[v.type]
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
              cells['type'] = cellsType[cells.type]
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
