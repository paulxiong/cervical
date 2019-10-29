<template>
  <div class="train">
    <section class="step">
      <el-steps :active="step">
        <el-step title="选择批次和病例" icon="el-icon-picture" />
        <el-step title="选择模型并调整参数" icon="el-icon-edit" />
        <el-step title="确认信息" icon="el-icon-upload" />
      </el-steps>
    </section>

    <section class="main">
      <checkImg v-if="step===1" />
      <checkModel v-if="step===2" ref="checkModel" />
      <startTrain v-if="step===3" />
    </section>
  </div>
</template>

<script>
import checkImg from './step1-img'
import checkModel from './step2-model'
import startTrain from './step3-train'

export default {
  name: 'Train',
  components: { checkImg, checkModel, startTrain },
  data() {
    return {
      step: 1
    }
  },
  methods: {
    stepNext() {
      if (this.step === 2) {
        this.$refs.checkModel.saveModelInfo()
      }
      if (this.step++ > 1) {
        this.step = 3
      }
    },
    stepBack() {
      if (this.step-- < 2) {
        this.step = 1
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.train {
  .step {
    margin-bottom: 10px;
  }
}
</style>
