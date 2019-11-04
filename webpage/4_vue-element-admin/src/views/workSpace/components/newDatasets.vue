<template>
  <div class="newDatasets">
    <section class="step">
      <el-steps :active="step">
        <el-step :title="upload ? '上传所选批次' : '选择批次和病例'" icon="el-icon-picture" />
        <el-step title="选择模型并调整参数" icon="el-icon-edit" />
        <el-step title="确认信息" icon="el-icon-upload" />
      </el-steps>
    </section>

    <section class="main">
      <uploadImg v-if="upload && step===1" />
      <checkImg v-if="!upload && step===1" />
      <checkModel v-if="step===2" ref="checkModel" />
      <startTrain v-if="step===3" />
    </section>
  </div>
</template>

<script>
import uploadImg from './uploadImg'
import checkImg from './step1-img'
import checkModel from './step2-model'
import startTrain from './step3-train'

export default {
  name: 'Newdatasets',
  components: { checkImg, checkModel, startTrain, uploadImg },
  props: {
    upload: {
      type: Boolean,
      default: false
    }
  },
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
