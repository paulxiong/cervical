<template>
  <div class="newCustomDatasets">
    <section class="step">
      <el-steps :active="step">
        <el-step :title="upload ? $t('workspace.projectDataUpload3') : $t('workspace.projectDataSelect')" icon="el-icon-picture" />
        <el-step :title="$t('workspace.projectDataModel3')" icon="el-icon-edit" />
        <el-step :title="$t('workspace.projectDataReconfirm')" icon="el-icon-upload" />
      </el-steps>
    </section>

    <section class="main">
      <customDataUpload v-if="upload && step===1" @checkUpload="checkUpload" />
      <checkImg v-if="!upload && step===1" @checkImg="checkImg" />
      <checkModel v-if="step===2" ref="checkModel" :upload="upload" @checkModel="checkModel" />
      <startTrain v-if="step===3" />
    </section>
  </div>
</template>

<script>
import customDataUpload from './customdataupload'
import checkImg from './step1-img'
import checkModel from './step2-model'
import startTrain from './step3-train'

export default {
  name: 'NewCustomDatasets',
  components: { checkImg, checkModel, startTrain, customDataUpload },
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
    checkUpload(val) {
      this.$emit('checkUpload', val)
    },
    checkImg(val) {
      this.$emit('checkImg', val)
    },
    checkModel(val) {
      this.$emit('checkModel', val)
    },
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
.step {
  margin-bottom: 10px;
}
</style>
