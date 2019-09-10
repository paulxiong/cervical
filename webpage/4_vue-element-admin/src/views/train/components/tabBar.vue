<template>
  <section class="tabBar">
    <section class="step flex">
      <el-button size="mini" :type="active===0?'success':'info'" @click="active=0"><i :class="percentage!==100?'el-icon-loading':'el-icon-finished'"></i> 图片</el-button>
      <i class="el-icon-arrow-right icon-right"></i>
      <el-button size="mini" :type="active===1?'success':'info'" @click="active=1" :disabled="percentage!==100"><i class="el-icon-finished"></i> 训练</el-button>
      <i class="el-icon-arrow-right icon-right"></i>
      <el-button size="mini" :type="active===2?'success':'info'" @click="active=2" :disabled="percentage!==100"><i class="el-icon-finished"></i> 评估</el-button>
      <i class="el-icon-arrow-right icon-right"></i>
      <el-button size="mini" :type="active===3?'success':'info'" @click="active=3" :disabled="percentage!==100"><i class="el-icon-finished"></i> 预测</el-button>
    </section>
    <section class="box">
      <imagesCom @finished="imagesFinished" v-if="active===0"></imagesCom>
      <trainCom v-if="active===1"></trainCom>
      <evaluateCom v-if="active===2"></evaluateCom>
      <predictCom v-if="active===3"></predictCom>
    </section>
  </section>
</template>

<script>
import imagesCom from "../images";
import trainCom from "../train";
import evaluateCom from "../evaluate";
import predictCom from "../predict";

export default {
  components: {
    imagesCom,
    trainCom,
    evaluateCom,
    predictCom
  },
  data() {
    return {
      activeName: "images",
      percentage: 0,
      active: 0
    };
  },
  methods: {
    tabClick() {
      console.log(123)
    },
    handleClick(tab, event) {
      console.log(tab, event);
    },
    imagesFinished(percentage) {
      this.percentage = percentage
    }
  }
};
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
