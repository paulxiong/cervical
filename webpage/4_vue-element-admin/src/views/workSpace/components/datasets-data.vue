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
        icon="el-icon-search"
        @click="filterSearch"
      >搜索</el-button>
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
        label="项目 ID"
        align="center"
        prop="id"
      />
      <el-table-column
        label="描述"
        align="center"
        prop="desc"
      />
      <el-table-column
        label="创建者"
        align="center"
        prop="created_by"
      />
      <el-table-column
        label="裁剪模型"
        align="center"
        prop="parameter_mid"
      />
      <el-table-column
        label="状态"
        align="center"
        prop="status"
      />
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
      <newDatasets />
      <div slot="footer" class="dialog-footer">
        <el-button size="mini" @click="dialogFormVisible = false">上一步</el-button>
        <el-button size="mini" type="primary" @click="dialogFormVisible = false">下一步</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { listdatasets } from '@/api/cervical'
import { taskStatus, createdBy } from '@/const/const'
import { parseTime } from '@/utils/index'
import newDatasets from './newTrain'

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
    this.listdatasets(10, 0, 1)
  },
  methods: {
    stepNext() {
      this.step++
    },
    stepBack() {
      this.step = 1
    },
    filterSearch() {
      console.log(1)
    },
    createDatasets() {
      console.log(2)
    },
    handleCurrentChange(val) {
      console.log(3)
    },
    listdatasets(limit, skip, order) {
      listdatasets({ 'limit': limit, 'skip': skip, 'order': order }).then(res => {
        res.data.data.datasets.map(v => {
          v.created_at = parseTime(v.created_at)
          v.updated_at = parseTime(v.updated_at)
          v.processtime = parseTime(v.processtime)
          v.processend = parseTime(v.processend)
          v.created_by = createdBy[v.created_by] || '普通用户'
          v.status = taskStatus[v.status]
          v.parameter_cache = v.parameter_cache === 1 ? '使用' : '不使用'
          v.parameter_gray = v.parameter_gray === 1 ? '灰色' : '彩色'
        })
        this.datasetsList = res.data.data.datasets || []
        this.total = res.data.data.total
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
