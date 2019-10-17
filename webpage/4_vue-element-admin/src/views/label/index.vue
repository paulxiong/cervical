<template>
  <div class="doctor">
    <section class="main flex">
      <h2>选择需要预测的病例号</h2>
      <el-checkbox-group class="checkbox" v-model="checkList">
        <el-tooltip class="item" effect="dark" content="n:p=4:9" placement="bottom">
          <el-checkbox label="1号病例-xxx"></el-checkbox>
        </el-tooltip>
        <el-checkbox label="2号病例-yyy"></el-checkbox>
        <el-checkbox label="3号病例-zzz"></el-checkbox>
      </el-checkbox-group>
      <el-button type="primary" :disabled="started" round @click="startPredict">
        开始预测
        <i v-show="ptg!==100&&started" class="icon el-icon-loading"></i>
      </el-button>
    </section>
    <el-divider>{{ptg===100?'预测结果':ptg+'%'}}</el-divider>
    <section class="result flex">
      <img id="hallstatt" class="img-result" :src="imgResult" />
      <div class="info">图片信息</div>
    </section>
  </div>
</template>

<script>
import { getLabelByImageId } from '@/api/cervical'
// import { setaddAnnotation } from '@/utils/setaddAnnotation'

export default {
  name: 'Doctor',
  components: {},
  data() {
    return {
      ptg: 0,
      started: false,
      checkList: ['1号病例-xxx'],
      imgResult: 'http://dev.medical.raidcdn.cn:3001/unsafe/645x0/img/17P0603/1904852/Images/IMG016x028.JPG',
      imgInfo: {}
    }
  },
  methods: {
    startPredict() {
      this.loopEvent()
      this.setaddAnnotation(this.imgResult, this.imgInfo.labels, this.imgInfo.imgw ? this.imgInfo.imgw / 645 : 3)
      this.started = true
    },
    getLabelByImageId() {
      getLabelByImageId({ 'limit': 100, 'skip': 0, 'imgid': 5 }).then(res => {
        this.imgInfo = res.data.data
      })
    },
    loopEvent() {
      setTimeout(() => {
        this.ptg = 25
      }, 1e3)
      setTimeout(() => {
        this.ptg = 66
      }, 2 * 1e3)
      setTimeout(() => {
        this.ptg = 100
        this.started = false
      }, 3 * 1e3)
    },
    setaddAnnotation(url, labels, divide) {
      window.anno.makeAnnotatable(document.getElementById('hallstatt'))
      window.anno.setProperties({
        outline: 'yellow',
        outline_width: 3,
        hi_outline: 'yellow',
        hi_outline_width: 2,
        stroke: 'yellow'
      })
      // 遍历获取snapshot表里图片头像框坐标信息并等比换算处理到页面上展示
      for (let i = 0; i < labels.length; i++) {
        const annotation = {
          src: url,
          text: labels[i].typeout,
          units: 'pixel',
          editable: true,
          shapes: [
            {
              type: 'rect',
              units: 'pixel',
              geometry: {
                x: parseInt(labels[i].x / divide),
                y: parseInt(labels[i].y / divide),
                width:
                  labels[i].w <= divide ? 1 : parseInt(labels[i].w / divide),
                height:
                  labels[i].h <= divide ? 1 : parseInt(labels[i].h / divide)
              }
            }
          ]
        }
        // 添加头像框到画布里
        window.anno.addAnnotation(annotation)
      }
    }
  },
  mounted() {
    this.getLabelByImageId()
  }
}
</script>

<style lang="scss" scoped>
@import "../../styles/annotorious-dark.css";

.doctor {
  padding-bottom: 100px;
  .main {
    flex-direction: column;
    h2 {
      margin-top: 20px;
      margin-bottom: 10px;
    }
    .checkbox {
      margin-bottom: 10px;
    }
    .icon {
      margin-left: 5px;
    }
  }
  .result {
    justify-content: flex-start;
    flex-wrap: wrap;
  }
}
</style>
