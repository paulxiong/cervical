<template>
  <div class="images">
    <section class="header">
      <div class="title">
        <h2>IMAGES</h2>
        <section class="info-box">
          <div class="input-info info">
            <el-badge is-dot class="badge">输入信息</el-badge>
            <div class="img-list info-list flex">
              <i>目录:</i>
              <span>{{objData.dir}}</span>
              <i>批次:</i>
              <span>{{objData.batchids}}</span>
              <i>病例:</i>
              <span>{{objData.medicalids}}</span>
              <i>图片总数/FOV&nbsp;N个数/FOV&nbsp;P个数:</i>
              <span>{{objData.fovcnt}}/{{objData.fovncnt}}/{{objData.fovpcnt}}</span>
              <i>标记次数/n标记次数/p标记次数:</i>
              <span>{{objData.labelcnt}}/{{objData.labelncnt}}/{{objData.labelpcnt}}</span>
              <i>n/p:</i>
              <span>{{objData.fovncnt}}/{{objData.fovpcnt}}</span>
            </div>
          </div>
          <div class="output-info info">
            <el-badge is-dot class="badge">输出信息</el-badge>
            <div class="img-list info-list flex">
              <i>目录:</i>
              <span>{{objData2.dir}}</span>
              <i>批次:</i>
              <span>{{objData2.batchids}}</span>
              <i>病例:</i>
              <span>{{objData2.medicalids}}</span>
              <i>图片总数/FOV&nbsp;N个数/FOV&nbsp;P个数:</i>
              <span>{{objData2.fovcnt}}/{{objData2.fovncnt}}/{{objData2.fovpcnt}}</span>
              <i>标记次数/n标记次数/p标记次数:</i>
              <span>{{objData2.labelcnt}}/{{objData2.labelncnt}}/{{objData2.labelpcnt}}</span>
              <i>n/p:</i>
              <span>{{objData2.fovncnt}}/{{objData2.fovpcnt}}</span>
            </div>
          </div>
          <div class="progress-info">
            <el-badge is-dot class="badge">状态进度</el-badge>
            <el-progress
              class="progress"
              :text-inside="true"
              :stroke-width="26"
              :percentage="percentage"
              status="success"
            ></el-progress>
          </div>
        </section>
      </div>
    </section>
    <el-divider>
      <i class="el-icon-picture"></i> 所有图片
    </el-divider>
    <section class="main">
      <el-tabs tab-position="left" @tab-click="tabClick">
        <el-tab-pane label="原图">
          <el-image
            class="img"
            v-for="(img,idx) in origin_imgs"
            :key="idx"
            :src="hosturlpath200 + img"
            lazy
          >
            <div slot="error" class="image-slot">
              <i class="el-icon-picture-outline"></i>
            </div>
          </el-image>
        </el-tab-pane>
        <el-tab-pane label="细胞图">
          <el-image
            class="img"
            v-for="(img,idx) in cells_crop"
            :key="idx"
            :src="hosturlpath200 + img"
            lazy
          >
            <div slot="error" class="image-slot">
              <i class="el-icon-picture-outline"></i>
            </div>
          </el-image>
        </el-tab-pane>
        <el-tab-pane label="细胞核图">
          <el-image
            class="img"
            v-for="(img,idx) in cells_crop_masked"
            :key="idx"
            :src="hosturlpath200 + img"
            lazy
          >
            <div slot="error" class="image-slot">
              <i class="el-icon-picture-outline"></i>
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
  name: 'images',
  components: {},
  data() {
    return {
      percentage: 0,
      dir: 'dsEoM8RR/',
      hosturlpath16: ImgServerUrl + '/unsafe/32x0/scratch/',
      hosturlpath64: ImgServerUrl + '/unsafe/640x0/scratch/',
      hosturlpath200: ImgServerUrl + '/unsafe/200x0/scratch/',
      hosturlpath645: ImgServerUrl + '/unsafe/800x0/scratch/',
      objData: {},
      objData2: {},
      cLog: '',
      origin_imgs: [],
      cells_crop: [],
      cells_crop_masked: []
    }
  },
  methods: {
    getjobresult() {
      getjobresult({ id: this.$route.query.id, done: '0' }).then(res => {
        this.objData = res.data.data
        this.origin_imgs = this.objData.origin_imgs
      })
      getjobresult({ id: this.$route.query.id, done: '1' }).then(res => {
        this.objData2 = res.data.data
        localStorage.setItem('cellTypes', JSON.stringify(this.objData2.types || []))
      })
    },
    getPercent() {
      getPercent({ id: this.$route.query.id }).then(res => {
        this.percentage = res.data.data
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
     * 通知父组件的图片状态更新为已完成
     */
    finishedImages() {
      this.$emit('finished', this.percentage)
    },
    /**
     * 定时器轮训百分比
     */
    loopGetPercent() {
      timer = setInterval(() => {
        if (this.percentage === 100) {
          clearInterval(timer)
          this.getjobresult()
        }
        this.getPercent()
      }, 1e4)
    }
  },
  mounted() {
    this.getjobresult()
    this.getPercent()
    this.getjoblog()
    this.loopGetPercent()
  },
  beforedestroy() {
    clearInterval(timer)
  }
}
</script>

<style lang="scss" scoped>
.images {
  padding: 0 30px;
  justify-content: space-between;
}
.output-info {
  margin-top: 20px;
}
.time-info {
  margin-left: 30px;
}
.progress-info {
  margin-top: 20px;
}
.info-box {
  justify-content: flex-start;
  align-items: flex-start;
  flex-wrap: wrap;
  margin-bottom: 10px;
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
  margin-bottom: 30px;
}
.main {
  .img {
    border: 1px solid #ccc;
    margin-right: 2px;
    border-radius: 5px;
  }
}
</style>
