<template>
  <div class="checkModel">
    <section class="info flex">
      <section class="model-info">
        <h4>{{ $t('workspace.dataSegmentationModel') }}</h4>
        <el-select v-model="model" class="model-option" :placeholder="$t('workspace.dataSegmentationModel2')">
          <el-option
            v-for="item in options"
            :key="item.id"
            :label="item.desc"
            :value="item"
            @change="changeModel"
          />
        </el-select>
      </section>
      <section class="param">
        <h4>{{ $t('workspace.dataCache') }}</h4>
        <el-radio-group v-model="cache">
          <el-radio-button :label="$t('workspace.dataCacheYes')" />
          <el-radio-button :label="$t('workspace.dataCacheNo')" />
        </el-radio-group>
      </section>
      <section class="param">
        <h4>{{ $t('workspace.dataColor') }}</h4>
        <el-radio-group v-model="imgColor">
          <el-radio-button :label="$t('workspace.dataColorGray')" />
          <el-radio-button :label="$t('workspace.dataColorColor')" />
        </el-radio-group>
      </section>
      <section class="param">
        <h4>{{ $t('workspace.dataSegmentationSize') }}</h4>
        <el-radio-group v-model="cutInput">
          <el-radio-button label="100" />
          <el-radio-button label="150" />
          <el-radio-button label="224" />
        </el-radio-group>
      </section>
      <section class="param">
        <h4>{{ $t('workspace.dataSegmentationType') }}</h4>
        <el-radio-group v-model="type">
          <el-radio-button :label="$t('workspace.dataSegmentationType0')" />
          <el-radio-button v-if="!upload" :label="$t('workspace.dataSegmentationType1')" />
          <!-- <el-radio-button label="2-mask-rcnn检测细胞和csv交集的切割" /> -->
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
  props: {
    upload: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      cache: this.$t('workspace.dataCacheYes'),
      imgColor: this.$t('workspace.dataColorGray'),
      cutInput: 100,
      type: this.$t('workspace.dataSegmentationType0'),
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
    changeModel(val) {
      this.$emit('checkModel', this.model.id)
    },
    getListmodel() {
      getListmodel().then(res => {
        this.options = res.data.data.models
        this.model = this.options[0]
        this.$emit('checkModel', false)
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
