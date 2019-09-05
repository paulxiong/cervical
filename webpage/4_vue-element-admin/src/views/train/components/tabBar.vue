<template>
  <section class="tabBar">
    <!-- <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
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
    </el-tabs> -->
    
    <el-steps :active="active" finish-status="success" simple style="margin-top: 20px">
      <el-step title="图片" icon="el-icon-picture"></el-step>
      <el-step title="训练" ></el-step>
      <el-step title="评估" ></el-step>
      <el-step title="预测" ></el-step>
    </el-steps>
    <section class="box">
      <imagesCom v-if="active===0"></imagesCom>
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
      active: 0
    };
  },
  methods: {
    handleClick(tab, event) {
      console.log(tab, event);
    }
  }
};
</script>
