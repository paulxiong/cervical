<template>
  <div class="modelData">
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
        @click="createModel"
      >新增模型</el-button>
    </div>
    <el-table
      :data="modelList"
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
            <el-form-item label="类型">
              <span>{{ props.row.type }}</span>
            </el-form-item>
            <el-form-item label="数据集 ID">
              <span>{{ props.row.datasets_id }}</span>
            </el-form-item>
            <el-form-item label="状态">
              <span>{{ props.row.status }}</span>
            </el-form-item>
            <el-form-item label="得分">
              <span>{{ props.row.score }}</span>
            </el-form-item>
            <el-form-item label="创建时间">
              <span>{{ props.row.created_at }}</span>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column
        label="项目 ID"
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
        label="得分"
        prop="score"
      />
      <el-table-column
        label="状态"
        prop="status"
      />
    </el-table>
    <div class="page-box flex">
      <el-pagination
        class="page"
        :current-page.sync="currentPage"
        :page-sizes="[10, 20, 30, 50]"
        :page-size="10"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script>
import { getListmodel } from '@/api/cervical'
export default {
  name: 'ModelData',
  components: {},
  data() {
    return {
      step: 1,
      currentPage: 1,
      total: undefined,
      modelList: [],
      dialogFormVisible: false,
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
    this.getListmodel(10, 0, 4)
  },
  methods: {
    filterSearch() {
      console.log(1)
    },
    createModel() {
      console.log(2)
    },
    handleCurrentChange(val) {
      console.log(val)
    },
    getListmodel(limit, skip, type) {
      // 裁剪是4,预测是5
      getListmodel({ 'limit': limit, 'skip': skip, 'type': type }).then(res => {
        this.modellist = res.data.data.models
        this.total = res.data.data.total
        console.log(this.modellist, '123')
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.modelData {
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
    width: 50%;
  }
}
</style>
