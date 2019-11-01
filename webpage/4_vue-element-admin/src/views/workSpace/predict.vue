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
      />
    </section>
    <section class="results">
      <section class="info-box">
        <el-table :data="predictResult.result" stripe border style="width: 100%">
          <el-table-column prop="type" width="400" label="类型" />
          <el-table-column prop="total" label="实际预测个数" />
          <el-table-column prop="falseCnt" label="错误个数" />
          <el-table-column prop="correct" label="正确个数" />
        </el-table>
      </section>
      <section class="img-list">
        <el-tabs tab-position="left" class="img-tabs">
          <el-tab-pane :label="`错误细胞 ${falseCellsList.length}`">
            <el-tooltip v-for="v in falseCellsList" :key="v.url" :content="`实际${v.type} - 预测${v.predict}`" effect="dark" class="item" placement="bottom">
              <img class="img-item img-false" :src="hosturlpath64+v.url">
            </el-tooltip>
          </el-tab-pane>
          <el-tab-pane :label="`正确细胞 ${rightCellsList.length}`">
            <el-tooltip v-for="v in rightCellsList" :key="v.url" :content="v.type" effect="dark" class="item" placement="bottom">
              <img class="img-item img-right" :src="hosturlpath64+v.url">
            </el-tooltip>
          </el-tab-pane>
        </el-tabs>
      </section>
    </section>
  </div>
</template>

<script>
import { ImgServerUrl } from '@/const/config'
import { cellsType } from '@/const/const'
import { getPercent, getPredictResult } from '@/api/cervical'
let timer

export default {
  name: 'Predict',
  components: {},
  data() {
    return {
      percentage: 0,
      startPredict: false,
      modelList: [],
      modelInfo: {},
      datasetsInfo: {},
      datasetsList: [],
      postCelltypes: [],
      hosturlpath64: ImgServerUrl + '/unsafe/64x0/',
      predictResult: {},
      rightCellsList: [],
      falseCellsList: []
    }
  },
  created() {
    this.getPredictResult()
  },
  beforedestroy() {
    clearInterval(timer)
  },
  methods: {
    getPredictResult() {
      getPredictResult({ 'id': this.$route.query.pid }).then(res => {
        if (typeof res.data.data !== 'string') {
          res.data.data.result.map(v => {
            v.falseCnt = v.total - v.correct
          })
          this.predictResult = res.data.data
          this.predictResult.crop_cells.map(v => {
            if (v.type === v.predict) {
              this.rightCellsList.push(v)
            } else {
              this.falseCellsList.push(v)
            }
            v.type = cellsType[v.type]
            v.predict = cellsType[v.predict]
          })
        }
      })
    },
    getPercent() {
      getPercent({ id: this.$route.query.pid, job: 2 }).then(res => {
        this.percentage = res.data.data
        if (this.percentage === 100) {
          clearInterval(timer)
        }
      })
    },
    /**
     * 定时器轮训百分比
     */
    loopGetPercent() {
      timer = setInterval(() => {
        this.getPercent()
        if (this.percentage === 100) {
          this.getPercent()
          clearInterval(timer)
        }
      }, 1e4)
    },
    changeCellTypes(val) {
      this.postCelltypes = val
    }
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
      border: 2px solid #27cc6a;
      border-radius: 5px;
    }
    .img-false {
      border: 2px solid #fd6e70;
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
