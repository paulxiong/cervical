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
          <el-tab-pane v-if="!predictResult.parameter_type" type="info" :label="`图 ${total}`" class="img-tab">
            <section class="tools-bar flex">
              <span>审核状态</span>
              <el-select v-model="filterValue.filterChecked" placeholder="审核状态" size="mini" style="width: 100px;margin: 5px;" @change="filterChecked">
                <el-option
                  v-for="item in checkedOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
              <span>细胞类型</span>
              <el-select v-model="filterValue.filterCellsType" placeholder="细胞类型" size="mini" style="width: 100px;margin: 5px;" @change="filterCellsType">
                <el-option
                  v-for="item in CellsTypeOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </section>
            <section class="label-img flex">
              <div class="check-box" :style="{height: fov_img.w < 1000 ? fov_img.h + 'px' : (fov_img.h*(1000/fov_img.w)) + 'px'}">
                <div v-for="(v, idx) in orgImgList" :key="idx" class="item-box" style="padding: 5px;" :class="selectFov === idx ? 'select-fov' : ''" @click="changeFovImg(v, idx)">
                  <img class="img-item" :src="hosturlpath64 + v.imgpath + '?width=100'">
                </div>
              </div>
              <AIMarker
                v-if="fov_img.imgpath"
                ref="aiPanel-editor"
                class="ai-observer"
                :style="{width: fov_img.w < 1000 ? fov_img.w + 'px' : 1000 + 'px',height: fov_img.w < 1000 ? fov_img.h + 'px' : (fov_img.h*(1000/fov_img.w)) + 'px'}"
                :read="readOnly"
                :img="hosturlpath64 + fov_img.imgpath + '?width=1000'"
                @vmarker:onSelect="onSelect"
              />
              <div class="check-box" style="width: 200px" :style="{height: fov_img.w < 1000 ? fov_img.h + 'px' : (fov_img.h*(1000/fov_img.w)) + 'px'}">
                <div v-for="v in renderData" :id="`anchor-${v.id}`" :key="v.id" :class="select.id === v.id ? 'item-box-select' : 'item-box'" style="position: relative;">
                  <el-badge :value="`score=${v.predict_score}`" :type="v.predict_type === 51 ? 'warning': 'info'" class="item">
                    <img class="img-item" :class="select.id === v.id ? 'img-false' : 'img-right'" :src="hosturlpath64 + v.cellpath + '?width=64'" @click="changeLabel(v)">
                  </el-badge>
                  <svg-icon style="width:30px;height:30px;" class="check-icon" :icon-class="v.status === 1 ? 'checked' : 'unchecked'" />
                  <el-cascader
                    :value="v.status ? v.true_type : v.predict_type"
                    :options="cellsOptions"
                    :props="{ checkStrictly: true, expandTrigger: 'hover' }"
                    size="mini"
                    :show-all-levels="false"
                    @change="updatePredict"
                    @focus="selectCells(v)"
                  />
                </div>
              </div>
            </section>
          </el-tab-pane>
          <el-tab-pane label="log">
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
import { getPercent, getPredictResult, getPredictResult2, getjoblog, getDatasetImgs, updatePredict } from '@/api/cervical'
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
      fov_img: {},
      imgInfo: {},
      renderData: [],
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
      total: 0,
      cellsOptions: [
        {
          value: 50,
          label: '阴性',
          children: [
            {
              value: 1,
              label: 'Norm正常细胞'
            },
            {
              value: 5,
              label: 'NILM未见上皮内病变'
            },
            {
              value: 12,
              label: 'T滴虫'
            },
            {
              value: 13,
              label: 'M霉菌'
            },
            {
              value: 14,
              label: 'HSV疱疹'
            },
            {
              value: 15,
              label: 'X1线索细胞'
            }
          ]
        },
        {
          value: 51,
          label: '阳性',
          children: [
            {
              value: 2,
              label: 'LSIL鳞状上皮细胞低度病变'
            },
            {
              value: 3,
              label: 'HSIL鳞状上皮细胞高度病变'
            },
            {
              value: 4,
              label: 'HPV感染'
            },
            {
              value: 6,
              label: 'SCC鳞状上皮细胞癌'
            },
            {
              value: 7,
              label: 'ASCUS不典型鳞状细胞低'
            },
            {
              value: 8,
              label: 'ASCH不典型鳞状细胞高'
            },
            {
              value: 9,
              label: 'AGC不典型腺细胞'
            },
            {
              value: 10,
              label: 'AIS颈管原位腺癌'
            },
            {
              value: 11,
              label: 'ADC腺癌'
            }
          ]
        },
        {
          value: 100,
          label: '未知类型'
        },
        {
          value: 200,
          label: '不是细胞'
        }
      ],
      checkedOptions: [
        {
          value: 0,
          label: '未审核'
        },
        {
          value: 1,
          label: '已审核'
        },
        {
          value: 2,
          label: '全部'
        }
      ],
      CellsTypeOptions: [
        {
          value: 0,
          label: '阴性'
        },
        {
          value: 1,
          label: '阳性'
        },
        {
          value: 2,
          label: '全部'
        }
      ],
      filterValue: {
        'filterChecked': 2,
        'filterCellsType': 2
      }
    }
  },
  created() {
    this.getDatasetImgs()
    this.getPercent()
    this.getjoblog()
    this.loopGetPercent()
  },
  destroyed() {
    clearInterval(timer)
  },
  methods: {
    changeLabel(item) {
      this.select = item
      this.$refs['aiPanel-editor'].getMarker().clearData()
      this.$refs['aiPanel-editor'].getMarker().renderData(this.renderData)
      this.$refs['aiPanel-editor'].getMarker().renderData([item])
    },
    filterChecked(value) {
      switch (value) {
        case 0:
          this.renderData = this.imgInfo.cells.filter(v => v.status === 0)
          this.renderLabel(this.renderData)
          break
        case 1:
          this.renderData = this.imgInfo.cells.filter(v => v.status === 1)
          this.renderLabel(this.renderData)
          break
        default:
          this.renderData = this.imgInfo.cells
          this.renderLabel(this.renderData)
          break
      }
    },
    filterCellsType(value) {
      switch (value) {
        case 0:
          this.renderData = this.imgInfo.cells.filter(v => v.predict_type === 50)
          this.renderLabel(this.renderData)
          break
        case 1:
          this.renderData = this.imgInfo.cells.filter(v => v.predict_type === 51)
          this.renderLabel(this.renderData)
          break
        default:
          this.renderData = this.imgInfo.cells
          this.renderLabel(this.renderData)
          break
      }
    },
    updatePredict(value) {
      updatePredict({
        'id': this.select.id,
        'true_type': value.length === 2 ? value[1] : value[0]
      }).then(res => {
        this.$message({
          message: '审核修改成功',
          type: 'success'
        })
      })
    },
    selectCells(v) {
      this.select = v
    },
    changeFovImg(v, idx) {
      this.fov_img = v
      this.selectFov = idx
      this.getPredictResult2(v.id, 999, 0)
    },
    onSelect(data) {
      this.select = data
      document.querySelector(`#anchor-${data.id}`).scrollIntoView(true)
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
    getPredictResult2(iid, limit, skip) {
      getPredictResult2({ 'iid': iid, 'limit': limit, 'skip': skip }).then(res => {
        this.imgInfo = res.data.data
        this.imgInfo.cells.map(v => {
          v.tag = `${v.imgid}-${v.predict_type}`
          v.tagName = v.predict_type
          v.position = {
            x: parseFloat(v.x1 / this.fov_img.w) * 100 + '%',
            x1: parseFloat(v.x2 / this.fov_img.w) * 100 + '%',
            y: parseFloat(v.y1 / this.fov_img.h) * 100 + '%',
            y1: parseFloat(v.y2 / this.fov_img.h) * 100 + '%'
          }
          v.uuid = v.id
        })
        this.renderData = this.imgInfo.cells
        this.renderLabel(this.renderData)
      })
    },
    getDatasetImgs(did) {
      getDatasetImgs({ 'did': this.$route.query.did }).then(res => {
        this.orgImgList = res.data.data.images
        this.fov_img = this.orgImgList[0]
        this.total = res.data.data.total
        this.getPredictResult2(this.fov_img.id, 999, 0)
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
    renderLabel(cells) {
      this.$refs['aiPanel-editor'].getMarker().clearData()
      this.$refs['aiPanel-editor'].getMarker().renderData(cells)
      this.select = cells[cells.length - 1]
      setTimeout(() => {
        document.querySelector(`#anchor-${this.select.id}`).scrollIntoView(true)
      }, 100)
    }
  }
}
</script>

<style lang="scss" scoped>
.predict {
  .img-tab {
    .label-img {
      justify-content: flex-start;
    }
    .item-box {
      padding: 10px 10px;
      border-bottom: 1px solid #ccc;
    }
    .tools-bar {
      justify-content: flex-start;
      margin-left: 5px;
      span {
        font-size: 14px;
      }
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
    .check-icon {
      position: absolute;
      top: 0;
      right: 0;
    }
  }
  .select-fov {
    background: rgba(238, 255, 0, 0.5);
  }
  .results {
    padding: 7px 30px;
    .item-box-select {
      padding: 10px 10px;
      border-bottom: 1px solid #ccc;
      background: rgba(238, 255, 0, 0.5);
    }
    .img-item {
      // margin-right: 10px;
      // margin-bottom: 10px;
    }
    .img-select {
      border: 2px solid rgb(238, 255, 0);
    }
    .img-right {
      border: 2px solid rgb(0, 255, 81);
      border-radius: 5px;
    }
    .img-false {
      border: 2px solid rgb(238, 255, 0);
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
