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
    <section class="content" v-if="!startPredict">
      <section class="model-info" v-if="modelList.length">
        <el-badge is-dot class="badge">模型信息</el-badge>
        <modelCard
          :modelInfo="modelInfo"
          :predict="predict"
          :modelList="modelList"
          @changeCellTypes="changeCellTypes"
        />
      </section>
      <section class="datasets-info" v-if="datasetsList.length">
        <el-badge is-dot class="badge">数据信息</el-badge>
        <datasetsCard :datasetsInfo="datasetsInfo" :predict="predict" :datasetsList="datasetsList" />
      </section>
    </section>
    <section class="results" v-else>
      <section class="info-box">
        <el-table :data="predictResult.result" stripe border style="width: 100%">
          <el-table-column prop="type" width="400" label="类型"></el-table-column>
          <el-table-column prop="total_org" label="输入个数"></el-table-column>
          <el-table-column prop="total" label="实际预测个数"></el-table-column>
          <el-table-column prop="count_false" label="错误个数"></el-table-column>
          <el-table-column prop="count_right" label="正确个数"></el-table-column>
        </el-table>
      </section>
      <section class="img-list">
        <el-tabs tab-position="left" v-loading="loading" class="img-tabs">
          <el-tab-pane :label="`错误细胞 ${falseCellsList.length}`">
            <el-image
              class="img-item img-false"
              v-for="(img,idx) in falseCellsList"
              :key="idx"
              :src="hosturlpath64 + img.url"
              lazy
            >
              <div slot="error" class="image-slot">
                <i class="el-icon-picture-outline"></i>
              </div>
            </el-image>
          </el-tab-pane>
          <el-tab-pane :label="`正确细胞 ${rightCellsList.length}`">
            <el-image
              class="img-item img-false"
              v-for="(img,idx) in rightCellsList"
              :key="idx"
              :src="hosturlpath64 + img.url"
              lazy
            >
              <div slot="error" class="image-slot">
                <i class="el-icon-picture-outline"></i>
              </div>
            </el-image>
          </el-tab-pane>
        </el-tabs>
      </section>
    </section>
  </div>
</template>

<script>
import modelCard from './components/model-card'
import datasetsCard from './components/datasets-card'
import { ImgServerUrl } from '@/const/config'
import { cellsType } from '@/const/const'
import { listdatasets, getListmodel, createPredict, getPredictResult } from '@/api/cervical'

export default {
  name: 'Predict',
  components: { modelCard, datasetsCard },
  data() {
    return {
      percentage: 0,
      predict: 'predict',
      startPredict: false,
      loading: true,
      modelList: [],
      modelInfo: {},
      datasetsInfo: {},
      datasetsList: [],
      postCelltypes: [],
      hosturlpath64: ImgServerUrl + '/unsafe/64x0/scratch/',
      predictResult: {},
      rightCellsList: [],
      falseCellsList: []
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
      createPredict({ 'did': this.datasetsInfo.id, 'mid': this.modelInfo.id, 'celltypes': this.postCelltypes }).then(res => {
        this.$message({
          message: res.data.data,
          type: 'success'
        })
        getPredictResult({ 'id': this.datasetsInfo.id }).then(res => {
          this.predictResult = res.data.data
          this.predictResult.result.map(v => {
            v.type = cellsType[v.type]
            v.count_right = v.total - v.count_false
          })
          this.predictResult.crop_cells.map(v => {
            if(v.type === v.predict) {
              this.rightCellsList.push(v)
            } else {
              this.falseCellsList.push(v)
            }
          })
        })
        this.startPredict = true
        this.loading = false
        this.percentage = 100
      })
    },
    changeCellTypes(val) {
      this.postCelltypes = val
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
  .info-box {
    margin-bottom: 20px;
  }
  .results {
    padding: 30px;
    .img-item {
      margin-right: 10px;
      margin-bottom: 10px;
    }
    .img-right {
      border: 5px solid #27cc6a;
      border-radius: 5px;
    }
    .img-false {
      border: 5px solid #fd6e70;
      border-radius: 5px;
    }
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
