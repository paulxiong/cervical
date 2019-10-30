<template>
  <div class="checkModel">
    <section class="info flex">
      <section class="model-info">
        <h4>切割模型</h4>
        <el-select v-model="model" class="model-option" placeholder="请选择">
          <el-option
            v-for="item in options"
            :key="item.id"
            :label="item.desc"
            :value="item"
          />
        </el-select>
      </section>
      <section class="param">
        <h4>使用缓存</h4>
        <el-radio-group v-model="cache">
          <el-radio-button label="是" />
          <el-radio-button label="否" />
        </el-radio-group>
      </section>
      <section class="param">
        <h4>背景色</h4>
        <el-radio-group v-model="imgColor">
          <el-radio-button label="灰色" />
          <el-radio-button label="彩色" />
        </el-radio-group>
      </section>
      <section class="param">
        <h4>裁剪大小(像素)</h4>
        <el-radio-group v-model="cutInput">
          <el-radio-button label="100" />
          <el-radio-button label="120" />
          <el-radio-button label="150" />
        </el-radio-group>
      </section>
      <section class="param">
        <h4>切割类型</h4>
        <el-radio-group v-model="type">
          <el-radio-button label="0-图片直接检测并切割出细胞" />
          <el-radio-button label="1-按照标注csv切割细胞" />
          <el-radio-button label="2-mask-rcnn检测细胞和csv交集的切割" />
        </el-radio-group>
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
      cache: '是',
      imgColor: '灰色',
      cutInput: 100,
      type: '0-图片直接检测并切割出细胞',
      options: [],
      model: ''
    }
  },
  created() {
    this.getListmodel()
  },
  methods: {
    saveModelInfo() {
      /**
       * 保存model和参数信息并下一步
       */
      const modelInfo = {
        cache: this.cache,
        imgColor: this.imgColor,
        cutSize: this.cutInput,
        type: this.type,
        model: this.model
      }
      localStorage.setItem('MODEL_INFO', JSON.stringify(modelInfo))
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
  .info {
    flex-wrap: wrap;
    justify-content: space-around;
  }
  .param {
    margin-left: 30px;
  }
  .input {
    width: 200px;
  }
}
</style>
