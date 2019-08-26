<template>
  <div class="train">
    <section class="header">
      <div class="title flex">
        <h2>Models</h2>
        <el-button type="primary">新建训练模型</el-button>
      </div>
      <el-progress :text-inside="true" :stroke-width="26" :percentage="percentage"  status="success"></el-progress>
    </section>
    <modelCard></modelCard>
  </div>
</template>

<script>
import modelSelect from "./components/model-select"
import modelCard from "./components/model-card"

export default {
  name: "train",
  components: { modelSelect, modelCard },
  data() {
    return {
      percentage: 0
    };
  },
  methods: {},
  mounted() {
    setTimeout(()=>{this.percentage=27},1000)
    setTimeout(()=>{this.percentage=64},3000)
    setTimeout(()=>{this.percentage=88},4000)
    setTimeout(()=>{this.percentage=100},6000)    
  }
};
</script>

<style lang="scss" scoped>
.train {
  padding: 0 30px;
  .header {
    .title {
      justify-content: flex-start;
      h2 {
        margin-right: 10px;
      }
    }
  }
}
</style>
