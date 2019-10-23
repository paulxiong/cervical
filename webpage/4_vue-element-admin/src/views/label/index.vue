<template>
  <div class="label flex">
    <section class="main">
      <section class="tools flex">
        <div class="btn-box">
          <el-button size="mini" type="primary">选择导入数据集</el-button>
          <el-button size="mini" type="primary">去训练</el-button>
          <el-button size="mini" type="primary">去预测</el-button>
        </div>
        <el-button-group>
          <el-button size="mini" type="info" icon="el-icon-arrow-left">上一张</el-button>
          <el-button size="mini" type="info">下一张<i class="el-icon-arrow-right el-icon--right" /></el-button>
        </el-button-group>
      </section>
      <section class="label-img">
        <AIMarker
          ref="aiPanel-editor"
          class="ai-observer"
          :img="fov_img"
          @vmarker:onDrawOne="onDrawOne"
        />
      </section>
    </section>
    <section class="info">
      <div class="cells-type">
        <el-divider content-position="left"><el-badge is-dot class="badge-item">请选择细胞标记类型</el-badge></el-divider>
        <el-radio-group v-model="cellType" size="mini" class="list">
          <el-radio v-for="(cell, idx) in cellsType" :key="idx" :label="idx" class="item">{{ cell }}</el-radio>
        </el-radio-group>
      </div>
      <div class="data-info">
        <el-divider content-position="left"><el-badge is-dot class="badge-item">标注记录</el-badge></el-divider>
        <div class="list">
          <div v-for="item in 17" :key="item" class="item" :class="item===activeItem?'active-item':''" @click="activeItem=item">20190523.1807285.N.IMG002x01{{ item }}.JPG</div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { getLabelByImageId } from '@/api/cervical'
import { AIMarker } from '@/components/vue-picture-bd-marker/label.js'
import { cellsType } from '@/const/const'

export default {
  name: 'Label',
  components: { AIMarker },
  data() {
    return {
      cellsType: cellsType,
      activeItem: 1,
      cellType: '1',
      labelLog: [],
      imgInfo: {},
      fov_img: 'http://medical.raidcdn.cn:3001/unsafe/1000x0/scratch/93jeRNKB/origin_imgs/redhouse.1816953.N.IMG018x024.JPG',
      cell_img: 'http://medical.raidcdn.cn:3001/unsafe/100x0/scratch/93jeRNKB/cells/crop/17P0603.1904165A.N.IMG001x020.JPG_n_5_1111_1394_1211_1494.png'
    }
  },
  mounted() {
    this.getLabelByImageId()
  },
  methods: {
    getLabelByImageId() {
      getLabelByImageId({ 'limit': 100, 'skip': 0, 'imgid': 5 }).then(res => {
        this.imgInfo = res.data.data
        this.imgInfo.labels.map(v => {
          v.tag = `${v.imgid}-${v.id}`
          v.tagName = this.cellsType[v.type]
          v.position = {
            x: parseFloat(v.x / this.imgInfo.imgw) * 100 + '%',
            x1: parseFloat(v.x / this.imgInfo.imgw) * 100 + parseFloat(v.h / this.imgInfo.imgh) * 100 + '%',
            y: parseFloat(v.y / this.imgInfo.imgh) * 100 + '%',
            y1: parseFloat(v.y / this.imgInfo.imgh) * 100 + parseFloat(v.h / this.imgInfo.imgh) * 100 + '%'
          }
          v.uuid = v.id
        })
        console.log(this.imgInfo.labels)
        this.renderLabel()
      })
    },
    onDrawOne(data, currentMovement) {
      // this.$refs['aiPanel-editor'].setTag({
      //   tagName: this.cellsType[this.cellType],
      //   tag: this.cellType
      // })
      this.labelLog.push()
    },
    renderLabel() {
      this.$refs['aiPanel-editor'].getMarker().renderData(this.imgInfo.labels)
    }
  }
}
</script>

<style lang="scss" scoped>
.label {
  height: 100%;
  justify-content: space-between;
  align-items: flex-start;
  .main {
    width: 80%;
    height: 100%;
    .tools {
      justify-content: space-between;
      padding: 0 5px;
      margin: 5px 0;
    }
    .label-img {
      max-height: calc(100vh - 90px);
      overflow: hidden;
    }
  }
  .info {
    width: 20%;
    height: 100%;
    .cells-type {
      border: 2px solid #ccc;
      height: 50%;
      overflow: auto;
      padding-left: 5px;
      padding-top: 5px;
      .list {
        display: block;
        .item {
          display: block;
          margin: 5px 0;
        }
      }
    }
    .data-info {
      border: 2px solid #ccc;
      padding-top: 5px;
      .list {
        margin-top: 5px;
        max-height: calc(100vh - 485px);
        overflow: auto;
        .item {
          border-top: 1px solid #000;
          border-bottom: 1px solid #000;
          font-size: 12px;
          padding: 5px;
          cursor: pointer;
        }
        .active-item {
          border-top: 1px solid #0088f9;
          border-bottom: 1px solid #0088f9;
          background: #0088f9;
          color: #fff;
        }
      }
    }
  }
}
</style>
