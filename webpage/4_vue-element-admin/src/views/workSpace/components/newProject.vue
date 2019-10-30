<template>
  <div class="newProject">
    <section class="step">
      <el-steps :active="step">
        <el-step title="选择数据集/模型" icon="el-icon-set-up" />
        <el-step title="确认信息" icon="el-icon-cpu" />
      </el-steps>
    </section>

    <section class="main">
      <div v-if="step===1" class="data-model">
        <datasetsCard
          :datasets-info="datasetsInfo"
          :datasets-list="datasetsList"
          @datasetsChange="datasetsChange"
        />
        <modelCard
          :model-info="modelInfo"
          :model-list="modelList"
          @modelChange="modelChange"
        />
      </div>
      <div v-if="step===2" class="start-train">
        <h2 class="title flex">
          <el-input
            v-model="inputName"
            autofocus
            placeholder="输入描述"
            show-word-limit
            maxlength="30"
            class="input-name"
            @keyup.enter.native="goDetail"
          />
          <el-button
            class="start-btn"
            type="danger"
            :disabled="!inputName.length"
            @click="goDetail"
          >开始处理</el-button>
        </h2>
        <div class="info flex">
          <section class="param">
            <h4>裁剪大小(像素)</h4>
            <el-radio-group v-model="cutInput">
              <el-radio-button label="100" />
              <el-radio-button label="120" />
              <el-radio-button label="150" />
            </el-radio-group>
          </section>
          <section class="param">
            <h4>最长用时</h4>
            <el-radio-group v-model="useTime">
              <el-radio-button label="1800" />
              <el-radio-button label="2400" />
              <el-radio-button label="3000" />
            </el-radio-group>
          </section>
          <section class="param">
            <h4>预测方式</h4>
            <el-radio-group v-model="predictWay">
              <el-radio-button label="没标注的图" />
              <el-radio-button label="有标注的图" />
            </el-radio-group>
          </section>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import modelCard from './model-card'
import datasetsCard from './datasets-card'
import { listdatasets, getListmodel, createPredict } from '@/api/cervical'
import { taskStatus, createdBy } from '@/const/const'

export default {
  name: 'Newproject',
  components: { modelCard, datasetsCard },
  data() {
    return {
      step: 1,
      useTime: '1800',
      predictWay: '没标注的图',
      cutInput: 100,
      inputName: '',
      modelList: [],
      modelInfo: {},
      datasetsInfo: {},
      datasetsList: [],
      postCelltypes: [],
      postDatasetsInfo: {},
      postModelInfo: {}
    }
  },
  created() {
    this.getListmodel(10, 0)
    this.getListdatasets(20, 0, 1)
  },
  methods: {
    stepNext() {
      if (this.step++ > 1) {
        this.step = 2
      }
    },
    stepBack() {
      this.step = 1
    },
    getListmodel(limit, skip) {
      getListmodel({ 'limit': limit, 'skip': skip }).then(res => {
        if (res.data.data.total > 0) {
          this.modelList = res.data.data.models
          this.modelInfo = this.modelList[0]
        }
      })
    },
    getListdatasets(limit, skip, order) {
      listdatasets({ 'limit': limit, 'skip': skip, 'order': order }).then(res => {
        if (res.data.data.total > 0) {
          res.data.data.datasets.map(v => {
            v.created_by = createdBy[v.created_by] || '普通用户'
            v.status = taskStatus[v.status]
            v.parameter_cache = v.parameter_cache === 1 ? '使用' : '不使用'
            v.parameter_gray = v.parameter_gray === 1 ? '灰色' : '彩色'
            this.datasetsList = res.data.data.datasets
            this.datasetsInfo = this.datasetsList[0]
          })
        }
      })
    },
    createPredict() {
      createPredict({ 'did': this.datasetsInfo.id, 'mid': this.modelInfo.id, 'celltypes': this.postCelltypes }).then(res => {
        this.$message({
          message: res.data.data,
          type: 'success'
        })
      })
    },
    datasetsChange(val) {
      console.log(val, 'data')
    },
    modelChange(val) {
      console.log(val, 'model')
    },
    goDetail() {
      console.log(1)
    }
  }
}
</script>

<style lang="scss" scoped>
.newProject {
  .info {
    flex-wrap: wrap;
    justify-content: space-around;
  }
}
</style>
