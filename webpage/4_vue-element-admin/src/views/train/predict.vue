<template>
  <div class="predict">
    <section class="header flex">
      <el-badge is-dot class="badge">预测进度</el-badge>
      <el-progress
        :text-inside="true"
        :stroke-width="26"
        :percentage="percentage"
        class="progress"
        status="success"
      ></el-progress>
      <el-button type="danger" class="predict-btn" @click="createPredict">开始预测</el-button>
    </section>
    <section class="content">
      <section class="model-info" v-if="modelList.length">
        <el-badge is-dot class="badge">模型信息</el-badge>
        <modelCard :modelInfo="modelInfo" :predict="predict" :modelList="modelList" />
      </section>
      <section class="datasets-info" v-if="datasetsList.length">
        <el-badge is-dot class="badge">数据信息</el-badge>
        <datasetsCard :datasetsInfo="datasetsInfo" :predict="predict" :datasetsList="datasetsList" />
      </section>
    </section>
  </div>
</template>

<script>
import modelCard from './components/model-card'
import datasetsCard from './components/datasets-card'
import { listdatasets, getListmodel, getTrainresult, createPredict } from '@/api/cervical'

export default {
  name: 'Predict',
  components: { modelCard, datasetsCard },
  data() {
    return {
      percentage: 50,
      predict: 'predict',
      modelList: [],
      modelInfo: {},
      datasetsInfo: {},
      datasetsList: []
    }
  },
  methods: {  
    getListmodel(limit, skip) {
      getListmodel({ 'limit': limit, 'skip': skip }).then(res => {
        if (res.data.data.total > 0) {
          this.modelList = res.data.data.models
          this.modelInfo = this.modelList[0]
        }
      })
    },
    getListdatasets(limit, skip, type) {
      listdatasets({ 'limit': limit, 'skip': skip, 'type': type }).then(res => {
        this.datasetsList = res.data.data.datasets
        this.datasetsInfo = this.datasetsList[0]
      })
    },
    createPredict() {
      createPredict({ 'did': this.datasetsInfo.id, 'mid': this.modelInfo.id }).then(res => {
        this.$message({
          message: res.data.data,
          type: 'success'
        })
      })
    }
  },
  mounted() {
    this.getListmodel(10, 0)
    this.getListdatasets(100, 0, 2)
  }
}
</script>

<style lang="scss" scoped>
.predict {
  margin-bottom: 100px;
  .badge {
    font-weight: bold;
  }
  .content {
    padding: 0 30px;
    .badge {
      margin-bottom: 5px;
    }
  }
  .header {
    border: 1px solid #ccc;
    background: #304155;
    min-width: 100%;
    justify-content: flex-end;
    position: fixed;
    bottom: -1px;
    right: -1px;
    padding: 10px 0;
    z-index: 999;
    .badge {
      color: #fff;
    }
    .progress {
      width: 70%;
      margin: 0 10px;
    }
    .predict-btn {
      width: 100px;
      margin-right: 30px;
    }
  }
  .model-option {
    display: block;
  }
  .model-select,
  .datasets-select,
  .progress-info,
  .model-info,
  .datasets-info {
    margin: 20px 0;
  }
}
</style>
