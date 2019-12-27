<template>
  <div class="temps">
    <section v-if="imgInfo.w" class="label-img flex">
      <AIMarker
        v-if="isPhone"
        ref="aiPanel-editor"
        class="ai-observer"
        :read="readOnly"
        :img="hosturlpath64 + imgInfo.imgpath2"
      />
      <AIMarker
        v-else
        ref="aiPanel-editor"
        class="ai-observer"
        :style="{width: imgInfo.w < 850 ? imgInfo.w + 'px' : 850 + 'px',height: imgInfo.w < 850 ? imgInfo.h + 'px' : (imgInfo.h*(850/imgInfo.w)) + 'px'}"
        :read="readOnly"
        :img="hosturlpath64 + imgInfo.imgpath2"
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
      <el-radio-group v-model="true_type" class="radio-list">
        <el-radio v-for="(cell, idx) in cellsType" :key="idx" :label="idx" class="radio-item">{{ cell }}</el-radio>
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
      isPhone: false,
      hosturlpath64: APIUrl + '/imgs/',
      imgInfo: {
        imgpath: '',
        cellpath: ''
      },
      x1: 0,
      x2: 0,
      y1: 0,
      y2: 0,
      skip: 0,
      fov_img: []
    }
  },
  created() {
    this.getLabelReviews(1, this.skip, 0)
  },
  mounted() {
    console.log(document.body.clientWidth)
    if (document.body.clientWidth < 600) {
      this.isPhone = true
    }
    // const canvas = this.$refs.myCanvas
    // const ctx = canvas.getContext('2d')
    // ctx.moveTo(100, 100)
    // ctx.lineTo(200, 100)
    // ctx.stroke()
  },
  methods: {
    // 计算需要框出来的正方形区域
    calculateSquare(_x1, _x2, _y1, _y2, w, h) {
      const sidehalf = 300 // 边长600
      const cellsidehalf = 50 // 边长600

      const x = parseFloat((_x1 + _x2) / 2)
      const y = parseFloat((_y1 + _y2) / 2)

      // 600x600图片的坐标
      let x1 = x - sidehalf
      let x2 = x + sidehalf
      let y1 = y - sidehalf
      let y2 = y + sidehalf

      // 100x100细胞坐标
      let cellx1 = sidehalf - cellsidehalf
      let celly1 = sidehalf - cellsidehalf
      let cellx2 = sidehalf + cellsidehalf
      let celly2 = sidehalf + cellsidehalf

      // 超出图片的要平移进来
      const deltax = (x1 < 0) ? (0 - x1) : (x2 > w) ? (w - x2) : 0
      const deltay = (y1 < 0) ? (0 - y1) : (y2 > h) ? (h - y2) : 0
      if (deltax !== 0) {
        x1 += deltax
        x2 += deltax
        // 还原细胞坐标
        cellx1 -= deltax
        cellx2 -= deltax
      }
      if (deltay !== 0) {
        y1 += deltay
        y2 += deltay
        celly1 -= deltay
        celly2 -= deltay
      }

      const neww = parseFloat(x2 - x1)
      const newh = parseFloat(y2 - y1)

      return { 'x1': x1, 'x2': x2, 'y1': y1, 'y2': y2, 'w': neww, 'h': newh, 'cellx1': cellx1, 'cellx2': cellx2, 'celly1': celly1, 'celly2': celly2 }
    },
    getLabelReviews(limit, skip, status) {
      getLabelReviews({ limit: limit, skip: skip, status: status }).then(res => {
        this.fov_img = res.data.data
        if (this.fov_img.reviews.length) {
          this.fov_img.reviews.map(v => {
            const xywh = this.calculateSquare(v.x1, v.x2, v.y1, v.y2, v.w, v.h)

            v.imgpath2 = v.imgpath + '?crop=' + xywh.x1 + ',' + xywh.y1 + '|' + xywh.x2 + ',' + xywh.y2 + '&quality=100'
            v.tagName = ''
            console.log(xywh)
            v.position = {
              // 如果靠边框的会框错
              x: parseFloat(xywh.cellx1 / xywh.w) * 100 + '%',
              x1: parseFloat(xywh.cellx2 / xywh.w) * 100 + '%',
              y: parseFloat(xywh.celly1 / xywh.h) * 100 + '%',
              y1: parseFloat(xywh.celly2 / xywh.h) * 100 + '%'
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
@media screen and (min-width: 300px) and (max-width: 600px) {
  .label-img {
    flex-direction: column;
    .ai-observer {
      // display: none;
      width: 100%;
      height: 300px;
    }
    .item {
      margin: 5px 0;
    }
  }
}
@media screen and (min-width: 600px) and (max-width: 800px) {
  .label-img {
    flex-direction: column;
    .ai-observer {
      // display: none;
      width: 100%;
      height: 400px;
    }
    .item {
      margin: 10px;
    }
  }
}
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
    flex-wrap: wrap;
  }
  .radio-list {
    display: block;
    border: 1px dashed #ccc;
    padding: 5px 10px;
    .radio-item {
      display: block;
      margin: 5px 0;
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
