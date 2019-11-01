<template>
  <section class="trainDetails">
    <!-- <section v-if="did && pid === undefined" class="step flex">
      <el-button size="mini" :type="active===1?'success':'info'" @click="active=1"><i class="el-icon-picture" style="margin-right:5px" />图片</el-button>
    </section> -->
    <section v-if="pid && type === 2" class="step flex">
      <el-button size="mini" :type="active===2?'success':'info'" @click="active=2"><i class="el-icon-finished" style="margin-right:5px" />训练&评估</el-button>
      <i class="el-icon-arrow-right icon-right" />
      <el-button size="mini" :type="active===1?'success':'info'" @click="active=1"><i class="el-icon-picture" style="margin-right:5px" />图片</el-button>
    </section>
    <section v-if="pid && type === 3" class="step flex">
      <el-button size="mini" :type="active===3?'success':'info'" @click="active=3"><i class="el-icon-finished" style="margin-right:5px" />预测</el-button>
      <i class="el-icon-arrow-right icon-right" />
      <el-button size="mini" :type="active===1?'success':'info'" @click="active=1"><i class="el-icon-picture" style="margin-right:5px" />图片</el-button>
    </section>
    <section class="box">
      <imagesCom v-if="active===1" />
      <trainCom v-if="active===2" />
      <predictCom v-if="active===3" />
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
      activeName: 'images',
      percentage: 0,
      active: undefined,
      did: undefined,
      pid: undefined,
      type: undefined
    }
  },
  created() {
    this.did = this.$route.query.did ? parseInt(this.$route.query.did) : undefined
    this.pid = this.$route.query.pid ? parseInt(this.$route.query.pid) : undefined
    this.type = this.$route.query.type ? parseInt(this.$route.query.type) : undefined
    if (this.pid && this.type === 2) {
      this.active = 2
    } else if (this.pid && this.type === 3) {
      this.active = 3
    } else {
      this.active = 1
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
