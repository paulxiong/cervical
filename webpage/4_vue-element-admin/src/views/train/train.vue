<template>
  <div class="train">
    <section class="header">
      <div class="title">
        <h2>TRAIN</h2>
      </div>
      <div class="cellTypes">
        <el-badge is-dot class="badge">请选择细胞类型</el-badge>
        <el-checkbox-group v-model="checkboxCell" @change="checkCellTypes" size="mini">
          <el-checkbox
            v-for="v in cellTypes"
            :key="v.celltype"
            checked
            :label="v"
            border
          ></el-checkbox>
        </el-checkbox-group>
      </div>
      <div class="progress-info">
        <el-badge is-dot class="badge">状态进度</el-badge>
        <el-progress
          :text-inside="true"
          :stroke-width="26"
          :percentage="percentage"
          status="success"
        ></el-progress>
      </div>
    </section>
    <modelCard></modelCard>
  </div>
</template>

<script>
import modelCard from './components/model-card'

export default {
  name: 'train',
  components: { modelCard },
  data() {
    return {
      percentage: 100,
      cellTypes: JSON.parse(localStorage.getItem('cellTypes')) || [],
      checkboxCell: []
    }
  },
  methods: {
    checkCellTypes(val) {
      console.log(val)
    }
  }
}
</script>

<style lang="scss" scoped>
.train {
  padding: 0 30px;
  .header {
    .title {
      justify-content: flex-start;
      h2 {
        margin-right: 10px;
      }
    }
    .badge {
        font-weight: bold;
        margin-bottom: 5px;
      }
    .cellTypes {
      margin-bottom: 20px;
    }
  }
}
</style>
