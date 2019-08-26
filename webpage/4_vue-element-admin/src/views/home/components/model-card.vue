<template>
  <div class="card">
    <el-card class="box-card" shadow="hover">
      <div slot="header" class="clearfix">
        <span>Cell20198_231125978646576151</span>
      </div>
      <div class="flex model-info">
        <section class="info flex created">
          <h3>Created</h3>
          <b>2019.8.20</b>
          <i>1 computer hour</i>
        </section>
        <section class="info flex analyzed">
          <h3>Analyzed</h3>
          <b>5238 images</b>
          <i>2 labels,520 test images</i>
        </section>
        <section class="info flex avg">
          <h3>Avg precision</h3>
          <b>0.996</b>
        </section>
        <section class="precent">
          <el-progress type="circle" class="precent" :percentage="95"></el-progress>
          <h4 class="precent-title">Precision</h4>
          <i class="el-icon-question"></i>
        </section>
        <section class="recall">
          <el-progress type="circle" class="recall" :percentage="96"></el-progress>
          <h4 class="recall-title">Recall</h4>
          <i class="el-icon-question"></i>
        </section>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: "card",
  components: {},
  data() {
    return {
      value: ""
    };
  },
  methods: {}
};
</script>

<style lang="scss" scoped>
.card {
  margin-top: 20px;
  i {
    color: #ccc;
    font-style: normal;
  }
  b {
    font-size: 22px;
  }
  .model-info {
    justify-content: space-around;
    .info {
      flex-direction: column;
      justify-content: flex-start;
    }
    .precent {
      position: relative;
    }
    .precent-title {
      position: absolute;
      top: 10px;
      left: 30px;
    }
    .el-icon-question {
      position: absolute;
      bottom: 30px;
      left: 55px;
    }
    .recall {
      position: relative;
    }
    .recall-title {
      position: absolute;
      top: 10px;
      left: 40px;
    }
  }
}
</style>
