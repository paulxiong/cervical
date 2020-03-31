<template>
  <div class="doctorreport">
    <keep-alive>
      <router-view v-if="$route.meta.keepAlive" />
    </keep-alive>
    <router-view v-if="!$route.meta.keepAlive" />
    <el-table
      v-loading="loading"
      element-loading-text="拼命加载中"
      :data="projectlist"
      style="width: 100%"
    >
      <!-- <el-table-column type="expand">
        <template slot-scope="scope">
          <expand-two :pid="scope.row.id" :predicts="scope.row.predictsList" :page="scope.row.currentPage" :pagesize="scope.row.currentPageSize" :total="scope.row.total" />
        </template>
      </el-table-column> -->
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
          <el-button
            style="float: right; padding: 3px 0"
            type="primary"
            @click="goFovmap(scope.row)"
          >查看详情</el-button>
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
import { getListprojects } from '@/api/cervical'
import { taskStatus, createdBy, taskType, projectType } from '@/const/const'
import { parseTime } from '@/utils/index'

export default {
  components: { },
  data() {
    return {
      mapargs: {
        bid: 'b20200327',
        mid: 'b20200327095341',
        ext: '.jpg',
        ImageWidth: 2448,
        ImageHeight: 2048,
        sceneWidth: 72348,
        sceneHeight: 72104
      },
      total: undefined,
      currentPage: 1,
      currentPageSize: 10,
      loading: false,
      projectlist: []
    }
  },
  created() {
    this.getListprojects(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
  },
  methods: {
    goFovmap(v) {
      this.$router.push({
        path: `/index3map?pid=${v.id}&did=${v.did}`
      })
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.getListprojects(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
    },
    handleSizeChange(val) {
      this.currentPageSize = val
      this.getListprojects(val, (this.currentPage - 1) * this.currentPageSize, 1)
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
    }
  }
}
</script>

<style>
.doctorReport {
  overflow: auto;
  height: 100%;
  padding-bottom: 30px;
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
</style>
