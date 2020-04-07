<template>
  <div id="app">
    <p>配置3倍放大：<span style="color:#ff6600">:scale="10"</span></p>
    <div class="pic-box">
      <pic-zoom url="http://dev.medical.raidcdn.cn:3000/imgs/scratch/img/b157936320000025/m157940002198925/Images/2eefcba36cb841cebddf869cfcbde31d?width=1000" :scale="10" />
    </div>
  </div>
</template>

<script>
import PicZoom from '@/components/mapx'

export default {
  name: 'App',
  components: {
    PicZoom
  },
  data() {
    return {
      url: 'static/imac2.jpg'
    }
  },
  methods: {
    changeUrl() {
      this.url = 'http://imgsrc.baidu.com/imgad/pic/item/3801213fb80e7beca9004ec5252eb9389b506b38.jpg'
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
  padding-bottom: 100px;
}
.pic-box{
  width:500px;
  height:500px;
  border:1px solid #eee;
}
</style>
