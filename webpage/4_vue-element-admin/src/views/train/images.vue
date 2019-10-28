<template>
  <div class="images">
    <section class="header flex">
      <el-badge is-dot class="badge">裁剪进度</el-badge>
      <el-progress
        class="progress"
        :text-inside="true"
        :stroke-width="26"
        :percentage="percentage"
        status="success"
      />
    </section>
    <section class="main">
      <section class="info-box">
        <el-table :data="tableData" stripe border style="width: 100%">
          <el-table-column prop="name" label="类型" />
          <el-table-column prop="dir" label="目录" />
          <el-table-column prop="batchids" label="批次" />
          <el-table-column prop="medicalids" label="病例" width="180" />
          <el-table-column prop="fovcnt" label="图片总数" />
          <el-table-column prop="fovncnt" label="fov-n个数" />
          <el-table-column prop="fovpcnt" label="fov-p个数" />
          <el-table-column prop="labelcnt" label="标记次数或输出细胞个数" />
          <el-table-column prop="labelncnt" label="n标记次数或输出细胞个数" />
          <el-table-column prop="labelpcnt" label="p标记次数或输出细胞个数" />
          <!-- <el-table-column prop="types" label="细胞类型"></el-table-column> -->
        </el-table>
      </section>
      <el-tabs v-loading="loading" tab-position="left" class="img-tabs" @tab-click="tabClick">
        <el-tab-pane label="原图">
          <el-image
            v-for="(img,idx) in origin_imgs"
            :key="idx"
            class="img"
            :src="hosturlpath100 + img"
            lazy
          >
            <div slot="error" class="image-slot">
              <i class="el-icon-picture-outline" />
            </div>
          </el-image>
        </el-tab-pane>
        <el-tab-pane label="细胞图">
          <el-image
            v-for="(img,idx) in cells_crop"
            :key="idx"
            class="img"
            :src="hosturlpath32 + img"
            lazy
          >
            <div slot="error" class="image-slot">
              <i class="el-icon-picture-outline" />
            </div>
          </el-image>
        </el-tab-pane>
        <el-tab-pane label="细胞核图">
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
        </el-tab-pane>
        <el-tab-pane label="图片处理log">
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
import { getjobresult, getPercent, getjoblog } from '@/api/cervical'
import { ImgServerUrl } from '@/const/config'
let timer

export default {
  name: 'Images',
  components: {},
  data() {
    return {
      percentage: 0,
      loading: true,
      dir: 'dsEoM8RR/',
      hosturlpath32: ImgServerUrl + '/unsafe/32x0/scratch/',
      hosturlpath100: ImgServerUrl + '/unsafe/100x0/scratch/',
      hosturlpath200: ImgServerUrl + '/unsafe/200x0/scratch/',
      hosturlpath645: ImgServerUrl + '/unsafe/645x0/scratch/',
      tableData: [],
      objData: { 'name': '输入信息' },
      objData2: { 'name': '输出信息' },
      cLog: '',
      origin_imgs: [],
      cells_crop: [],
      cells_crop_masked: []
    }
  },
  created() {
    this.getjobresult()
    this.getPercent()
    this.getjoblog()
    this.loopGetPercent()
  },
  methods: {
    getjobresult() {
      // 异步任务改为同步
      getjobresult({ id: this.$route.query.id, done: '0' }).then(res => {
        this.objData = Object.assign(this.objData, res.data.data)
        getjobresult({ id: this.$route.query.id, done: '1' }).then(res => {
          this.objData2 = Object.assign(this.objData2, res.data.data)
          this.tableData.push(this.objData, this.objData2)
          this.origin_imgs = this.objData.origin_imgs
          localStorage.setItem('jobResult', JSON.stringify(this.objData2))
        })
      })
    },
    getPercent() {
      getPercent({ id: this.$route.query.id, job: 0 }).then(res => {
        this.percentage = res.data.data
        if (this.percentage === 100) {
          this.loading = false
          clearInterval(timer)
        }
        this.finishedImages()
      })
    },
    getjoblog() {
      getjoblog({ id: this.$route.query.id, type: 'c' }).then(res => {
        this.cLog = res.data.data
      })
    },
    /**
     * 切换展示时，为数组赋值
     */
    tabClick(tab, evt) {
      switch (tab.index) {
        case '0':
          this.origin_imgs = this.objData.origin_imgs
          break
        case '1':
          this.cells_crop = this.objData.cells_crop
          break
        case '2':
          this.cells_crop_masked = this.objData.cells_crop_masked
          break
      }
    },
    /**
     * 父组件的图片状态更新为已完成
     */
    finishedImages() {
      this.$emit('finished', this.percentage)
    },
    /**
     * 定时器轮训百分比
     */
    loopGetPercent() {
      timer = setInterval(() => {
        this.getPercent()
        if (this.percentage === 100) {
          this.getjobresult()
          this.getPercent()
          this.getjoblog()
          clearInterval(timer)
        }
      }, 1e4)
    }
  },
  beforedestroy() {
    clearInterval(timer)
  }
}
</script>

<style lang="scss" scoped>
.images {
  margin-bottom: 100px;
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
  margin: 20px 0;
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
