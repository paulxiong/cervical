<template>
  <div class="card">
    <el-card class="box-card" shadow="hover">
      <div v-if="save === 'save'" slot="header" class="flex card-header">
        <el-input
          v-model="inputName"
          autofocus
          :placeholder="$t('workspace.projectNewEnterDesc')"
          show-word-limit
          maxlength="30"
          class="input-name"
          @keyup.enter.native="saveModel"
        />
        <el-button
          v-if="showSaveBtn"
          type="danger"
          size="small"
          class="save-btn"
          :disabled="!modelInfo.desc"
          @click="saveModel"
        >{{ $t('workspace.projectSaveModel') }}</el-button>
      </div>
      <div v-else slot="header" class="flex card-header">
        <el-badge is-dot class="badge-item">{{ $t('workspace.projectSelectModel') }}</el-badge>
        <el-select
          v-model="model"
          class="model-option"
          style="width:240px"
          :placeholder="$t('workspace.projectSelectModel2')"
          size="mini"
          @change="modelChange"
        >
          <el-option v-for="(item, idx) in modelList" :key="item.id" :label="item.desc" :value="idx" />
        </el-select>
      </div>
      <div class="flex model-info">
        <section class="info">
          <i>{{ $t('workspace.projectModelPrecision') }}:</i>
          <b>{{ modelInfo.precision }}</b>
        </section><section class="info">
          <i>{{ $t('workspace.projectModelRecall') }}:</i>
          <b>{{ modelInfo.recall }}</b>
        </section>
        <section class="info">
          <i>{{ $t('workspace.projectModelLoss') }}:</i>
          <b>{{ modelInfo.loss }}</b>
        </section>
        <section v-if="modelInfo.input_shape" class="info">
          <i>{{ $t('workspace.projectModelSize') }}:</i>
          <b>{{ modelInfo.input_shape }}</b>
        </section>
        <section class="info">
          <i>{{ $t('workspace.projectModelType2') }}:</i>
          <b>{{ modelInfo.type | filterModelType }}</b>
        </section>
        <section class="info">
          <i>{{ $t('workspace.projectModelTrainNum') }}:</i>
          <b>{{ modelInfo.n_train }}</b>
        </section>
        <section class="info">
          <i>{{ $t('workspace.projectModelClassNum') }}:</i>
          <b>{{ modelInfo.n_classes }}</b>
        </section>
        <section v-if="modelInfo.types" class="info" style="height: auto;overflow: auto;">
          <i>{{ $t('workspace.projectModelCellType') }}:</i>
          <b>{{ modelInfo.types | filtersCellsType }}</b>
        </section>
      </div>
    </el-card>
  </div>
</template>

<script>
import { savemodel } from '@/api/cervical'
import { modelType, cellsType } from '@/const/const'

export default {
  name: 'Card',
  components: {},
  filters: {
    filterModelType(value) {
      return modelType[value]
    },
    filtersCellsType(val) {
      const arr = []
      val.map(v => {
        v = cellsType[v]
        arr.push(v)
      })
      return arr
    }
  },
  props: {
    save: {
      type: String,
      default: ''
    },
    modelInfo: {
      type: Object || String,
      default: ''
    },
    modelList: {
      type: Array,
      default() {
        return []
      }
    }
  },
  data() {
    return {
      inputName: '',
      checkboxCell: [],
      model: 0,
      showSaveBtn: true
    }
  },
  created() {
    this.inputName = this.modelInfo.desc
    this.changeCellTypes()
  },
  methods: {
    saveModel() {
      savemodel({
        'id': this.modelInfo.pid,
        'desc': this.inputName
      }).then(res => {
        this.$message({
          message: res.data.data,
          type: 'success'
        })
        this.showSaveBtn = false
      })
    },
    modelChange() {
      this.$emit('modelChange', this.modelList[this.model])
    },
    changeCellTypes() {
      const postCelltypes = []
      this.checkboxCell.map(v => {
        v = parseInt(v.slice(0, 1))
        postCelltypes.push(v)
      })
      this.$emit('changeCellTypes', postCelltypes)
    }
  }
}
</script>

<style lang="scss" scoped>
.card {
  margin-top: 10px;
  opacity: 0.9;
  i {
    color: #666;
    font-style: normal;
    margin-right: 5px;
    font-size: 14px
  }
  b {
    font-size: 14px;
    font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
  }
  .model-input {
    width: 50%;
  }
  .card-header {
    justify-content: flex-start;
    .badge-item {
      margin-right: 10px;
    }
  }
  .model-info {
    justify-content: space-between;
    flex-wrap: wrap;
    .info {
      width: calc(100%/4);
      overflow: hidden;
      text-overflow: ellipsis;
      margin: 5px 0;
    }
  }
}
</style>
