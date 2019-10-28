<template>
  <div class="train">
    <section class="step">
      <el-steps :active="step">
        <el-step description="选择批次和病例" icon="el-icon-picture" />
        <el-step description="选择模型并调整参数" icon="el-icon-edit" />
        <el-step description="选择开始训练" icon="el-icon-upload" />
      </el-steps>
    </section>

    <section class="main">
      <checkImg v-if="step===1" />
      <checkModel v-if="step===2" />
      <startTrain v-if="step===3" />
    </section>
  </div>
</template>

<script>
import checkImg from './components/step1-img'
import checkModel from './components/step2-model'
import startTrain from './components/step3-train'

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
      this.step++
    },
    stepBack() {
      this.step = 1
    }
  }
}
</script>

<style lang="scss" scoped>
.train {
  padding: 30px;
  .step {
    margin-bottom: 10px;
  }
}
</style>
