<template>
  <div class="train">
    <section class="header">
      <div class="title">
        <h2>TRAIN</h2>
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
    setTimeout(()=>{this.percentage=27},3000)
    setTimeout(()=>{this.percentage=64},5000)
    setTimeout(()=>{this.percentage=88},7000)
    setTimeout(()=>{this.percentage=100},9000)
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
