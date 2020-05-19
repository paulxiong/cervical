<template>
  <div class="img-content">
    <div class="img-div">
      <el-divider content-position="left">标注</el-divider>
      <el-table :data="tableData" height="320" highlight-current-row style="width: 100%" @row-click="rowclick">
        <el-table-column prop="shortname" label="缩写" width="85" />
        <el-table-column :show-overflow-tooltip="true" prop="label" label="全称" width="260" />
        <el-table-column prop="typeid" label="状态" />
      </el-table>
    </div>
    <div>
      <el-divider content-position="left">操作</el-divider>
      <div class="btn-box">
        <el-button class="labelbtn" type="success" @click="labelclicked">标注</el-button>
        <el-button class="labelbtn" type="success" @click="cancellabelclicked">退出标注模式</el-button>
        <el-button v-if="!imported" :disabled="imported" class="labelbtn" type="success" @click="importclicked">{{ importbuttontext }}</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { getPredictsByPID2, updateLabelReview } from '@/api/cervical'
import { medicalURL } from '@/api/filesimages'

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
      importbuttontext: '导入系统标注',
      imported: false,
      cellRadio: 100,
      total: 0,
      currentPage: 1,
      currentPageSize: 10,
      cellWidth: 36,
      cellsList: [],
      cellsListAll: [],
      selectedcell: { id: 0 }, // 随便初始化一个值，防止页面报错
      reviewed: 0, // 已经审核的个数
      notreviewed: 0, // 没有审核的个数
      tableData: []
    }
  },
  created() {
    this.cellWidth = window.innerHeight <= 769 ? 38 : window.innerHeight <= 939 ? 66 : 80
    this.getPredictsByPID2All(200, 0, this.$route.query.pid, 0, 51)
  },
  methods: {
    getPredictsByPID2(limit, skip, pid, status, type, cb) {
      // status 0 未审核 1 已审核 2 移除 3 管理员确认 4 全部
      getPredictsByPID2({ 'limit': limit, 'skip': skip, 'pid': pid, 'status': status, 'type': type, 'order': 1 }).then(res => {
        res.data.data.predicts.map(v => {
          v.cellpath = medicalURL.cellPath(v.cellpath)
        })
        this.cellsList = res.data.data.predicts
        this.total = res.data.data.total
        this.updateLocalCellsList(-1, -1) // 只是发送一下审核进度给父组件

        return cb && cb()
      })
    },
    getPredictsByPID2All(limit, skip, pid, status, type) {
      // status 0 未审核 1 已审核 2 移除 3 管理员确认 4 全部
      getPredictsByPID2({ 'limit': limit, 'skip': skip, 'pid': pid, 'status': status, 'type': type, 'order': 1 }).then(res => {
        res.data.data.predicts.map(v => {
          v.cellpath = medicalURL.cellPath(v.cellpath)
        })
        this.cellsListAll = res.data.data.predicts
      })
    },
    rowclick(row, column, event) {
      const x = (row.x1 + row.x2) / 2
      const y = (row.y1 + row.y2) / 2
      this.$emit('gotolatlng', { 'x': x, 'y': y })
    },
    updateLabelTable(labeltree) { // 更新列表
      this.tableData = []
      var _table = []
      for (var level1 in labeltree) {
        for (var level2 in labeltree[level1]) {
          _table.push(labeltree[level1][level2])
        }
      }
      this.tableData = _table
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
      if (this.cellsList.length > 0) {
        this.imgclicked(this.cellsList[0])
      } else {
        const that = this
        setTimeout(() => {
          if (that.cellsList.length > 0) {
            that.defaultclicked(that.cellsList[0], that)
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
    importclicked() {
      this.getPredictsByPID2(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, this.$route.query.pid, 0, 51, f => { // 系统预测小图预览
        if (!this.imported) { // 说明是点按钮触发的
          this.$emit('importpredict', this.cellsListAll)
        }
        this.gotofirstcell() // 系统预测小图预览的第一个细胞
        this.imported = true
        this.importbuttontext = '已导入系统标注'
      })
    },
    cancellabelclicked() {
      this.$emit('cancellabelclicked')
    },
    defaultclicked(cell, _this) {
      _this.selectedcell = { ...cell }
      _this.cellRadio = cell.predict_type
      if (cell.status !== 0) {
        _this.cellRadio = cell.true_type
      }
      _this.$emit('imgclicked', cell)
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
          message: '审核确认成功',
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
.btn-box {
  display: flex;
  .labelbtn {
    width: 45%;
  }
}
.img-div {
  flex-wrap: wrap;
  justify-content: flex-start;
  .img-box {
    position: relative;
  }
  // /deep/ .el-image {
  //   height: 80px;
  // }
  .img {
    margin: 2px 2px 2px 2px;
    border-radius: 10%;
    border: 0px solid red;
  }
  .img-clicked {
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
