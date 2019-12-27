<template>
  <div class="projectData">
    <el-table
      v-loading="loading"
      element-loading-text="拼命加载中"
      :data="projectlist"
      style="width: 100%"
      @expand-change="expandChange"
    >
      <el-table-column type="expand">
        <template slot-scope="scope">
          <div class="temp-box flex">
            <el-table
              ref="multipleTable"
              :data="scope.row.predictsList"
              tooltip-effect="dark"
              style="width: 50%"
              @selection-change="handleSelectionChange"
            >
              <el-table-column type="selection" width="55" />
              <el-table-column label="ID" prop="id" width="120" />
              <el-table-column label="预测结果" prop="predict_str" width="200" />
              <el-table-column label="初审核结果" prop="true_str" width="200" show-overflow-tooltip />
            </el-table>
            <div class="select-box" style="width:50%;">
              <h3>分配给</h3>
              <el-select v-model="vid" placeholder="请选择">
                <el-option
                  v-for="item in userList"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                >
                  <img :src="item.image" style="float: left;width:25px;height:25px;">
                  <span style="float: right; color: #8492a6; font-size: 13px">{{ item.name }}</span>
                </el-option>
              </el-select>
              <el-button type="primary" @click="setPredictsReview">确定</el-button>
            </div>
          </div>

          <el-pagination
            class="page"
            :current-page.sync="scope.row.currentPage"
            :page-sizes="[10, 20, 30, 50]"
            :page-size="scope.row.currentPageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="scope.row.total"
            @current-change="handleCurrentChange2"
            @size-change="handleSizeChange2"
          />
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
import { getPredictsByPID, getListprojects, setPredictsReview } from '@/api/cervical'
import { getUserLists } from '@/api/user'
import { taskStatus, createdBy, taskType, projectType, cellsType } from '@/const/const'
import { parseTime } from '@/utils/index'

export default {
  name: 'ProjectData',
  components: {},
  data() {
    return {
      projectlist: [],
      predicts: [],
      userList: [],
      selectedList: [],
      pid: 121,
      vid: undefined,
      total: undefined,
      currentPage: 1,
      currentPageSize: 10,
      total2: undefined,
      currentPage2: 1,
      currentPageSize2: 10,
      loading: false
    }
  },
  created() {
    this.getUserLists(100, 0, 1)
    this.getListprojects(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
    this.getPredictsByPID(this.currentPageSize2, (this.currentPage2 - 1) * this.currentPageSize2, this.pid)
  },
  methods: {
    handleCurrentChange(val) {
      this.currentPage = val
      this.getListprojects(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
    },
    handleSizeChange(val) {
      this.currentPageSize = val
      this.getListprojects(val, (this.currentPage - 1) * this.currentPageSize, 1)
    },
    handleCurrentChange2(val) {
      console.log(val, 'curpage')
      this.currentPage2 = val
      this.getPredictsByPID(this.currentPageSize2, (this.currentPage2 - 1) * this.currentPageSize2, this.pid)
    },
    handleSizeChange2(val) {
      console.log(val, 'cursize')
      this.currentPageSize2 = val
      this.getPredictsByPID(this.currentPageSize2, (this.currentPage2 - 1) * this.currentPageSize2, this.pid)
    },
    handleSelectionChange(val) {
      this.selectedList = []
      val.map(v => {
        this.selectedList.push(v.id)
      })
    },
    expandChange(val, event) {
      if (event.length) {
        this.pid = val.id
        this.getPredictsByPID(this.currentPageSize2, (this.currentPage2 - 1) * this.currentPageSize2, val.id)
      }
    },
    getPredictsByPID(limit, skip, pid) {
      getPredictsByPID({ 'limit': limit, 'skip': skip, 'pid': pid, 'status': 1 }).then(res => {
        this.projectlist.map(v => {
          if (v.id === this.pid) {
            res.data.data.predicts.map(item => {
              item.predict_str = cellsType[item.predict_type]
              item.true_str = cellsType[item.true_type]
            })
            v.predictsList = res.data.data.predicts
            v.currentPage = 1
            v.currentPageSize = 10
            const _this = this
            v.handleCurrentChange = function(val) {
              console.log(val, _this.pid)
              v.predictsList = []
              _this.$forceUpdate()

              getPredictsByPID({ 'limit': 10, 'skip': (val - 1) * 10, 'pid': _this.pid, 'status': 1 }).then(res => {
                res.data.data.predicts.map(item => {
                  item.predict_str = cellsType[item.predict_type]
                  item.true_str = cellsType[item.true_type]
                })
                v.predictsList = res.data.data.predicts
                console.log(v.predictsList)
                _this.$forceUpdate()
              })
            }
            v.total = res.data.data.total
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
    },
    setPredictsReview() {
      this.loading = true
      const postData = {
        'pid': this.pid,
        'predicts': this.selectedList,
        'vid': this.vid
      }
      setPredictsReview(postData).then(res => {
        this.loading = false
        this.getPredictsByPID(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, this.pid)
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
