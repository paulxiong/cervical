<template>
  <div style="width:200px">
    <vue-photo-zoom-pro
      ref="thumbs"
      :width="width"
      :height="height"
      :url="url"
      :zoomer-style="{ 'background-color': 'rgba(79, 255, 0, 0.2)', 'border': '1px solid rgba(245, 6, 6, 0.78)' }"
      @updatexy="updatexy"
    />
  </div>
</template>

<script>
import VuePhotoZoomPro from '@/components/mapx/vue-photo-zoom-pro'

export default {
  name: 'Mapx',
  components: { VuePhotoZoomPro },
  props: {
    url: {
      type: String,
      default: ''
    },
    col: { type: Number, default: 34 },
    row: { type: Number, default: 41 }
  },
  data() {
    return {
      width: 200 / (this.col / 2), // 假设一屏显示2列
      height: 200 / (this.row / 2), // 假设一屏显示2行
      xpercent: 0, // 全图移动写回鹰眼图的时候要先检查坐标是不是变了
      ypercent: 0 // 全图移动写回鹰眼图的时候要先检查坐标是不是变了
    }
  },
  created() {
  },
  mounted() {
  },
  methods: {
    updatexy(xy) {
      this.xpercent = xy.xpercent.toFixed(2)
      this.ypercent = xy.ypercent.toFixed(2)
      this.$emit('updatexy', xy)
    },
    mouseMoveToXY(xpercent, ypercent) {
      if (parseInt(xpercent * 100) !== parseInt(this.xpercent * 100) ||
        parseInt(ypercent * 100) !== parseInt(this.ypercen * 100)) {
        this.$refs.thumbs.mouseMoveToXY(xpercent, ypercent)
      }
    }
  }
}
</script>

<style>
</style>
