<template>
  <div class="predict">
    <!-- <section class="header flex">
      <el-badge is-dot class="badge">预测进度</el-badge>
      <el-progress
        :text-inside="true"
        :stroke-width="26"
        :percentage="percentage"
        class="progress"
        status="success"
      />
    </section> -->
    <section v-loading="loading" :element-loading-text="loadingtext" class="results">
      <!-- <section class="info-box">
        <el-table :data="predictResult.result" stripe border style="width: 100%">
          <el-table-column prop="type" width="400" label="类型" />
          <el-table-column prop="total" label="预测个数" />
          <el-table-column v-if="predictResult.parameter_type" prop="falseCnt" label="错误个数" />
          <el-table-column v-if="predictResult.parameter_type" prop="correct" label="正确个数" />
        </el-table>
      </section> -->
      <section class="img-list">
        <el-tabs tab-position="left" class="img-tabs">
          <el-tab-pane v-if="predictResult.parameter_type" :label="`错误细胞 ${falseCellsList.length}`" class="img-tab flex">
            <div v-for="v in falseCellsList" :key="v.url" class="item-box">
              <el-badge :value="`${v.type}>${v.predict}`" type="info" class="item">
                <img class="img-item img-false" :src="hosturlpath64 + v.url + '?width=64'">
              </el-badge>
            </div>
          </el-tab-pane>
          <el-tab-pane v-if="predictResult.parameter_type" type="info" :label="`正确细胞 ${rightCellsList.length}`" class="img-tab flex">
            <div v-for="v in rightCellsList" :key="v.url" class="item-box">
              <el-badge :value="`${v.type}-${v.score}`" class="item">
                <img class="img-item img-right" :src="hosturlpath64 + v.url + '?width=64'">
              </el-badge>
            </div>
          </el-tab-pane>
          <el-tab-pane v-if="!predictResult.parameter_type" type="info" :label="`细胞图 ${rightCellsList.length}`" class="img-tab flex">
            <section class="label-img flex">
              <AIMarker
                ref="aiPanel-editor"
                class="ai-observer"
                :style="{width: imgInfo.imgw < 1000 ? imgInfo.imgw + 'px' : 1000 + 'px',height: imgInfo.imgw < 1000 ? imgInfo.imgh + 'px' : (imgInfo.imgh*(1000/imgInfo.imgw)) + 'px'}"
                :read="readOnly"
                :img="fov_img"
              />
              <div class="check-box" :style="{height: imgInfo.imgw < 1000 ? imgInfo.imgh + 'px' : (imgInfo.imgh*(1000/imgInfo.imgw)) + 'px'}">
                <div v-for="v in rightCellsList" :key="v.url" class="item-box">
                  <el-badge :value="`score:${v.score}`" :type="v.type === '50' ? 'warning': 'info'" class="item">
                    <img class="img-item img-right" :src="hosturlpath64 + v.url + '?width=64'">
                  </el-badge>
                  <el-radio-group v-model="v.type" size="mini">
                    <el-radio-button label="51">阴性</el-radio-button>
                    <el-radio-button label="50">阳性</el-radio-button>
                    <el-radio-button label="100">不确定</el-radio-button>
                  </el-radio-group>
                </div>
              </div>
            </section>
          </el-tab-pane>
          <el-tab-pane label="预测log">
            <el-input
              v-model="cLog"
              type="textarea"
              :rows="2"
              placeholder="预测log"
              :autosize="{ minRows: 2, maxRows: 16}"
              readonly
            >1</el-input>
          </el-tab-pane>
        </el-tabs>
      </section>
    </section>
  </div>
</template>

<script>
import { APIUrl } from '@/const/config'
import { cellsType } from '@/const/const'
import { getPercent, getPredictResult, getjoblog, getLabelByImageId } from '@/api/cervical'
import { AIMarker } from '@/components/vue-picture-bd-marker/label.js'

let timer

export default {
  name: 'Predict',
  components: { AIMarker },
  data() {
    return {
      percentage: 0,
      startPredict: false,
      readOnly: true,
      url: APIUrl + '/imgs/',
      fov_img: 'img/20190523/1807178/Images/IMG001x014.JPG?width=1000',
      imgInfo: {},
      modelList: [],
      modelInfo: {},
      datasetsInfo: {},
      datasetsList: [],
      loading: true,
      ETA: 10,
      status: 0,
      loadingtext: '正在执行',
      postCelltypes: [],
      cLog: '',
      hosturlpath64: APIUrl + '/imgs/',
      predictResult: {},
      rightCellsList: [],
      falseCellsList: []
    }
  },
  created() {
    this.getPredictResult()
    this.getPercent()
    this.getjoblog()
    this.loopGetPercent()
    this.fov_img = this.url + this.fov_img
    this.getLabelByImageId(1909, 10)
  },
  destroyed() {
    clearInterval(timer)
  },
  methods: {
    getPredictResult() {
      getPredictResult({ 'id': this.$route.query.pid }).then(res => {
        if (typeof res.data.data !== 'string') {
          if (res.data.data.result) {
            res.data.data.result.map(v => {
              v.falseCnt = v.total - v.correct
              v.type = cellsType[v.type]
            })
          }
          this.predictResult = res.data.data
          if (res.data.data.crop_cells) {
            this.predictResult.crop_cells.map(v => {
              if (v.type === v.predict) {
                this.rightCellsList.push(v)
              } else {
                this.falseCellsList.push(v)
              }
            })
          }
        }
      })
    },
    getjoblog() {
      // type 0 未知 1 数据集处理 2 训练 3 预测
      getjoblog({ id: this.$route.query.pid, type: '3' }).then(res => {
        this.cLog = res.data.data
      })
    },
    getPercent() {
      // type 0 未知 1 数据集处理 2 训练 3 预测
      getPercent({ id: this.$route.query.pid, type: 3 }).then(res => {
        this.percentage = res.data.data.percent
        this.status = res.data.data.status
        this.ETA = res.data.data.ETA
        if ((this.percentage === 100) || (this.status === 4) || (this.ETA === 0)) {
          this.loading = false
          clearInterval(timer)
        } else {
          this.loadingtext = '预计还需要' + this.ETA + '秒'
        }
      })
    },
    getLabelByImageId(id, status) {
      getLabelByImageId({ 'limit': 999, 'skip': 0, 'imgid': id, 'status': status }).then(res => {
        this.imgInfo = res.data.data
        this.imgInfo.labels.map(v => {
          v.tag = `${v.imgid}-${v.type}`
          v.tagName = v.type
          v.position = {
            x: parseFloat(v.x1 / this.imgInfo.imgw) * 100 + '%',
            x1: parseFloat(v.x2 / this.imgInfo.imgw) * 100 + '%',
            y: parseFloat(v.y1 / this.imgInfo.imgh) * 100 + '%',
            y1: parseFloat(v.y2 / this.imgInfo.imgh) * 100 + '%'
          }
          v.uuid = v.id
        })
        this.renderLabel()
      })
    },
    /**
     * 定时器轮训百分比
     */
    loopGetPercent() {
      timer = setInterval(() => {
        if ((this.percentage === 100) || (this.status === 4) || (this.ETA === 0)) {
          this.getPercent()
          this.getjoblog()
          location.reload()
          clearInterval(timer)
        }
      }, 5000)
    },
    changeCellTypes(val) {
      this.postCelltypes = val
    },
    renderLabel() {
      this.$refs['aiPanel-editor'].getMarker().clearData()
      this.$refs['aiPanel-editor'].getMarker().renderData(this.imgInfo.labels)
    }
  }
}
</script>

<style lang="scss" scoped>
.predict {
  .img-tab {
    justify-content: flex-start;
    flex-wrap: wrap;
    .item-box {
      padding: 10px 20px;
      border-bottom: 1px solid #ccc;
    }
  }
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
    margin-bottom: 7px;
  }
  .check-box {
    overflow: auto;
    width: 220px;
    border: 1px dashed #ccc;
    margin-left: 7px;
  }
  .results {
    padding: 7px 30px;
    .img-item {
      // margin-right: 10px;
      // margin-bottom: 10px;
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
