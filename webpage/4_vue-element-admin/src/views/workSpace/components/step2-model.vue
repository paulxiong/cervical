<template>
  <div class="checkModel">
    <section class="btn flex">
      <el-button type="primary" :disabled="!options.length" class="next-btn" @click="nextStep">
        下一步
        <i class="el-icon-arrow-right el-icon--right" />
      </el-button>
    </section>
    <section class="info flex">
      <section class="model-info">
        <h4>模型选择</h4>
        <el-select v-model="model" class="model-option" clearable placeholder="请选择">
          <el-option
            v-for="item in options"
            :key="item.id"
            :label="item.desc"
            :value="item"
          />
        </el-select>
      </section>

      <section class="param">
        <h4>图片色彩</h4>
        <el-radio-group v-model="imgColor">
          <el-radio-button label="黑白" />
          <el-radio-button label="彩色" />
        </el-radio-group>
      </section>
      <section class="param">
        <h4>裁剪大小(单位px)</h4>
        <el-input v-model="cutInput" class="input" placeholder="请输入裁剪大小" />
      </section>
    </section>
  </div>
</template>

<script>
import { getListmodel } from '@/api/cervical'
export default {
  name: 'CheckModel',
  components: {},
  data() {
    return {
      imgColor: '黑白',
      cutInput: 100,
      options: [],
      model: ''
    }
  },
  created() {
    this.getListmodel()
  },
  methods: {
    nextStep() {
      /**
       * 保存model和参数信息并下一步
       */
      const modelInfo = {
        imgColor: this.imgColor,
        cutSize: this.cutInput,
        model: this.model
      }
      localStorage.setItem('MODEL_INFO', JSON.stringify(modelInfo))
      this.$parent.stepNext()
    },
    getListmodel() {
      getListmodel().then(res => {
        this.options = res.data.data.models
        this.model = this.options[0]
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.checkModel {
  .next-btn {
    width: 150px;
    font-weight: bold;
  }
  .param {
    margin-left: 30px;
  }
  .input {
    width: 200px;
  }
}
</style>
