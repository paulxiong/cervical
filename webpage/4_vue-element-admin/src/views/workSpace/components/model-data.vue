<template>
  <div class="modelData">
    <el-table
      :data="modellist"
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
    </el-table>
  </div>
</template>

<script>
export default {
  name: 'ModelData',
  components: {},
  props: {
    modellist: {
      type: Array,
      default() {
        return []
      }
    }
  },
  data() {
    return {
      value: 'modelData'
    }
  },
  methods: {}
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
