<template>
  <div class="temps">
    <section v-if="imgInfo.w" class="label-img flex">
      <AIMarker
        ref="aiPanel-editor"
        class="ai-observer"
        :style="{width: imgInfo.w < 850 ? imgInfo.w + 'px' : 850 + 'px',height: imgInfo.w < 850 ? imgInfo.h + 'px' : (imgInfo.h*(850/imgInfo.w)) + 'px'}"
        :read="readOnly"
        :img="hosturlpath64 + imgInfo.imgpath + '?width=850'"
      />
      <el-badge
        :value="`${imgInfo.predict_type}`"
        type="info"
        class="item"
      >
        <el-image
          class="img-item img-right"
          :src="hosturlpath64 + imgInfo.cellpath + '?width=200'"
        />
      </el-badge>
      <el-radio-group v-model="true_type" class="list">
        <el-radio v-for="(cell, idx) in cellsType" :key="idx" :label="idx" class="item">{{ cell }}</el-radio>
        <el-button type="primary" :disabled="!true_type" @click="updateLabelReview">确定</el-button>
        <el-link type="info" disabled style="margin-left: 10px;">剩余 {{ fov_img.total }} 个</el-link>
      </el-radio-group>
    </section>
    <section v-else class="flex">
      已审核完成，暂无其他审核任务...
    </section>
    <!-- <canvas id="myCanvas" ref="myCanvas" /> -->
  </div>
</template>

<script>
import { APIUrl } from '@/const/config'
import { getLabelReviews, updateLabelReview } from '@/api/cervical'
import { cellsType } from '@/const/const'
import { AIMarker } from '@/components/vue-picture-bd-marker/label.js'

export default {
  name: 'Temps',
  components: { AIMarker },
  data() {
    return {
      true_type: '',
      readOnly: true,
      cellsType: cellsType,
      hosturlpath64: APIUrl + '/imgs/',
      imgInfo: {
        imgpath: '',
        cellpath: ''
      },
      skip: 0,
      fov_img: []
    }
  },
  created() {
    this.getLabelReviews(1, this.skip, 0)
  },
  // mounted() {
  //   const canvas = this.$refs.myCanvas
  //   const ctx = canvas.getContext('2d')
  //   ctx.moveTo(100, 100)
  //   ctx.lineTo(200, 100)
  //   ctx.stroke()
  // },
  methods: {
    getLabelReviews(limit, skip, status) {
      getLabelReviews({ limit: limit, skip: skip, status: status }).then(res => {
        this.fov_img = res.data.data
        if (this.fov_img.reviews.length) {
          this.fov_img.reviews.map(v => {
            v.tagName = ''
            v.position = {
              x: parseFloat(v.x1 / v.w) * 100 + '%',
              x1: parseFloat(v.x2 / v.w) * 100 + '%',
              y: parseFloat(v.y1 / v.h) * 100 + '%',
              y1: parseFloat(v.y2 / v.h) * 100 + '%'
            }
          })
          this.imgInfo = this.fov_img.reviews[0]
          setTimeout(() => {
            this.renderLabel(this.fov_img.reviews)
          }, 200)
        } else {
          this.imgInfo = {
            imgpath: '',
            cellpath: ''
          }
        }
      })
    },
    updateLabelReview() {
      updateLabelReview({
        id: this.imgInfo.id,
        true_type: parseInt(this.true_type.split(' ')[0])
      }).then(res => {
        this.true_type = ''
        this.imgInfo = {
          imgpath: '',
          cellpath: ''
        }
        this.getLabelReviews(1, this.skip++, 0)
        this.$message({
          message: '审核确认成功',
          type: 'success'
        })
      })
    },
    renderLabel(cells) {
      this.$refs['aiPanel-editor'].getMarker().clearData()
      this.$refs['aiPanel-editor'].getMarker().renderData(cells)
    }
  }
}
</script>

<style lang="scss" scoped>
.temps {
  .mycanvas {
    width: 100px;
    height: 100px;
    position: absolute;
    z-index: 999;
  }
  .ai-observer {
    position: relative;
    border: 2px solid rgb(0, 255, 81);
    border-radius: 5px;
  }
  .label-img {
    justify-content: space-around;
  }
  .list {
    display: block;
    border: 1px dashed #ccc;
    padding: 10px 20px;
    .item {
      display: block;
      margin: 7px 0;
      font-size: 24px;
    }
  }
  .img-item {
    border: 1px solid #ccc;
  }
  .img-right {
    border: 2px solid rgb(0, 255, 81);
    border-radius: 5px;
  }
}
</style>
