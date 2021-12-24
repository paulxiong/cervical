<template>
  <div class="images">
    <section class="main">
      <section class="info-box">
        <el-table :data="tableData" stripe border style="width: 100%">
          <el-table-column prop="name" :label="$t('workspace.dataType')" />
          <el-table-column prop="dir" :label="$t('workspace.dataDir')" />
          <el-table-column :label="$t('workspace.dataBatch2')" width="180">
            <template slot-scope="scope">{{ scope.row.batchids }}</template>
          </el-table-column>
          <el-table-column :label="$t('workspace.dataCase2')" width="180">
            <template slot-scope="scope">{{ scope.row.medicalids }}</template>
          </el-table-column>
          <el-table-column prop="fovcnt" :label="$t('workspace.dataNumberImage')" />
          <el-table-column prop="fovncnt" :label="$t('workspace.dataNumberN')" />
          <el-table-column prop="fovpcnt" :label="$t('workspace.dataNumberP')" />
          <el-table-column prop="labelcnt" :label="$t('workspace.dataNumberLabels')" />
          <el-table-column prop="labelncnt" :label="$t('workspace.dataNumberNLabels')" />
          <el-table-column prop="labelpcnt" :label="$t('workspace.dataNumberPLabels')" />
        </el-table>
      </section>
      <el-tabs
        v-loading="loading"
        :element-loading-text="loadingtext"
        tab-position="left"
        class="img-tabs"
        @tab-click="tabClick"
      >
        <el-tab-pane :label="$t('workspace.dataOriginalImage')">
          <div class="img-div" style="overflow-y: auto;height:500px;">
            <el-image
              v-for="(img,idx) in origin_imgs"
              :key="idx"
              class="img"
              :src="hosturlpath100 + img + '?width=100'"
              lazy
            >
              <div slot="error" class="image-slot">
                <i class="el-icon-picture-outline" />
              </div>
            </el-image>
          </div>
          <el-pagination
            v-if="total2"
            class="page"
            :current-page.sync="currentPage2"
            :page-sizes="[10, 20, 50, 100, 200]"
            :page-size="currentPageSize2"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total2"
            @current-change="handleCurrentChange2"
            @size-change="handleSizeChange2"
          />
        </el-tab-pane>
        <el-tab-pane style="overflow: scroll;">
          <span slot="label">
            {{ $t('workspace.dataCells') }}
            <i v-if="downloadLoading" class="el-icon-loading" />
            <svg-icon v-else class="download" icon-class="download" @click="downloadImgs" />
          </span>
          <div class="img-div" style="overflow-y: auto;height:600px;">
            <el-image
              v-for="(img,idx) in cells_crop"
              :key="idx"
              class="img"
              :src="hosturlpath32 + img + '?width=32'"
              lazy
            >
              <div slot="error" class="image-slot">
                <i class="el-icon-picture-outline" />
              </div>
            </el-image>
          </div>
          <el-pagination
            v-if="total"
            class="page"
            :current-page.sync="currentPage"
            :page-sizes="[500, 1000, 2000, 5000]"
            :page-size="currentPageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total"
            @current-change="handleCurrentChange"
            @size-change="handleSizeChange"
          />
        </el-tab-pane>
        <el-tab-pane :label="$t('workspace.dataSegmentationLog')">
          <el-input
            v-model="cLog"
            type="textarea"
            :rows="2"
            placeholder="log"
            :autosize="{ minRows: 2, maxRows: 16}"
            readonly
          >1</el-input>
        </el-tab-pane>
      </el-tabs>
    </section>
          <p> boostx </p>
          <B_zumly ref="Z" :msg_inB="hosturlpath100 + origin_imgs[0] + '?width=300'"/>
  </div>


</template>

<script>
import { getjobresult, getPercent, getjoblog, downloadImgs } from '@/api/cervical'
import { APIUrl } from '@/const/config'
import B_zumly from './components/zumly.vue'
let timer

export default {
  name: 'Images',
  components: {},
  components: {B_zumly},
  data() {
    return {
      percentage: 0,
      ETA: 10,
      status: 0,
      loadingtext: this.$t('workspace.dataInProgress'),
      loading: true,
      dir: 'dsEoM8RR/',
      hosturlpath32: APIUrl + '/imgs/',
      hosturlpath100: APIUrl + '/imgs/',
      tableData: [],
      objData: { 'name': this.$t('workspace.dataInputInformation') },
      objData2: { 'name': this.$t('workspace.dataOutputInformation') },
      cLog: '',
      origin_imgs: [],
      cells_crop: [],
      downloadLoading: false,
      currentPage: 1,
      currentPage2: 1,
      total: 1,
      total2: 1,
      currentPageSize: 500,
      currentPageSize2: 100,
      cells_crop_masked: []
    }
  },
  created() {
    this.loopGetPercent()
  },
  beforeDestroy() {
    clearInterval(timer)
  },
  methods: {
    downloadImgs() {
      this.downloadLoading = true
      this.$alert(`${this.$t('workspace.dataDownloadAlert')}${parseFloat(this.total * 20 / 1024).toFixed(1)}`, {
        confirmButtonText: this.$t('workspace.dataDownloadConfirm')
      })
      downloadImgs({ 'id': this.$route.query.did }).then(res => {
        const blob = new Blob([res.data])
        if (window.navigator.msSaveOrOpenBlob) {
          navigator.msSaveBlob(blob, 'nb')
        } else {
          const link = document.createElement('a')
          const evt = document.createEvent('HTMLEvents')
          evt.initEvent('click', false, false)
          link.href = URL.createObjectURL(blob)
          link.download = this.$t('workspace.dataDownloadZip')
          link.style.display = 'none'
          document.body.appendChild(link)
          link.click()
          window.URL.revokeObjectURL(link.href)
        }
        this.$message({
          message: this.$t('workspace.dataDownloadSucc'),
          type: 'success'
        })
        this.downloadLoading = false
      })
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.getjobresult2()
      this.$nextTick(() => {
        this.cells_crop = this.objData2.cells_crop
      })
    },
    handleSizeChange(val) {
      this.currentPageSize = val
      this.getjobresult2()
      this.$nextTick(() => {
        this.cells_crop = this.objData2.cells_crop
      })
    },
    handleCurrentChange2(val) {
      this.currentPage2 = val
      this.getjobresult2()
      this.$nextTick(() => {
        this.origin_imgs = this.objData2.origin_imgs
      })
    },
    handleSizeChange2(val) {
      this.currentPageSize2 = val
      this.getjobresult2()
      this.$nextTick(() => {
        this.origin_imgs = this.objData2.origin_imgs
      })
    },
    getjobresult2() {
      getjobresult({ did: this.$route.query.did, done: '1', limit: this.currentPageSize, skip: (this.currentPage - 1) * this.currentPageSize, limit2: this.currentPageSize2, skip2: (this.currentPage2 - 1) * this.currentPageSize2 }).then(res => {
        this.objData2 = Object.assign(this.objData2, res.data.data)
        this.origin_imgs = this.objData2.origin_imgs
      })
    },
    getjobresult() {
      // 异步任务改为同步,数组去重复
      getjobresult({ did: this.$route.query.did, done: '0' }).then(res => {
        this.objData = Object.assign(this.objData, res.data.data)
        this.objData.batchids = Array.from(new Set(this.objData.batchids))
        this.objData.medicalids = Array.from(new Set(this.objData.medicalids))
        getjobresult({ did: this.$route.query.did, done: '1', limit: this.currentPageSize, skip: (this.currentPage - 1) * this.currentPageSize, limit2: this.currentPageSize2, skip2: (this.currentPage2 - 1) * this.currentPageSize2 }).then(res => {
          this.objData2 = Object.assign(this.objData2, res.data.data)
          this.objData2.batchids = Array.from(new Set(this.objData2.batchids))
          this.objData2.medicalids = Array.from(new Set(this.objData2.medicalids))
          this.tableData = []
          this.tableData.push(this.objData, this.objData2)
          this.origin_imgs = this.objData2.origin_imgs
          this.total = this.objData2.cells_total
          this.total2 = this.objData2.origin_total
        })
      })
    },
    getPercent() {
      // type 0 未知 1 数据集处理 2 训练 3 预测
      getPercent({ id: this.$route.query.did, type: 1 }).then(res => {
        this.percentage = res.data.data.percent
        this.ETA = res.data.data.ETA
        this.status = res.data.data.status
        if (this.status >= 3) {
          this.loading = false
          clearInterval(timer)
          if ((this.percentage === 100) || (this.ETA === 0)) {
            this.getjobresult()
            this.getjoblog()
          }
        } else {
          this.loadingtext = this.$t('workspace.dataETA') + this.ETA
        }
      })
    },
    getjoblog() {
      // type 0 未知 1 数据集处理 2 训练 3 预测
      getjoblog({ id: this.$route.query.did, type: '1' }).then(res => {
        this.cLog = res.data.data
      })
    },
    /**
     * 切换展示时，为数组赋值
     */
    tabClick(tab, evt) {
      switch (tab.index) {
        case '0':
          this.origin_imgs = this.objData2.origin_imgs
          break
        case '1':
          this.cells_crop = this.objData2.cells_crop
          break
      }
      this.$refs.Z.method1()

    },
    /**
     * 定时器轮训百分比
     */
    loopGetPercent() {
      timer = setInterval(() => {
        this.getPercent()
      }, 2000)
    }
  }
}
</script>

<style lang="scss" scoped>
.download {
  font-size: 24px;
  margin-left: 10px;
  color: #000;
  :hover {
    color: #00c764;
  }
}
/deep/ .el-image__inner {
  margin-right: 10px;
}
.time-info {
  margin-left: 30px;
}
.progress-info {
  margin-bottom: 20px;
}
.info-box {
  justify-content: flex-start;
  align-items: flex-start;
  flex-wrap: wrap;
  margin: 7px 0;
  .info-list {
    justify-content: flex-start;
    flex-wrap: wrap;
  }
  .badge {
    font-weight: bold;
    margin-bottom: 5px;
  }
  i {
    color: #666;
    font-size: 14px;
  }
  span {
    margin-right: 16px;
  }
}
.header {
  border: 1px solid #ccc;
  background: #304155;
  width: 100%;
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
    width: 75%;
    margin: 0 30px 0 10px;
  }
}
.main {
  padding: 0 30px;
  position: relative;
  .img {
    border: 1px solid #ccc;
    margin-right: 2px;
    border-radius: 5px;
  }
}
</style>
