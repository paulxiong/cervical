<template>
  <div class="projectData">
    <div class="filter-box">
      <el-button
        class="filter-btn"
        type="primary"
        :icon="loading?'el-icon-loading':'el-icon-refresh-left'"
        @click="filterSearch"
      >{{ $t('workspace.projectsRefresh') }}</el-button>
      <el-button
        class="filter-btn"
        style="margin-left: 10px;"
        type="success"
        icon="el-icon-edit"
        @click="dialogFormVisible = true"
      >{{ $t('workspace.projectsNew') }}</el-button>
    </div>
    <el-table
      v-loading="loading"
      :element-loading-text="$t('workspace.loading')"
      :data="projectlist"
      style="width: 100%"
    >
      <el-table-column type="expand">
        <template slot-scope="props">
          <el-form label-position="left" inline class="table-expand">
            <el-form-item :label="$t('workspace.projectDir')">
              <span>{{ props.row.dir }}</span>
            </el-form-item>
            <el-form-item :label="$t('workspace.projectOwner')">
              <span>{{ props.row.username }}</span>
            </el-form-item>
            <el-form-item :label="$t('workspace.projectModelID')">
              <span>{{ props.row.parameter_mid }}</span>
            </el-form-item>
            <el-form-item :label="$t('workspace.projectModelType')">
              <span>{{ props.row.parameter_mtype }}</span>
            </el-form-item>
            <el-form-item :label="$t('workspace.projectSize')">
              <span>{{ props.row.parameter_resize }}</span>
            </el-form-item>
            <el-form-item :label="$t('workspace.projectTime')">
              <span>{{ props.row.parameter_time }}</span>
            </el-form-item>
            <el-form-item :label="$t('workspace.projectType')">
              <span>{{ props.row.parameter_type === 0 ? $t('workspace.projectTypeNoLabel') : $t('workspace.projectTypeLabel') }}</span>
            </el-form-item>
            <el-form-item :label="$t('workspace.projectPercent')">
              <span>{{ props.row.percent }}</span>
            </el-form-item>
            <el-form-item :label="$t('workspace.projectETA')">
              <span>{{ props.row.ETA }}</span>
            </el-form-item>
            <el-form-item :label="$t('workspace.projectStatus')">
              <span>{{ props.row.status }}</span>
            </el-form-item>
            <el-form-item :label="$t('workspace.projectStartTime')">
              <span>{{ props.row.starttime }}</span>
            </el-form-item>
            <el-form-item :label="$t('workspace.projectEndTime')">
              <span>{{ props.row.endtime }}</span>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column width="100" :label="$t('workspace.projectID')" prop="id" />
      <el-table-column width="350" :label="$t('workspace.projectDesc')" prop="desc" />
      <el-table-column width="150" :label="$t('workspace.projectDID')" prop="did" />
      <el-table-column :label="$t('workspace.projectCreator')">
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
      <el-table-column :label="$t('workspace.projectType2')" prop="projectType" />
      <el-table-column :label="$t('workspace.projectCreatTime')" prop="created_at" />
      <el-table-column :label="$t('workspace.projectStatus2')" prop="statusTime">
        <template slot-scope="scope">
          <el-tag :type="scope.row.statusType" effect="light">{{ $t(scope.row.statusTime) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column fixed="right" :label="$t('workspace.projectOP')" width="100">
        <template slot-scope="scope">
          <el-button type="primary" size="mini" @click="goDetail(scope.row)">{{ $t('workspace.projectOPLook') }}</el-button>
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
    <el-dialog :title="$t('workspace.projectNew')" :visible.sync="dialogFormVisible">
      <newProject ref="newProject" style="margin-top:-40px;" />
    </el-dialog>
  </div>
</template>

<script>
import { getListprojects } from '@/api/cervical'
import { taskStatus, createdBy, taskType, projectType } from '@/const/const'
import { parseTime } from '@/utils/index'
import newProject from './newProject'

export default {
  name: 'ProjectData',
  components: { newProject },
  props: {
    activename: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      projectlist: [],
      total: undefined,
      dialogFormVisible: false,
      // step: 1,
      currentPage: 1,
      currentPageSize: 10,
      loading: false,
      listQuery: {
        desc: undefined,
        type: undefined
      }
    }
  },
  created() {
    this.getListprojects(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
  },
  methods: {
    handleClick(row) {
    },
    filterSearch() {
      this.getListprojects(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.getListprojects(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
    },
    handleSizeChange(val) {
      this.currentPageSize = val
      this.getListprojects(val, (this.currentPage - 1) * this.currentPageSize, 1)
    },
    goDetail(val) {
      this.$router.push({
        path: `/workSpace/details?pid=${val.id}&did=${val.did}&type=${val.type}`
      })
    },
    getListprojects(limit, skip, order) {
      this.loading = true
      getListprojects({ 'limit': limit, 'skip': skip, 'order': order }).then(res => {
        res.data.data.projects.map(v => {
          v.created_at = parseTime(v.created_at)
          v.updated_at = parseTime(v.updated_at)
          v.starttime = parseTime(v.starttime)
          v.endtime = parseTime(v.endtime)
          v.created_by = createdBy[v.created_by] || '普通用户'
          v.statusType = taskType[v.status]
          v.statusTime = v.status === '开始' ? `${v.status}(${v.ETA}s)` : taskStatus[v.status]
          v.projectType = this.$t(projectType[v.type])
        })
        this.projectlist = res.data.data.projects
        this.total = res.data.data.total
        this.loading = false
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
