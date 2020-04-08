<template>
  <div style="width:200px">
    <vue-photo-zoom-pro
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
      default: 'http://medical.raidcdn.cn:3000/imgs/scratch/img/b20200403/m20200403193737/Thumbs/Result-1905955%2B%E4%BD%8E.jpg?width=300'
    },
    col: { type: Number, default: 34 },
    row: { type: Number, default: 41 }
  },
  data() {
    return {
      width: 200 / (this.col / 2), // 假设一屏显示2列
      height: 200 / (this.row / 2) // 假设一屏显示2行
    }
  },
  created() {
  },
  methods: {
    updatexy(xy) {
      this.$emit('updatexy', xy)
    }
  }
}
</script>

<style>
</style>
