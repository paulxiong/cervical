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
          <el-tab-pane v-if="!predictResult.parameter_type" type="info" :label="`细胞图 ${total}`" class="img-tab flex">
            <section class="label-img flex">
              <div class="check-box" :style="{height: imgInfo.imgw < 1000 ? imgInfo.imgh + 'px' : (imgInfo.imgh*(1000/imgInfo.imgw)) + 'px'}">
                <div v-for="(v, idx) in orgImgList" :key="idx" class="item-box" style="padding: 5px;" :class="selectFov === idx ? 'select-fov' : ''" @click="changeFovImg(v, idx)">
                  <img class="img-item" :src="hosturlpath64 + v.imgpath + '?width=100'">
                </div>
              </div>
              <AIMarker
                ref="aiPanel-editor"
                class="ai-observer"
                :style="{width: imgInfo.imgw < 1000 ? imgInfo.imgw + 'px' : 1000 + 'px',height: imgInfo.imgw < 1000 ? imgInfo.imgh + 'px' : (imgInfo.imgh*(1000/imgInfo.imgw)) + 'px'}"
                :read="readOnly"
                :img="hosturlpath64 + fov_img + '?width=1000'"
                @vmarker:onSelect="onSelect"
              />
              <div class="check-box" :style="{height: imgInfo.imgw < 1000 ? imgInfo.imgh + 'px' : (imgInfo.imgh*(1000/imgInfo.imgw)) + 'px'}">
                <div v-for="(v, idx) in rightCellsList" :id="`anchor-${idx}`" :key="v.url" class="item-box">
                  <el-badge :value="`score=${v.score}`" :type="v.type === '50' ? 'warning': 'info'" class="item">
                    <img class="img-item" :class="idx === 0 ? 'img-false' : 'img-right'" :src="hosturlpath64 + v.url + '?width=64'" @click="changeLabel(v, idx)">
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
import { getPercent, getPredictResult, getjoblog, getLabelByImageId, getDatasetImgs } from '@/api/cervical'
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
      fov_img: '',
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
      falseCellsList: [],
      select: {},
      selectFov: 0,
      orgImgList: [],
      total: 0
    }
  },
  created() {
    this.getPredictResult()
    this.getDatasetImgs(62)
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
    changeLabel(item, idx) {
      this.select = this.imgInfo.labels[idx]
      const labels = this.imgInfo.labels
      labels.map((v, i) => {
        if (this.select.id === v.id) {
          labels.splice(i, 1)
        }
      })
      labels.push(this.select)
      this.renderLabel(labels)
    },
    changeFovImg(v, idx) {
      this.fov_img = v.imgpath
      this.selectFov = idx
    },
    onSelect(data) {
      this.select = data
      document.querySelector(`#anchor-${parseInt(Math.random() * 10) + 10}`).scrollIntoView(true)
    },
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
    getDatasetImgs(did) {
      getDatasetImgs({ 'did': did }).then(res => {
        this.orgImgList = res.data.data.images
        this.fov_img = this.orgImgList.length ? this.orgImgList[this.orgImgList.length - 1].imgpath : ''
        this.total = res.data.data.total
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
        if ((this.percentage === 100) || (this.status >= 3) || (this.ETA === 0)) {
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
        this.select = this.imgInfo.labels[5]
        this.renderLabel(this.imgInfo.labels)
      })
    },
    /**
     * 定时器轮训百分比
     */
    loopGetPercent() {
      timer = setInterval(() => {
        if ((this.percentage === 100) || (this.status >= 3) || (this.ETA === 0)) {
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
    renderLabel(lables) {
      this.$refs['aiPanel-editor'].getMarker().clearData()
      this.$refs['aiPanel-editor'].getMarker().renderData(lables)
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
      padding: 10px 10px;
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
    border: 1px dashed #ccc;
    margin-left: 7px;
  }
  .select-fov {
    background: rgb(255, 0, 255);
  }
  .results {
    padding: 7px 30px;
    .img-item {
      // margin-right: 10px;
      // margin-bottom: 10px;
    }
    .img-select {
      border: 2px solid rgb(255, 0, 255);
    }
    .img-right {
      border: 2px solid rgb(0, 255, 81);
      border-radius: 5px;
    }
    .img-false {
      border: 2px solid rgb(255, 0, 255);
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
