<template>
  <div class="train">
    <section class="header">
      <div class="title flex">
        <h2>TRAIN</h2>
        <el-button type="danger" @click="handleTrain" :disabled="checkboxCell.length<2">开始训练</el-button>
      </div>
      <div class="cellTypes">
        <el-badge is-dot class="badge">请选择细胞类型</el-badge>
        <el-checkbox-group v-model="checkboxCell" size="mini">
          <el-checkbox v-for="(v, i) in cellTypes" :key="i" :label="v" :checked="i<=1" border></el-checkbox>
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
import { createTrain } from '@/api/cervical'

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
    handleTrain() {
      console.log(this.checkboxCell)
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
