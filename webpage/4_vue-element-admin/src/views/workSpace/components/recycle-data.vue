<template>
  <div class="recycleData">
    <!-- <div class="filter-box">
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
    </div> -->
    <el-table
      :data="recycleList"
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
            <el-form-item label="模型 ID">
              <span>{{ props.row.model_id }}</span>
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
      <el-table-column
        fixed="right"
        label="操作"
      >
        <template slot-scope="scope">
          <el-button type="text" @click="goDetail(scope.row)">恢复</el-button>
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
      />
    </div>
  </div>
</template>

<script>
export default {
  name: 'RecycleData',
  components: {},
  data() {
    return {
      step: 1,
      currentPage: 1,
      total: 12,
      recycleList: [
        {
          'id': '1',
          'desc': '第一个项目',
          'created_by': '用户六',
          'score': '98.6',
          'status': '已完成',
          'created_at': '2019-10-25 17:53:13',
          'model_id': '2',
          'datasets_id': '3'
        },
        {
          'id': '2',
          'desc': '第二个项目',
          'created_by': '用户一',
          'status': '已完成',
          'score': '98.6',
          'created_at': '2019-10-25 17:00:13',
          'model_id': '1',
          'datasets_id': '1'
        },
        {
          'id': '3',
          'desc': '第三个项目',
          'created_by': '管理员',
          'status': '已完成',
          'score': '94.0',
          'created_at': '2019-10-25 11:03:13',
          'model_id': '2',
          'datasets_id': '2'
        },
        {
          'id': '4',
          'desc': '第四个项目',
          'created_by': '用户二',
          'status': '未完成',
          'score': '0',
          'created_at': '2019-10-25 06:00:00',
          'model_id': '7',
          'datasets_id': '2'
        },
        {
          'id': '5',
          'desc': '第五个项目',
          'created_by': '用户三',
          'status': '已完成',
          'score': '99.0',
          'created_at': '2019-10-25 11:00:13',
          'model_id': '1',
          'datasets_id': '1'
        },
        {
          'id': '6',
          'desc': '第六个项目',
          'created_by': '用户四',
          'status': '未完成',
          'score': '0',
          'created_at': '2019-10-25 12:00:13',
          'model_id': '3',
          'datasets_id': '4'
        },
        {
          'id': '7',
          'desc': '第七个项目',
          'created_by': '用户五',
          'status': '已完成',
          'score': '98.1',
          'created_at': '2019-10-25 14:53:13',
          'model_id': '2',
          'datasets_id': '3'
        }
      ],
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
  methods: {
    filterSearch() {
      console.log(1)
    },
    handleCurrentChange(val) {
      console.log(val)
    }
  }
}
</script>

<style lang="scss" scoped>
.recycleData {
  overflow: auto;
  height: 100%;
  padding-bottom: 30px;
  .filter-box {
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
    width: 50%;
  }
}
</style>
