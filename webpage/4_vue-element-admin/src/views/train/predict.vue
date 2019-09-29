<template>
  <div class="predict">
    <section class="header">
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
    <section class="model-select">
      <el-badge is-dot class="badge">模型选择</el-badge>
      <el-select class="model-option" @change="modelChange" v-model="model" clearable placeholder="请选择">
        <el-option
          v-for="item in options"
          :key="item.id"
          :label="item.desc"
          :value="item"
        ></el-option>
      </el-select>
    </section>
    <section class="datasets-select">
      <el-badge is-dot class="badge">数据集选择</el-badge>
      <div class="datasets">
        jjj
      </div>
    </section>
    <section class="model-info">
      <el-badge is-dot class="badge">模型信息</el-badge>
      <modelCard :trainInfo="trainInfo" :predict="predict"></modelCard>
    </section>
  </div>
</template>

<script>
import modelCard from './components/model-card'
import { getListmodel, getTrainresult } from '@/api/cervical'

export default {
  name: 'Predict',
  components: { modelCard },
  data() {
    return {
      percentage: 100,
      predict: 'predict',
      options: [],
      model: '',
      trainInfo: {}
    }
  },
  methods: {
    modelChange() {
      this.getTrainresult()
    },
    getListmodel() {
      getListmodel().then(res => {
        this.options = res.data.data.models
        this.model = this.options[0]
        this.getTrainresult()
      })
    },
    getTrainresult() {
      getTrainresult({ 'id': this.model.did }).then(res => {
        this.trainInfo = res.data.data
      })
    }
  },
  mounted() {
    this.getListmodel()
  }
}
</script>

<style lang="scss" scoped>
.predict {
  padding: 0 30px;
  .badge {
    font-weight: bold;
    margin-bottom: 5px;
  }
  .model-option {
    display: block;
  }
  .model-select, .datasets-select, .progress-info {
    margin: 20px 0;
  }
}
</style>
