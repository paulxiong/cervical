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
          <el-tab-pane v-if="!report" type="info" :label="`正确细胞 ${predictResult.correc_total ? predictResult.correc_total : ''}`" class="img-tab">
            <div class="img-div flex" style="overflow-y: auto;height:600px;">
              <div v-for="v in rightCellsList" :key="v.url" class="item-box" style="padding: 20px;">
                <el-badge :value="`${v.type}-${v.score}`" :type="v.type === 51 ? 'warning': 'info'" class="item">
                  <el-image class="img-item img-right" :src="hosturlpath64 + v.url + '?width=64'" lazy />
                </el-badge>
              </div>
            </div>
            <el-pagination
              v-if="predictResult.correc_total"
              class="page"
              :current-page.sync="currentPage"
              :page-sizes="[500, 1000, 2000, 5000]"
              :page-size="currentPageSize"
              layout="total, sizes, prev, pager, next, jumper"
              :total="predictResult.correc_total"
              @current-change="handleCurrentChange"
              @size-change="handleSizeChange"
            />
          </el-tab-pane>
          <el-tab-pane v-if="!report" :label="`错误细胞 ${predictResult.incorrec_total ? predictResult.incorrec_total : ''}`" class="img-tab flex">
            <div class="img-div" style="overflow-y: auto;height:600px;">
              <div v-for="v in falseCellsList" :key="v.url" class="item-box" style="padding: 20px;">
                <el-badge :value="`${v.type}>${v.predict}`" :type="v.type === 51 ? 'warning': 'info'" class="item">
                  <el-image class="img-item img-false" :src="hosturlpath64 + v.url + '?width=64'" lazy />
                </el-badge>
              </div>
            </div>
            <el-pagination
              v-if="predictResult.incorrec_total"
              class="page"
              :current-page.sync="currentPage2"
              :page-sizes="[500, 1000, 2000, 5000]"
              :page-size="currentPageSize2"
              layout="total, sizes, prev, pager, next, jumper"
              :total="incorrec_total"
              @current-change="handleCurrentChange2"
              @size-change="handleSizeChange2"
            />
          </el-tab-pane>
          <el-tab-pane v-if="report" type="info" :label="`原图 ${total}`" class="img-tab flex">
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
                <span>细胞类型: {{ renderData.length }}个</span>
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
              <div v-if="select.id" class="check-box" style="width: 200px;display:flex;justify-content:space-between;flex-direction:column;align-items:center;" :style="{height: fov_img.w < 1000 ? fov_img.h + 'px' : (fov_img.h*(1000/fov_img.w)) + 'px'}">
                <div class="item-box-select" style="position: relative;">
                  <el-badge :value="`${select.predict_score}`" :type="select.predict_type === 51 ? 'warning': 'info'" class="item">
                    <el-image class="img-item img-right" :src="hosturlpath64 + select.cellpath + '?width=100'" lazy />
                  </el-badge>
                  <svg-icon style="width:30px;height:30px;" class="check-icon" :icon-class="select.status === 1 ? 'checked' : select.status === 2 ? 'delete' : select.status === 3 ? 'adminA' : 'unchecked'" />
                  <el-cascader
                    v-if="select.status"
                    v-model="select.true_type"
                    :disabled="report === 'admin'"
                    :options="cellsOptions"
                    :props="{ checkStrictly: true }"
                    size="mini"
                    :show-all-levels="false"
                    @change="updatePredict"
                  />
                  <el-cascader
                    v-else
                    v-model="select.predict_type"
                    :disabled="report === 'admin'"
                    :options="cellsOptions"
                    :props="{ checkStrictly: true }"
                    size="mini"
                    :show-all-levels="false"
                    @change="updatePredict"
                  />
                  <el-radio-group v-if="report === 'admin'" v-model="select.status" size="mini" style="position: absolute;top: 45px;right: 0;" @change="updateAdminValue">
                    <el-radio-button label="错误" />
                    <el-radio-button label="正确" />
                  </el-radio-group>
                </div>
                <div class="checked-all flex">
                  <el-dialog
                    title="提示"
                    :visible.sync="centerDialogVisible"
                    width="30%"
                    center
                    @close="closeDialog"
                  >
                    <span>是否将以下 <span style="color:#ff3c43;">{{ renderData.length }}</span> 个细胞一键审核为
                      <el-cascader
                        v-if="report === 'doctor'"
                        v-model="all_true_type"
                        :options="cellsOptions"
                        :props="{ checkStrictly: true }"
                        size="mini"
                        :show-all-levels="false"
                      />
                      <el-radio-group v-else v-model="all_tf" size="mini">
                        <el-radio-button label="错误" />
                        <el-radio-button label="正确" />
                      </el-radio-group>
                    </span>
                    <span slot="footer" class="dialog-footer">
                      <el-button @click="centerDialogVisible = false">取 消</el-button>
                      <el-button type="primary" :loading="updateLoading" @click="checkedAll">确 定</el-button>
                    </span>
                  </el-dialog>
                  <el-button type="danger" :disabled="!renderData.length" @click="showDialogCheckAll">一键审核</el-button>
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
  filters: {
    filtersTrueType(val) {
      return cellsType[val]
    }
  },
  data() {
    return {
      percentage: 0,
      startPredict: false,
      centerDialogVisible: false,
      updateLoading: false,
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
      select: {
        cellpath: ''
      },
      selectFov: 0,
      orgImgList: [],
      adminValue: '正确',
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
          label: '未知类型'
        },
        {
          value: 3,
          label: '不是细胞'
        },
        {
          value: 4,
          label: '全部'
        }
      ],
      filterValue: {
        'filterChecked': 0, // 0 未审核 1 已审核 2 移除 3 管理员确认 4 全部
        'filterCellsType': 1
      },
      report: '',
      all_true_type: 100,
      all_tf: '正确',
      imgCellsInfo: {},
      currentPage: 1,
      currentPage2: 1,
      currentPageSize: 500,
      currentPageSize2: 100
    }
  },
  created() {
    this.report = this.$route.query.report
    this.loopGetPercent()
  },
  beforeDestroy() {
    clearInterval(timer)
  },
  methods: {
    updateAdminValue(val) {
      const status = val === '错误' ? 2 : 3
      reviewpredict({
        'id': this.select.id,
        'status': status
      }).then(res => {
        this.$message({
          message: '审核确认成功',
          type: 'success'
        })
      })
    },
    filterSearch() {
      this.getPredictResult2(this.fov_img.id, 999, 0, this.filterValue.filterChecked)
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.getPredictResult(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
    },
    handleSizeChange(val) {
      this.currentPageSize = val
      this.getPredictResult(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, 1)
    },
    handleCurrentChange2(val) {
      this.currentPage2 = val
      this.getPredictResult(this.currentPageSize2, (this.currentPage2 - 1) * this.currentPageSize2, 0)
    },
    handleSizeChange2(val) {
      this.currentPageSize2 = val
      this.getPredictResult(this.currentPageSize2, (this.currentPage2 - 1) * this.currentPageSize2, 0)
    },
    filterChecked(value, select) {
      this.getPredictResult2(this.fov_img.id, 999, 0, this.filterValue.filterChecked)
    },
    filterCellsType() {
      switch (this.filterValue.filterCellsType) {
        case 0:
          this.renderData = this.imgInfo.cells.filter(v => this.filterValue.filterChecked === 1 ? v.true_type === 50 : v.predict_type === 50)
          break
        case 1:
          this.renderData = this.imgInfo.cells.filter(v => this.filterValue.filterChecked === 1 ? v.true_type === 51 : v.predict_type === 51)
          break
        case 2:
          this.renderData = this.imgInfo.cells.filter(v => this.filterValue.filterChecked === 1 ? v.true_type === 100 : v.predict_type === 100)
          break
        case 3:
          this.renderData = this.imgInfo.cells.filter(v => this.filterValue.filterChecked === 1 ? v.true_type === 200 : v.predict_type === 200)
          break
        default:
          this.renderData = this.imgInfo.cells
          break
      }
      setTimeout(() => {
        this.renderLabel(this.renderData)
      }, 200)
    },
    showDialogCheckAll() {
      this.centerDialogVisible = true
      this.all_true_type = this.renderData[0].true_type
    },
    checkedAll() {
      this.updateLoading = true
      this.renderData.map((v, idx) => {
        updatePredict({
          'id': v.id,
          'true_type': parseInt(this.all_true_type)
        }).then(res => {
          if (idx === this.renderData.length - 1) {
            this.filterSearch()
            this.imgCellsInfo.imgcellsall = res.data.data.imgcellsall
            this.imgCellsInfo.imgcellsverified = res.data.data.imgcellsverified
            this.imgCellsInfo.cellsall = res.data.data.cellsall
            this.imgCellsInfo.cellsverified = res.data.data.cellsverified
            this.$message({
              message: '一键审核修改成功',
              type: 'success'
            })
            this.updateLoading = false
            this.centerDialogVisible = false
          }
        })
      })
    },
    closeDialog() {
      this.all_true_type = 100
      this.all_tf = '正确'
    },
    updatePredict(value) {
      if (value.length === 1 && (value[0] === 50 || value[0] === 51)) {
        this.$alert('请选择到二级目录（细胞类型）')
        return
      }
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
      localStorage.setItem('FOV_IMG', JSON.stringify(v))
      localStorage.setItem('FOV_IMG_INDEX', idx)
      this.fov_img = v
      this.selectFov = idx
      this.getPredictResult2(v.id, 999, 0, this.filterValue.filterChecked)
    },
    onSelect(data) {
      this.select = data
      // document.querySelector(`#anchor-${data.id}`).scrollIntoView(true)
    },
    getPredictResult(limit, skip, correct) {
      getPredictResult({ 'id': this.$route.query.pid, 'limit': limit, 'skip': skip, 'correct': correct }).then(res => {
        this.rightCellsList = []
        this.falseCellsList = []
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
      getPredictResult2({ 'pid': this.$route.query.pid, 'iid': iid, 'limit': limit, 'skip': skip, 'status': status }).then(res => {
        this.imgInfo = res.data.data
        this.imgInfo.cells.map((v, idx) => {
          v.tag = `${v.imgid}-${v.status === 1 ? v.true_type : v.predict_type}`
          // v.tagName = v.status === 1 ? v.true_type : v.predict_type
          v.tagName = ''
          v.position = {
            x: parseFloat(v.x1 / this.fov_img.w) * 100 + '%',
            x1: parseFloat(v.x2 / this.fov_img.w) * 100 + '%',
            y: parseFloat(v.y1 / this.fov_img.h) * 100 + '%',
            y1: parseFloat(v.y2 / this.fov_img.h) * 100 + '%'
          }
          v.uuid = v.id
        })
        this.imgCellsInfo = this.imgInfo.info
        this.filterCellsType()
      })
    },
    getDatasetImgs(did) {
      getDatasetImgs({ 'did': this.$route.query.did }).then(res => {
        this.orgImgList = res.data.data.images
        this.total = res.data.data.total
        if (this.orgImgList.length) {
          // const fovImg = JSON.parse(localStorage.getItem('FOV_IMG'))
          // const fovImgIdx = localStorage.getItem('FOV_IMG_INDEX')
          // this.fov_img = fovImg.id ? fovImg : this.orgImgList[0]
          // this.selectFov = fovImgIdx

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
            this.getPredictResult(this.currentPageSize, this.currentPage, 1)
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
      }, 2000)
    },
    changeCellTypes(val) {
      this.postCelltypes = val
    },
    renderLabel(cells, select) {
      this.select = {}
      this.$refs['aiPanel-editor'].getMarker().clearData()
      if (cells.length) {
        this.select = cells[cells.length - 1]
        console.log(this.select)
        this.$refs['aiPanel-editor'].getMarker().renderData(cells)
      }
      // if (!select && cells.length) {
      //   this.select = cells[cells.length - 1]
      //   this.$nextTick(() => {
      //     document.querySelector(`#anchor-${this.select.id}`).scrollIntoView(true)
      //   })
      // }
    }
  }
}
</script>

<style lang="scss" scoped>
.img-tab {
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
}
.tools-bar {
  width: 1310px;
  justify-content: space-between;
  margin-left: 7px;
  span {
    font-size: 14px;
  }
}
.predict {
  .img-div {
    justify-content: flex-start;
    flex-wrap: wrap;
    .label-img {
      justify-content: flex-start;
    }
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
    .check-icon {
      position: absolute;
      top: 0;
      right: 0;
    }
  }
  .select-fov {
    background: rgb(0, 255, 81);
  }
  .results {
    padding: 7px;
    .checked-all {
      margin-bottom: 10px;
    }
    .item-box-select {
      padding: 10px 10px;
      border-bottom: 1px solid #ccc;
      background: rgba(207, 207, 207, 0.5);
    }
    .img-item {
      border: 1px solid #ccc;
      // margin-right: 10px;
      // margin-bottom: 10px;
    }
    .img-select {
      border: 2px solid rgb(0, 255, 81);
    }
    .img-right {
      border: 2px solid rgb(0, 255, 81);
      border-radius: 5px;
    }
    .img-false {
      border: 2px solid rgb(0, 255, 81);
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
