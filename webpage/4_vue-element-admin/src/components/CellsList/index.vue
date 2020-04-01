<template>
  <div class="img-content">
    <div class="img-div flex">
      <div v-for="(img) in cellsList" :key="img.id" class="img-box">
        <el-image
          class="img"
          :src="hosturlpath32 + img.cellpath + '?width=' + cellWidth"
          @click="imgclicked(img)"
        >
          <div slot="error" class="image-slot">
            <i class="el-icon-picture-outline" />
          </div>
        </el-image>
        <svg-icon style="width:15px;height:15px;" class="check-icon" :icon-class="'unchecked'" />
      </div>
    </div>
    <el-pagination
      v-if="total"
      class="page"
      :current-page.sync="currentPage"
      :page-size="currentPageSize"
      layout="total, pager"
      :total="total"
      @current-change="handleCurrentChange"
      @size-change="handleSizeChange"
    />
    <el-divider content-position="left"><el-radio v-model="cellRadio" :label="50">阴性</el-radio></el-divider>
    <el-radio-group v-model="cellRadio" size="mini" class="radio-box">
      <el-radio v-for="cell of cellsOptions" :key="cell.value" :label="cell.value" border style="margin:0 6px 7px 0;">
        {{ cell.label }}
      </el-radio>
    </el-radio-group>
    <el-divider content-position="left"><el-radio v-model="cellRadio" :label="51">阳性</el-radio></el-divider>
    <el-radio-group v-model="cellRadio" size="mini" class="radio-box">
      <el-radio v-for="cell of cellsOptions2" :key="cell.value" :label="cell.value" border style="margin:0 6px 7px 0;">
        {{ cell.label }}
      </el-radio>
    </el-radio-group>
    <el-divider content-position="left">其他</el-divider>
    <el-radio-group v-model="cellRadio" size="mini" class="radio-box">
      <el-radio v-for="cell of cellsOptions3" :key="cell.value" :label="cell.value" border style="margin:0 6px 7px 0;">
        {{ cell.label }}
      </el-radio>
    </el-radio-group>

    <div class="btn-box">
      <el-divider content-position="center">医生复核区</el-divider>
      <el-button icon="el-icon-check" type="success" style="width:100%;">确认复核</el-button>
    </div>
  </div>
</template>

<script>
import { getPredictsByPID2 } from '@/api/cervical'
import { APIUrl } from '@/const/config'
import { cellsOptions, cellsOptions2, cellsOptions3 } from '@/const/const'

export default {
  data() {
    return {
      cellsOptions: cellsOptions,
      cellsOptions2: cellsOptions2,
      cellsOptions3: cellsOptions3,
      cellRadio: 50,
      cellsList: [],
      total: 0,
      currentPage: 1,
      currentPageSize: 10,
      cellWidth: 36,
      hosturlpath32: '' + APIUrl + '/imgs/'
    }
  },
  created() {
    this.cellWidth = window.innerHeight <= 769 ? 35 : window.innerHeight <= 939 ? 74 : 85
    this.getPredictsByPID2(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, this.$route.query.pid)
  },
  // mounted() {
  //   this.$nextTick(() => {
  //     console.log(document.querySelector('.el-tabs__content').getBoundingClientRect())
  //   })
  // },
  methods: {
    getPredictsByPID2(limit, skip, pid) {
      getPredictsByPID2({ 'limit': limit, 'skip': skip, 'pid': pid, 'status': 0, 'type': 51, 'order': 0 }).then(res => {
        this.cellsList = res.data.data.predicts
        this.total = res.data.data.total
      })
    },
    handleCurrentChange(val) {
      this.currentPage = val
    },
    handleSizeChange(val) {
      this.currentPageSize = val
    },
    imgclicked(img) {
      this.$emit('imgclicked', img)
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
  .img {
    margin: 0 2px;
    border-radius: 10%;
    // border-bottom-right-radius: 50%;
  }
  .check-icon {
    position: absolute;
    right: 1px;
    bottom: 3px;
  }
}
/deep/ .el-divider {
  margin-top: 18px;
  margin-bottom: 18px;
}
</style>
