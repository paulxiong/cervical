<template>
  <div class="img-content">
    <div class="img-div flex">
      <div v-for="img in cellsList" :key="img.id" class="img-box">
        <el-image
          :class="img.id == selectedcell.id ? 'img-clicked' : 'img'"
          :src="img.cellpath + '?width=' + cellWidth"
          @click="imgclicked(img)"
        >
          <div slot="error" class="image-slot">
            <i class="el-icon-picture-outline" />
          </div>
        </el-image>
        <svg-icon style="width:15px;height:15px;" class="check-icon" :icon-class="img.status === 1 ? 'checked' : img.status === 2 ? 'delete' : img.status === 3 ? 'adminA' : 'unchecked'" />
      </div>
    </div>
    <div class="flex">
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
    <el-divider content-position="left"><el-radio v-model="cellRadio" :label="50">阴性</el-radio></el-divider>
    <el-radio-group v-model="cellRadio" size="mini" class="radio-box">
      <el-radio v-for="cell of cellsOptions" :key="cell.value" :label="cell.value" border style="margin:0 6px 3px 0;">
        {{ cell.label }}
      </el-radio>
    </el-radio-group>
    <el-divider content-position="left"><el-radio v-model="cellRadio" :label="51">阳性</el-radio></el-divider>
    <el-radio-group v-model="cellRadio" size="mini" class="radio-box">
      <el-radio v-for="cell of cellsOptions2" :key="cell.value" :label="cell.value" border style="margin:0 6px 3px 0;">
        {{ cell.label }}
      </el-radio>
    </el-radio-group>
    <el-divider content-position="left">其他</el-divider>
    <el-radio-group v-model="cellRadio" size="mini" class="radio-box">
      <el-radio v-for="cell of cellsOptions3" :key="cell.value" :label="cell.value" border style="margin:0 6px 3px 0;">
        {{ cell.label }}
      </el-radio>
    </el-radio-group>

    <div class="btn-box">
      <el-divider content-position="center">医生复核区</el-divider>
      <el-button icon="el-icon-check" type="success" style="width:100%;" @click="confirmclicked">确认复核</el-button>
    </div>
  </div>
</template>

<script>
import { getPredictsByPID2, updateLabelReview } from '@/api/cervical'
import { cellsOptions, cellsOptions2, cellsOptions3 } from '@/const/const'
import { medicalURL } from '@/api/filesimages'

export default {
  data() {
    return {
      cellsOptions: cellsOptions,
      cellsOptions2: cellsOptions2,
      cellsOptions3: cellsOptions3,
      cellRadio: 100,
      cellsList: [],
      total: 0,
      currentPage: 1,
      currentPageSize: 10,
      cellWidth: 36,
      selectedcell: { id: 0 }, // 随便初始化一个值，防止页面报错
      reviewed: 0, // 已经审核的个数
      notreviewed: 0 // 没有审核的个数
    }
  },
  created() {
    this.cellWidth = window.innerHeight <= 769 ? 38 : window.innerHeight <= 939 ? 66 : 80
    this.getPredictsByPID2(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, this.$route.query.pid, 0, 51)
  },
  mounted() {
    this.$nextTick(() => {
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
    })
  },
  methods: {
    getPredictsByPID2(limit, skip, pid, status, type) {
      // status 0 未审核 1 已审核 2 移除 3 管理员确认 4 全部
      getPredictsByPID2({ 'limit': limit, 'skip': skip, 'pid': pid, 'status': status, 'type': type, 'order': 1 }).then(res => {
        res.data.data.predicts.map(v => {
          v.cellpath = medicalURL.cellPath(v.cellpath)
        })
        res.data.data.predicts
        this.cellsList = res.data.data.predicts
        this.total = res.data.data.total
        this.updateLocalCellsList(-1, -1) // 只是发送一下审核进度给父组件
      })
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.getPredictsByPID2(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, this.$route.query.pid, 0, 51)
    },
    handleSizeChange(val) {
      this.currentPageSize = val
      this.getPredictsByPID2(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, this.$route.query.pid, 0, 51)
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
