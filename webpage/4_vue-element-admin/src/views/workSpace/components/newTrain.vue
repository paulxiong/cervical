<template>
  <div class="train">
    <section class="step">
      <el-steps :active="step">
        <el-step title="选择批次和病例" description="步骤1" icon="el-icon-picture" />
        <el-step title="选择模型并调整参数" description="步骤2" icon="el-icon-edit" />
        <el-step title="选择开始训练" description="步骤3" icon="el-icon-upload" />
      </el-steps>

      <!-- <section class="btn flex">
        <el-button type="primary" icon="el-icon-arrow-left" @click="stepReduce">上一步</el-button>
        <el-button type="primary" @click="stepAdd">
          下一步
          <i class="el-icon-arrow-right el-icon--right"></i>
        </el-button>
      </section> -->
    </section>

    <section class="main">
      <checkImg v-if="step===1" />
      <checkModel v-if="step===2" />
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
