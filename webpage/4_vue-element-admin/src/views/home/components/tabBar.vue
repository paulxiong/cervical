<template>
  <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
    <el-tab-pane label="图片" name="images">
      <imagesCom></imagesCom>
    </el-tab-pane>
    <el-tab-pane label="训练" name="train">
      <trainCom></trainCom>
    </el-tab-pane>
    <el-tab-pane label="评估" name="evaluate">
      <evaluateCom></evaluateCom>
    </el-tab-pane>
    <el-tab-pane label="预测" name="predict">
      <predictCom></predictCom>
    </el-tab-pane>
  </el-tabs>
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
      activeName: "images"
    };
  },
  methods: {
    handleClick(tab, event) {
      console.log(tab, event);
    }
  }
};
</script>