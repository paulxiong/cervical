<template>
  <div class="projectData">
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
      <el-button class="filter-btn" type="primary" icon="el-icon-search" @click="filterSearch">刷新</el-button>
      <el-button
        class="filter-btn"
        style="margin-left: 10px;"
        type="success"
        icon="el-icon-edit"
        @click="dialogFormVisible = true"
      >新增项目</el-button>
    </div>
    <el-table :data="projectlist" style="width: 100%">
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
      <el-table-column label="项目 ID" align="center" prop="id" />
      <el-table-column label="描述" align="center" prop="desc" />
      <el-table-column label="数据集 ID" align="center" prop="did" />
      <el-table-column label="创建者" align="center" prop="created_by" />
      <el-table-column label="剩余时间(秒)" align="center" prop="ETA" />
      <el-table-column
        label="状态"
        align="center"
        prop="status"
      >
        <template slot-scope="scope">
          <el-tag
            :type="scope.row.statusType"
            effect="dark"
          >
            {{ scope.row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column
        fixed="right"
        label="操作"
        width="100"
      >
        <template slot-scope="scope">
          <el-button type="text" @click="goDetail(scope.row)">查看</el-button>
          <el-button type="text" style="color: #ff3c43;">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="page-box flex">
      <el-pagination
        class="page"
        :current-page.sync="currentPage"
        :page-size="10"
        layout="prev, pager, next, jumper"
        :total="total"
        @current-change="handleCurrentChange"
      />
    </div>
    <el-dialog title="新建项目" :visible.sync="dialogFormVisible">
      <newProject ref="newProject" />
      <div slot="footer" class="dialog-footer">
        <el-button size="mini" @click="stepBack">上一步</el-button>
        <el-button size="mini" type="primary" @click="stepNext">下一步</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getListprojects } from '@/api/cervical'
import { taskStatus, createdBy, taskType } from '@/const/const'
import { parseTime } from '@/utils/index'
import newProject from './newProject'

export default {
  name: 'ProjectData',
  components: { newProject },
  data() {
    return {
      projectlist: undefined,
      total: undefined,
      dialogFormVisible: false,
      currentPage: 1,
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
    this.getListprojects(10, 0, 1)
  },
  methods: {
    stepNext() {
      this.$refs.newProject.stepNext()
    },
    stepBack() {
      this.$refs.newProject.stepBack()
    },
    filterSearch() {
      this.getListprojects(10, (this.currentPage - 1) * 10, 1)
    },
    handleCurrentChange(val) {
      this.getListprojects(10, (val - 1) * 10, 1)
    },
    getListprojects(limit, skip, order) {
      getListprojects({ 'limit': limit, 'skip': skip, 'order': order }).then(res => {
        res.data.data.projects.map(v => {
          v.created_at = parseTime(v.created_at)
          v.updated_at = parseTime(v.updated_at)
          v.processtime = parseTime(v.processtime)
          v.processend = parseTime(v.processend)
          v.created_by = createdBy[v.created_by] || '普通用户'
          v.statusType = taskType[v.status]
          v.status = taskStatus[v.status]
        })
        this.projectlist = res.data.data.projects
        this.total = res.data.data.total
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.projectData {
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
