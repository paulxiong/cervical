<template>
  <div class="reportData">
    <div class="filter-box">
      <el-input
        v-model="listQuery.desc"
        placeholder="请输入描述搜索"
        style="width:200px;"
        class="filter-input"
        @keyup.enter.native="filterSearch"
      />
      <el-select
        v-model="listQuery.type"
        placeholder="类型"
        clearable
        class="filter-type"
        style="width: 130px"
      >
        <el-option
          v-for="item in typeOptions"
          :key="item.key"
          :label="item.name"
          :value="item.key"
        />
      </el-select>
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
        icon="el-icon-edit"
        @click="dialogFormVisible = true"
      >新增报告</el-button>
    </div>
    <el-table
      v-loading="loading"
      element-loading-text="拼命加载中"
      :data="reportlist"
      style="width: 100%"
    >
      <el-table-column type="expand">
        <template slot-scope="props">
          <el-form label-position="left" inline class="table-expand">
            <el-form-item label="项目 ID">
              <span>{{ props.row.id }}</span>
            </el-form-item>
            <el-form-item label="描述">
              <span>{{ props.row.desc }}</span>
            </el-form-item>
            <el-form-item label="工作目录">
              <span>{{ props.row.dir }}</span>
            </el-form-item>
            <el-form-item label="创建者">
              <span>{{ props.row.created_by }}</span>
            </el-form-item>
            <el-form-item label="数据集 ID">
              <span>{{ props.row.did }}</span>
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
            <el-form-item label="创建时间">
              <span>{{ props.row.created_at }}</span>
            </el-form-item>
            <el-form-item label="更新时间">
              <span>{{ props.row.updated_at }}</span>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column width="60" label="ID" prop="id" />
      <el-table-column label="描述" prop="desc" />
      <el-table-column label="数据集 ID" prop="did" />
      <el-table-column label="创建者" prop="created_by" />
      <el-table-column label="类型" prop="projectType" />
      <el-table-column label="状态/剩余时间(秒)" prop="statusTime">
        <template slot-scope="scope">
          <el-tag :type="scope.row.statusType" effect="dark">{{ scope.row.statusTime }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="操作" width="100">
        <template slot-scope="scope">
          <el-button type="text" @click="goDetail(scope.row)">查看</el-button>
          <el-button type="text" style="color: #ff3c43;">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
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
    <el-dialog title="新增报告" :visible.sync="dialogFormVisible">
      <newReport ref="newReport" style="margin-top:-40px;" />
    </el-dialog>
  </div>
</template>

<script>
import { getListprojects } from '@/api/cervical'
import { taskStatus, createdBy, taskType, projectType } from '@/const/const'
import { parseTime } from '@/utils/index'

export default {
  name: 'ReportData',
  components: {},
  data() {
    return {
      reportlist: [],
      total: undefined,
      dialogFormVisible: false,
      currentPage: 1,
      currentPageSize: 10,
      loading: false,
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
    this.getListreport(10, 0, 101, 1)
  },
  methods: {
    handleClick(row) {
      console.log(row)
    },
    filterSearch() {
      this.getListreport(10, (this.currentPage - 1) * this.currentPageSize, 101, 1)
    },
    handleCurrentChange(val) {
      this.getListreport(this.currentPageSize, (this.currentPage - 1) * val, 101, 1)
    },
    handleSizeChange(val) {
      this.currentPageSize = val
      this.getListreport(val, (this.currentPage - 1) * val, 101, 1)
    },
    goDetail(val) {
      this.$router.push({
        path: '/report'
      })
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
        })
        this.reportlist = res.data.data.projects
        this.total = res.data.data.total
        this.loading = false
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.reportData {
  overflow: auto;
  height: 100%;
  padding-bottom: 30px;
  // margin-top: 30px;
  .filter-box {
    // position: fixed;
    // float: auto;
    // z-index: 10;
    // margin-top: -40px;
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
