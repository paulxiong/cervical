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
          v-for="(item, idx) in options"
          :key="item.id"
          :label="item.desc"
          :value="idx"
        ></el-option>
      </el-select>
    </section>
    <section class="datasets-select">
      <el-badge is-dot class="badge">数据选择</el-badge>
      <el-select class="model-option" @change="datasetsChange" v-model="datasets" clearable placeholder="请选择">
        <el-option
          v-for="(item, idx) in dataList"
          :key="item.id"
          :label="item.desc"
          :value="idx"
        ></el-option>
      </el-select>
    </section>
    <section class="model-info">
      <el-badge is-dot class="badge">模型信息</el-badge>
      <modelCard :trainInfo="trainInfo" :predict="predict"></modelCard>
    </section>
    <section class="datasets-info">
      <el-badge is-dot class="badge">数据信息</el-badge>
      <datasetsCard :datasets="datasetsInfo"></datasetsCard>
    </section>
  </div>
</template>

<script>
import modelCard from './components/model-card'
import datasetsCard from './components/datasets-card'
import { listdatasets, getListmodel, getTrainresult } from '@/api/cervical'

export default {
  name: 'Predict',
  components: { modelCard, datasetsCard },
  data() {
    return {
      percentage: 100,
      predict: 'predict',
      options: [],
      model: 0,
      datasets: 0,
      trainInfo: {},
      datasetsInfo: {},
      dataList: []
    }
  },
  methods: {
    modelChange() {
      this.modelInfo = this.options[this.model]
      this.getTrainresult()
    },
    datasetsChange() {
      this.datasetsInfo = this.dataList[this.datasets]
    },
    getListmodel() {
      getListmodel().then(res => {
        this.options = res.data.data.models
        this.modelInfo = this.options[0]
        this.getTrainresult()
      })
    },
    getTrainresult() {
      getTrainresult({ 'id': this.modelInfo.did }).then(res => {
        this.trainInfo = res.data.data
      })
    },
    getListdatasets(limit, skip, type) {
      listdatasets({ 'limit': limit, 'skip': skip, 'type': type }).then(res => {
        this.dataList = res.data.data.datasets
        this.datasetsInfo = this.dataList[0]
      })
    }
  },
  mounted() {
    this.getListmodel()
    this.getListdatasets(100, 0, 2)
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
  .model-select, .datasets-select, .progress-info, .model-info, .datasets-info {
    margin: 20px 0;
  }
}
</style>
