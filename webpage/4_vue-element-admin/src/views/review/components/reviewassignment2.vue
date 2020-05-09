<template>
  <div class="reviewAssignment2">
    <el-table
      v-loading="loading"
      element-loading-text="拼命加载中"
      :data="projectlist"
      style="width: 100%"
      :row-key="getRowKeys"
      :expand-row-keys="expands"
      @row-click="clickRowHandle"
      @expand-change="expandChange"
    >
      <el-table-column type="expand">
        <template slot-scope="scope">
          <expand-two :pid="scope.row.id" :predicts="scope.row.predictsList" :page="scope.row.currentPage" :pagesize="scope.row.currentPageSize" :total="scope.row.total" />
        </template>
      </el-table-column>
      <el-table-column width="60" label="ID" prop="id" />
      <el-table-column label="描述" prop="desc" />
      <el-table-column label="数据集 ID" prop="did" />
      <el-table-column label="创建者">
        <template slot-scope="scope">
          <el-tooltip v-if="scope.row.username" :content="scope.row.username" placement="right">
            <el-image
              style="width:36px;height:36px;border-radius:7px;"
              :src="scope.row.userimg"
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
import { APIUrl } from '@/const/config'
import { getPredictsByPID2, getListprojects } from '@/api/cervical'
import { getUserLists } from '@/api/user'
import { taskStatus, createdBy, taskType, projectType, cellsType } from '@/const/const'
import { parseTime } from '@/utils/index'
import expandTwo from './expandTwo'

export default {
  name: 'ReviewAssignment2',
  components: { expandTwo },
  data() {
    return {
      hosturlpath64: APIUrl + '/imgs/',
      projectlist: [],
      predicts: [],
      userList: [],
      selectedList: [],
      pid: 121,
      vid: 0,
      total: undefined,
      currentPage: 1,
      currentPageSize: 10,
      loading: false,
      // 获取row的key值
      getRowKeys(row) {
        return row.id
      },
      // 要展开的行，数值的元素是row的key值
      expands: []
    }
  },
  created() {
    this.getUserLists(100, 0, 1)
    this.getListprojects(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
  },
  methods: {
    clickRowHandle(row, column, event) {
      if (this.expands.includes(row.id)) {
        this.expands = this.expands.filter(val => val !== row.id)
      } else {
        this.expands.push(row.id)
      }
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.getListprojects(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
    },
    handleSizeChange(val) {
      this.currentPageSize = val
      this.getListprojects(val, (this.currentPage - 1) * this.currentPageSize, 1)
    },
    handleSelectionChange(event) {
      // console.log(event, this.$refs.multipleTable)
      this.selectedList = []
      // val.map(v => {
      //   this.selectedList.push(v.id)
      // })
    },
    expandChange(val, event) {
      if (event.length) {
        this.pid = val.id
        this.projectlist.map(v => {
          if (v.id === val.id) {
            this.getPredictsByPID2(v.currentPageSize, (v.currentPage - 1) * v.currentPageSize, v.id)
          }
        })
      }
    },
    getPredictsByPID2(limit, skip, pid) {
      getPredictsByPID2({ 'limit': limit, 'skip': skip, 'pid': pid, 'status': 0, 'type': 50, 'order': 0 }).then(res => {
        this.projectlist.map(v => {
          if (v.id === pid) {
            v.pid = pid
            v.predictsList = []
            v.currentPagetmp = v.currentPage
            v.currentPage = 1
            v.total = 0
          }
        })
        if (!res.data.data) {
          return
        }
        this.projectlist.map(v => {
          if (v.id === pid) {
            res.data.data.predicts.map(item => {
              item.predict_str = cellsType[item.predict_type]
              item.true_str = cellsType[item.true_type]
            })
            v.pid = pid
            v.predictsList = res.data.data.predicts
            v.total = res.data.data.total
            v.currentPage = v.currentPagetmp
          }
        })
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
          v.projectType = projectType[v.type]
          v.currentPage = 0
          v.currentPageSize = 10
          v.selectedList = []
        })
        this.projectlist = res.data.data.projects
        this.pid = res.data.data.projects[0].id
        this.total = res.data.data.total
        this.loading = false
      })
    },
    getUserLists(limit, skip, order) {
      getUserLists({ 'limit': limit, 'skip': skip, 'order': order }).then(res => {
        this.userList = res.data.data.users
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
    width: calc(100% / 4);
  }
}
</style>
