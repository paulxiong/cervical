<template>
  <div class="img-content">
    <div>
      <el-divider content-position="left">{{ $t('label.details') }}</el-divider>
      <div class="img-div">
        <div v-for="img in labelList" :key="img.labelid" class="img-box">
          <el-image
            :class="img.labelid == selectedcell.labelid ? 'img-clicked' : 'img'"
            :src="img.cellpath"
            @click="imgclicked(img)"
          >
            <div slot="error" class="image-slot">
              <i class="el-icon-picture-outline" />
            </div>
          </el-image>
          <svg-icon style="width:15px;height:15px;" class="check-icon" :icon-class="img.status === 1 ? 'checked' : img.status === 2 ? 'delete' : img.status === 3 ? 'adminA' : 'unchecked'" />
        </div>
      </div>
    </div>
    <div class="pagination-container1">
      <el-pagination
        v-if="total"
        small
        layout="total, prev, pager, next"
        :current-page.sync="currentPage"
        :page-size="currentPageSize"
        :total="total"
        @current-change="handleCurrentChange"
        @size-change="handleSizeChange"
      />
    </div>
    <div>
      <el-divider content-position="left">{{ $t('label.operation2') }}</el-divider>
      <!--
      <div id='radio'>
        <el-radio-group v-model="radio1"   @change="Radio1valueChange" border>
          <el-radio-button label="start_label">{{ $t('label.label2') }}</el-radio-button>
          <el-radio-button label="end_label">{{ $t('label.exitLabelMode') }}</el-radio-button>
        </el-radio-group>
      </div>
      -->
      <div class="btn-box">
        <el-button class="labelbtn" type="success" @click="labelclicked">{{ $t('label.label2') }}</el-button>
        <el-button class="labelbtn" type="success" @click="cancellabelclicked">{{ $t('label.exitLabelMode') }}</el-button>
        <el-button v-if="!imported" :disabled="imported" class="labelbtn" type="success" @click="importclicked">{{ importbuttontext }}</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { getPredictsByPID2, updateLabelReview } from '@/api/cervical'
import { medicalURL } from '@/api/filesimages'
import { fullPosation2Fov } from '@/utils/label'

export default {
  props: {
    scantxt: {
      type: Object,
      default: () => {
        return { }
      }
    }
  },
  data() {
    return {
      importbuttontext: this.$t('label.importSystemAnnotations'),
      imported: false,
      cellRadio: 100,
      total: 0,
      currentPage: 1,
      currentPageSize: 20,
      cellWidth: 80,
      labelList: [],
      labelListAll: [],
      cellsList: [],
      cellsListAll: [],
      selectedcell: { id: 0 }, // 随便初始化一个值，防止页面报错
      reviewed: 0, // 已经审核的个数
      notreviewed: 0, // 没有审核的个数
      tableData: [],
      radio1: 'end_label'
    }
  },
  created() {
    this.getPredictsByPID2All(200, 0, this.$route.query.pid, 0, 51)
  },
  methods: {
    getPredictsByPID2All(limit, skip, pid, status, type) {
      // status 0 未审核 1 已审核 2 移除 3 管理员确认 4 全部
      getPredictsByPID2({ 'limit': limit, 'skip': skip, 'pid': pid, 'status': status, 'type': type, 'order': 1 }).then(res => {
        res.data.data.predicts.map(v => {
          v.cellpath = medicalURL.cellPath(v.cellpath)
        })
        this.cellsListAll = res.data.data.predicts
      })
    },
    _getCellsTable() { // 分页显示
      this.labelList = []
      var _labelList = []
      for (var i = 0; i < this.labelListAll.length; i++) {
        if (_labelList.length >= this.currentPageSize) {
          break
        }
        if (i < (this.currentPage - 1) * this.currentPageSize) {
          continue
        }
        const fov = fullPosation2Fov(this.labelListAll[i], this.scantxt) // 标注在FOV里面的位置
        this.labelListAll[i].cellpath = fov.cellurl
        _labelList.push(this.labelListAll[i])
      }
      this.labelList = _labelList
    },
    updateLabelTable(labeltree) { // 更新列表
      this.labelListAll = []
      var _table = []
      for (var level1 in labeltree) {
        for (var level2 in labeltree[level1]) {
          _table.push(Object.assign({}, labeltree[level1][level2]))
        }
      }
      this.labelListAll = _table.sort(function(a, b) {
        return (b.order - a.order)
      })

      this.total = this.labelListAll.length
      this._getCellsTable() // 取出当前页面需要显示的
    },
    tableRowClassName({ row, rowIndex }) {
      if (rowIndex === 1) {
        return 'warning-row'
      } else if (rowIndex === 3) {
        return 'success-row'
      }
      return ''
    },
    gotofirstcell() {
      if (this.labelList.length > 0) {
        this.imgclicked(this.labelList[0])
      } else {
        const that = this
        setTimeout(() => {
          if (that.labelList.length > 0) {
            that.defaultclicked(that.labelList[0], that)
          }
        }, 1000)
      }
    },
    importedfunc() {
      this.imported = true
      this.importclicked()
    },
    labelclicked() {
      this.$emit('labelclicked')
    },
    Radio1valueChange(val){
      //console.log('boost-debug:radioChange')
      if (val ==='start_label') {
        this.$emit('labelclicked')
      }
      if (val ==='end_label') {
        this.$emit('cancellabelclicked')
      }
    },
    importclicked() {
      if (!this.imported) { // 说明是点按钮触发的
        this.$emit('importpredict', this.cellsListAll)
      }
      this.gotofirstcell() // 系统预测小图预览的第一个细胞
      this.imported = true
      this.importbuttontext = this.$t('label.importedSystemAnnotations')
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this._getCellsTable()
    },
    handleSizeChange(val) {
      this.currentPageSize = val
      this._getCellsTable()
    },
    cancellabelclicked() {
      this.$emit('cancellabelclicked')
    },
    defaultclicked(cell, _this) {
      _this.selectedcell = { ...cell }
      _this.$emit('labelimgclicked', cell)
    },
    imgclicked(cell) {
      this.defaultclicked(cell, this)
    },
    confirmclicked() {
      this.updateLabelReview(this.selectedcell, this.cellRadio)
    },
    updateLabelReview() {
      updateLabelReview({
        id: this.selectedcell.id,
        true_type: this.cellRadio
      }).then(res => {
        this.reviewed = res.data.data.reviewed
        this.notreviewed = res.data.data.notreviewed
        this.updateLocalCellsList(this.selectedcell.id, this.cellRadio)
        this.$message({
          message: this.$t('label.reviewSuccessful'),
          type: 'success'
        })
      })
    },
    updateLocalCellsList(id, _type) {
      this.cellsList.map(v => {
        if (v.id === id) {
          v.status = 1 // status 0 未审核 1 已审核 2 移除 3 管理员确认
          v.true_type = _type
        }
      })
      this.$emit('updatereviewcnt', { reviewed: this.reviewed, notreviewed: this.notreviewed })
    }
  }
}
</script>

<style lang="scss" scoped>
.pagination-container1 {
  text-align: center;
}
.btn-box {
  display: flex;
  .labelbtn {
    width: 100%;
  }
}
.img-div {
  flex-wrap: wrap;
  display: flex;
  justify-content: space-around;
  .img-box {
    position: relative;
    width: 84px;
    height: 88px;
  }
  .img {
    width: 80px;
    height: 80px;
    margin: 2px 2px 2px 2px;
    border-radius: 10%;
    border: 0px solid red;
  }
  .img-clicked {
    width: 84px;
    height: 84px;
    margin: 0 0 0 0;
    border-radius: 10%;
    border: 2px solid red;
  }
  .check-icon {
    position: absolute;
    right: 1px;
    bottom: 3px;
  }
}
/deep/ .el-divider {
  margin-top: 15px;
  margin-bottom: 15px;
}
</style>
