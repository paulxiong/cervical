<template>
  <div class="predict">
    <section v-loading="loading" :element-loading-text="loadingtext" class="results">
      <section v-if="!report" class="info-box">
        <el-table :data="predictResult.result" stripe border style="width: 100%">
          <el-table-column prop="type" width="400" label="类型" />
          <el-table-column prop="total" label="预测个数" />
          <el-table-column v-if="predictResult.parameter_type" prop="falseCnt" label="错误个数" />
          <el-table-column v-if="predictResult.parameter_type" prop="correct" label="正确个数" />
        </el-table>
      </section>
      <section class="img-list">
        <el-tabs tab-position="left" class="img-tabs">
          <el-tab-pane v-if="!report" :label="`错误细胞 ${falseCellsList.length}`" class="img-tab flex">
            <div v-for="v in falseCellsList" :key="v.url" class="item-box" style="padding: 20px;">
              <el-badge :value="`${v.type}>${v.predict}`" type="info" class="item">
                <img class="img-item img-false" :src="hosturlpath64 + v.url + '?width=64'">
              </el-badge>
            </div>
          </el-tab-pane>
          <el-tab-pane v-if="!report" type="info" :label="`正确细胞 ${rightCellsList.length}`" class="img-tab flex">
            <div v-for="v in rightCellsList" :key="v.url" class="item-box" style="padding: 20px;">
              <el-badge :value="`${v.type}-${v.score}`" class="item">
                <img class="img-item img-right" :src="hosturlpath64 + v.url + '?width=64'">
              </el-badge>
            </div>
          </el-tab-pane>
          <el-tab-pane v-if="report" type="info" :label="`图 ${total}`" class="img-tab">
            <section class="tools-bar flex">
              <div>总进度:{{ imgCellsInfo.cellsverified }} / {{ imgCellsInfo.cellsall }}</div>
              <div class="fitler-tools">
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
                <el-button class="filter-btn" type="primary" size="mini" :icon="loading?'el-icon-loading':'el-icon-refresh-left'" @click="filterSearch">刷新</el-button>
              </div>
              <div>当前图片进度:{{ imgCellsInfo.imgcellsverified }} / {{ imgCellsInfo.imgcellsall }}</div>
            </section>
            <section v-if="orgImgList.length" class="label-img flex">
              <div class="check-box" style="width: 110px" :style="{height: fov_img.w < 1000 ? fov_img.h + 'px' : (fov_img.h*(1000/fov_img.w)) + 'px'}">
                <div v-for="(v, idx) in orgImgList" :key="idx" class="item-box" style="padding: 3px 3px 0px 4px;" :class="selectFov === idx ? 'select-fov' : ''" @click="changeFovImg(v, idx)">
                  <el-image class="img-item" :src="hosturlpath64 + v.imgpath + '?width=100'" lazy />
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
                    <el-image class="img-item" :class="select.id === v.id ? 'img-false' : 'img-right'" :src="hosturlpath64 + v.cellpath + '?width=64'" @click="changeLabel(v)" />
                  </el-badge>
                  <svg-icon style="width:30px;height:30px;" class="check-icon" :icon-class="v.status === 1 ? 'checked' : v.status === 2 ? 'delete' : v.status === 3 ? 'adminA' : 'unchecked'" />
                  <el-cascader
                    :disabled="report === 'admin'"
                    :value="v.status ? v.true_type : v.predict_type"
                    :options="cellsOptions"
                    :props="{ checkStrictly: true }"
                    size="mini"
                    :show-all-levels="false"
                    @change="updatePredict"
                    @focus="selectCells(v)"
                  />
                  <el-radio-group v-if="report === 'admin'" v-model="v.status" size="mini" style="position: absolute;top: 45px;right: 0;" @change="updateAdminValue">
                    <el-radio-button label="错误" />
                    <el-radio-button label="正确" />
                  </el-radio-group>
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
import { getPercent, getPredictResult, getPredictResult2, getjoblog, getDatasetImgs, updatePredict, reviewpredict } from '@/api/cervical'
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
      adminValue: '错误',
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
          label: '移除'
        },
        {
          value: 3,
          label: '管理员已确认'
        },
        {
          value: 4,
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
        'filterChecked': 0, // 0 未审核 1 已审核 2 移除 3 管理员确认 4 全部
        'filterCellsType': 2
      },
      report: '',
      imgCellsInfo: {}
    }
  },
  created() {
    this.report = this.$route.query.report
    this.filterValue.filterChecked = this.report === 'admin' ? 1 : 0
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
    updateAdminValue(val) {
      const status = val === '错误' ? 2 : 3
      reviewpredict({
        'id': this.select.id,
        'status': status
      }).then(res => {
        this.changeLabel(this.select)
        this.$message({
          message: '审核确认成功',
          type: 'success'
        })
      })
    },
    filterSearch() {
      this.getPredictResult2(this.fov_img.id, 999, 0, this.filterValue.filterChecked)
      this.$nextTick(() => {
        this.filterCellsType(this.filterValue.filterCellsType)
      })
    },
    filterChecked(value, select) {
      this.getPredictResult2(this.fov_img.id, 999, 0, this.filterValue.filterChecked)
    },
    filterCellsType(value) {
      switch (value) {
        case 0:
          this.renderData = this.imgInfo.cells.filter(v => v.predict_type === 50)
          break
        case 1:
          this.renderData = this.imgInfo.cells.filter(v => v.predict_type === 51)
          break
        default:
          this.renderData = this.imgInfo.cells
          break
      }
      this.renderLabel(this.renderData)
    },
    updatePredict(value) {
      updatePredict({
        'id': this.select.id,
        'true_type': value.length === 2 ? value[1] : value[0]
      }).then(res => {
        this.filterSearch()
        this.imgCellsInfo.imgcellsall = res.data.data.imgcellsall
        this.imgCellsInfo.imgcellsverified = res.data.data.imgcellsverified
        this.imgCellsInfo.cellsall = res.data.data.cellsall
        this.imgCellsInfo.cellsverified = res.data.data.cellsverified
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
      this.getPredictResult2(v.id, 999, 0, this.filterValue.filterChecked)
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
    getPredictResult2(iid, limit, skip, status, select) {
      getPredictResult2({ 'iid': iid, 'limit': limit, 'skip': skip, 'status': status }).then(res => {
        this.imgInfo = res.data.data
        this.imgInfo.cells.map(v => {
          v.tag = `${v.imgid}-${v.status === 1 ? v.true_type : v.predict_type}`
          v.tagName = v.status === 1 ? v.true_type : v.predict_type
          v.position = {
            x: parseFloat(v.x1 / this.fov_img.w) * 100 + '%',
            x1: parseFloat(v.x2 / this.fov_img.w) * 100 + '%',
            y: parseFloat(v.y1 / this.fov_img.h) * 100 + '%',
            y1: parseFloat(v.y2 / this.fov_img.h) * 100 + '%'
          }
          v.uuid = v.id
        })
        this.renderData = this.imgInfo.cells
        this.imgCellsInfo = this.imgInfo.info
        this.renderLabel(this.renderData, select)
        if (select) this.changeLabel(this.select)
      })
    },
    getDatasetImgs(did) {
      getDatasetImgs({ 'did': this.$route.query.did }).then(res => {
        this.orgImgList = res.data.data.images
        this.total = res.data.data.total
        if (this.orgImgList.length) {
          this.fov_img = this.orgImgList[0]
          this.getPredictResult2(this.fov_img.id, 999, 0, this.filterValue.filterChecked)
        } else {
          this.$alert('所选数据集为空', '提示', {
            confirmButtonText: '确定'
          })
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
        if (this.status >= 3) {
          this.loading = false
          clearInterval(timer)
          if (this.$route.query.report) {
            this.getDatasetImgs()
          } else {
            this.getPredictResult()
          }
          this.getjoblog()
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
        this.getPercent()
      }, 1500)
    },
    changeCellTypes(val) {
      this.postCelltypes = val
    },
    renderLabel(cells, select) {
      this.$refs['aiPanel-editor'].getMarker().clearData()
      if (cells.length < 1) return
      this.$refs['aiPanel-editor'].getMarker().renderData(cells)
      if (!select) {
        this.select = cells[cells.length - 1]
        this.$nextTick(() => {
          document.querySelector(`#anchor-${this.select.id}`).scrollIntoView(true)
        })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.predict {
  .img-tab {
    justify-content: flex-start;
    flex-wrap: wrap;
    .label-img {
      justify-content: flex-start;
    }
    .item-box {
      padding: 10px 10px;
      border-bottom: 1px solid #ccc;
    }
    .tools-bar {
      width: 1310px;
      justify-content: space-between;
      margin-left: 7px;
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
