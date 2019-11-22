<template>
  <div class="images">
    <!-- <section class="header flex">
      <el-badge is-dot class="badge">裁剪进度</el-badge>
      <el-progress
        class="progress"
        :text-inside="true"
        :stroke-width="26"
        :percentage="percentage"
        status="success"
      />
    </section> -->
    <section class="main">
      <section class="info-box">
        <el-table :data="tableData" stripe border style="width: 100%">
          <el-table-column prop="name" label="类型" />
          <el-table-column prop="dir" label="目录" />
          <el-table-column label="批次" width="180">
            <template slot-scope="scope">{{ scope.row.batchids }}</template>
          </el-table-column>
          <el-table-column label="病例" width="180">
            <template slot-scope="scope">{{ scope.row.medicalids }}</template>
          </el-table-column>
          <el-table-column prop="fovcnt" label="图片总数" />
          <el-table-column prop="fovncnt" label="fov-n个数" />
          <el-table-column prop="fovpcnt" label="fov-p个数" />
          <el-table-column prop="labelcnt" label="标记次数或输出细胞个数" />
          <el-table-column prop="labelncnt" label="n标记次数或输出细胞个数" />
          <el-table-column prop="labelpcnt" label="p标记次数或输出细胞个数" />
          <!-- <el-table-column prop="types" label="细胞类型"></el-table-column> -->
        </el-table>
      </section>
      <el-tabs
        v-loading="loading"
        :element-loading-text="loadingtext"
        tab-position="left"
        class="img-tabs"
        @tab-click="tabClick"
      >
        <el-tab-pane label="原图">
          <div class="img-div" style="overflow-y: auto;height:600px;">
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
            细胞图
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
        <!-- <el-tab-pane label="细胞核图">
          <el-image
            v-for="(img,idx) in cells_crop_masked"
            :key="idx"
            class="img"
            :src="hosturlpath32 + img"
            lazy
          >
            <div slot="error" class="image-slot">
              <i class="el-icon-picture-outline" />
            </div>
          </el-image>
        </el-tab-pane>-->
        <el-tab-pane label="Log">
          <el-input
            v-model="cLog"
            type="textarea"
            :rows="2"
            placeholder="裁剪log"
            :autosize="{ minRows: 2, maxRows: 16}"
            readonly
          >1</el-input>
        </el-tab-pane>
      </el-tabs>
    </section>
  </div>
</template>

<script>
import { getjobresult, getPercent, getjoblog, downloadImgs } from '@/api/cervical'
import { APIUrl } from '@/const/config'
let timer

export default {
  name: 'Images',
  components: {},
  data() {
    return {
      percentage: 0,
      ETA: 10,
      status: 0,
      loadingtext: '正在执行',
      loading: true,
      dir: 'dsEoM8RR/',
      hosturlpath32: APIUrl + '/imgs/',
      hosturlpath100: APIUrl + '/imgs/',
      tableData: [],
      objData: { 'name': '输入信息' },
      objData2: { 'name': '输出信息' },
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
  methods: {
    downloadImgs() {
      this.downloadLoading = true
      downloadImgs({ 'id': this.$route.query.did }).then(res => {
        console.log(res)
        const blob = new Blob([res.data])
        if (window.navigator.msSaveOrOpenBlob) {
          navigator.msSaveBlob(blob, 'nb')
        } else {
          const link = document.createElement('a')
          const evt = document.createEvent('HTMLEvents')
          evt.initEvent('click', false, false)
          link.href = URL.createObjectURL(blob)
          link.download = '细胞图.zip'
          link.style.display = 'none'
          document.body.appendChild(link)
          link.click()
          window.URL.revokeObjectURL(link.href)
        }
        this.$message({
          message: '下载成功',
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
        if ((this.percentage === 100) || (this.status >= 3) || (this.ETA === 0)) {
          this.loading = false
          this.getjobresult()
          this.getjoblog()
          clearInterval(timer)
        } else {
          this.loadingtext = '预计还需要' + this.ETA + '秒'
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
    },
    /**
     * 定时器轮训百分比
     */
    loopGetPercent() {
      timer = setInterval(() => {
        this.getPercent()
        if ((this.percentage === 100) || (this.status >= 3) || (this.ETA === 0)) {
          this.getjobresult()
          this.getPercent()
          this.getjoblog()
          location.reload()
          clearInterval(timer)
        }
      }, 1500)
    }
  },
  beforedestroy() {
    clearInterval(timer)
  }
}
</script>

<style lang="scss" scoped>
.images {
}
.download {
  color: #000;
  :hover {
    color: #00c764;
  }
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
