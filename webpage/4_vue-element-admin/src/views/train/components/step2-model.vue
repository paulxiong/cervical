<template>
  <div class="checkModel">
    <section class="btn flex">
      <!-- :disabled="!options.length" -->
      <el-button type="primary" @click="nextStep" class="next-btn">
        下一步
        <i class="el-icon-arrow-right el-icon--right"></i>
      </el-button>
    </section>
    <section class="info flex">
      <section class="model-info">
        <h4>模型选择</h4>
        <el-select class="model-option" v-model="model" clearable placeholder="请选择">
          <el-option
            v-for="item in options"
            :key="item.id"
            :label="item.desc"
            :value="item"
          ></el-option>
        </el-select>
      </section>

      <section class="param">
        <h4>图片色彩</h4>
        <el-radio-group v-model="imgColor">
          <el-radio-button label="黑白"></el-radio-button>
          <el-radio-button label="彩色"></el-radio-button>
        </el-radio-group>
      </section>
      <section class="param">
        <h4>裁剪大小(单位px)</h4>
        <el-input class="input" v-model="cutInput" placeholder="请输入裁剪大小"></el-input>
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
  },
  mounted() {
    this.getListmodel()
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
