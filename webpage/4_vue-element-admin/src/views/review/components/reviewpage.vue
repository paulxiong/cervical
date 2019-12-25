<template>
  <div class="temps">
    <section class="label-img flex">
      <AIMarker
        ref="aiPanel-editor"
        class="ai-observer"
        :style="{width: imgInfo.w < 850 ? imgInfo.w + 'px' : 850 + 'px',height: imgInfo.w < 850 ? imgInfo.h + 'px' : (imgInfo.h*(850/imgInfo.w)) + 'px'}"
        :read="readOnly"
        :img="hosturlpath64 + imgInfo.imgpath + '?width=850'"
      />
      <el-badge
        :value="`${imgInfo.predict_score}`"
        :type="imgInfo.predict_type === 51 ? 'warning': 'info'"
        class="item"
      >
        <el-image
          class="img-item img-right"
          :src="hosturlpath64 + imgInfo.cellpath + '?width=200'"
        />
      </el-badge>
      <el-radio-group v-model="true_type" style="width: 200px;" @change="updateLabelReview">
        <el-radio-button v-for="(cells, idx) of cellsType" :key="idx" :label="cells" />
      </el-radio-group>
    </section>
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
      imgInfo: {},
      skip: 0,
      fov_img: []
    }
  },
  created() {
    this.getLabelReviews(1, this.skip, 0)
  },
  methods: {
    getLabelReviews(limit, skip, status) {
      getLabelReviews({ limit: limit, skip: skip, status: status }).then(res => {
        this.fov_img = res.data.data
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
        this.renderLabel(this.fov_img.reviews)
      })
    },
    updateLabelReview() {
      updateLabelReview({
        id: this.imgInfo.id,
        true_type: parseInt(this.true_type.split(' ')[0])
      }).then(res => {
        this.true_type = ''
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
  .label-img {
    justify-content: space-around;
  }
  .img-item {
    border: 1px solid #ccc;
    // margin-right: 10px;
    // margin-bottom: 10px;
  }
  .img-right {
    border: 2px solid rgb(0, 255, 81);
    border-radius: 5px;
  }
}
</style>
