<template>
  <div class="datasetsData">
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
      >新增数据集</el-button>
    </div>
    <el-table
      :data="datasetsList"
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
            <el-form-item label="创建者">
              <span>{{ props.row.created_by }}</span>
            </el-form-item>
            <el-form-item label="目录">
              <span>{{ props.row.dir }}</span>
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
            <el-form-item label="创建时间">
              <span>{{ props.row.created_at }}</span>
            </el-form-item>
            <el-form-item label="更新时间">
              <span>{{ props.row.updated_at }}</span>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column
        label="ID"
        width="60"
        prop="id"
      />
      <el-table-column
        label="描述"
        prop="desc"
      />
      <el-table-column
        label="创建者"
        prop="created_by"
      />
      <el-table-column
        label="裁剪模型"
        prop="parameter_mid"
      />
      <el-table-column
        label="状态/剩余时间(秒)"
        prop="statusTime"
      >
        <template slot-scope="scope">
          <el-tag
            :type="scope.row.statusType"
            effect="dark"
          >
            {{ scope.row.statusTime }}
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
    <el-dialog title="新建数据集" :visible.sync="dialogFormVisible">
      <newDatasets ref="newDatasets" />
      <div slot="footer" class="dialog-footer">
        <el-button v-show="step===3 || step===2" size="mini" @click="stepBack">上一步</el-button>
        <el-button v-show="step===1 || step===2" size="mini" type="primary" @click="stepNext">下一步</el-button>
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
  data() {
    return {
      datasetsList: [],
      step: 1,
      total: undefined,
      dialogFormVisible: false,
      currentPage: 1,
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
    this.listdatasets(10, 0, 1)
  },
  methods: {
    stepNext() {
      this.$refs.newDatasets.stepNext()
      this.step = this.$refs.newDatasets.step
    },
    stepBack() {
      this.$refs.newDatasets.stepBack()
      this.step = this.$refs.newDatasets.step
    },
    filterSearch() {
      this.listdatasets(10, (this.currentPage - 1) * 10, 1)
    },
    handleCurrentChange(val) {
      this.listdatasets(10, (val - 1) * 10, 1)
    },
    goDetail(val) {
      this.$router.push({
        path: `/train/detailsTrain?id=${val.id}`
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
            v.status = taskStatus[v.status]
            v.statusTime = v.status === '开始' ? `${v.status}(${v.ETA}s)` : v.status
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
    width: calc(100%/4);
  }
}
</style>
