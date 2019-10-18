<template>
  <section class="trainDetails">
    <section v-if="showStep===1?true:false" class="step flex">
      <el-button size="mini" :type="active===0?'success':'info'" @click="active=0"><i :class="percentage!==100?'el-icon-loading':'el-icon-finished'" />图片</el-button>
      <i class="el-icon-arrow-right icon-right" />
      <el-button size="mini" :type="active===1?'success':'info'" :disabled="percentage!==100" @click="active=1"><i class="el-icon-finished" />训练&评估</el-button>
      <i class="el-icon-arrow-right icon-right" />
      <el-button size="mini" :type="active===2?'success':'info'" :disabled="percentage!==100" @click="active=2"><i class="el-icon-finished" />预测</el-button>
    </section>
    <section class="box">
      <imagesCom v-if="active===0" @finished="imagesFinished" />
      <trainCom v-if="active===1" />
      <predictCom v-if="active===2" />
    </section>
  </section>
</template>

<script>
import imagesCom from './images'
import trainCom from './train'
import predictCom from './predict'

export default {
  components: {
    imagesCom,
    trainCom,
    predictCom
  },
  data() {
    return {
      showStep: parseInt(localStorage.getItem('isPredict')) || 1,
      activeName: 'images',
      percentage: 0,
      active: 0
    }
  },
  methods: {
    imagesFinished(percentage) {
      this.percentage = percentage
    }
  }
}
</script>

<style lang="scss" scoped>
.step {
  margin-top: 20px;
  padding: 10px 0;
  background: #f5f7fa;
  justify-content: space-around;
  cursor: pointer;
  .icon-right {
    color: #c7cad2;
  }
}
</style>
