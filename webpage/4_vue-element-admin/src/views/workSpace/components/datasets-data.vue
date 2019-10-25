<template>
  <div class="datasetsData">
    <el-table
      :data="datasetslist"
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
        label="状态"
        prop="status"
      />
    </el-table>
  </div>
</template>

<script>
export default {
  name: 'DatasetsData',
  components: {},
  props: {
    datasetslist: {
      type: Array,
      default() {
        return []
      }
    }
  },
  data() {
    return {
      value: 'datasetsData'
    }
  },
  methods: {}
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
    width: 50%;
  }
}
</style>
