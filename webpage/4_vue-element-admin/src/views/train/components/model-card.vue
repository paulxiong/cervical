<template>
  <div class="card">
    <el-card class="box-card" shadow="hover">
      <div slot="header" class="flex card-header">
        <el-select
          v-if="predict === 'predict'"
          class="model-option"
          v-model="model"
          clearable
          placeholder="请选择"
          @change="modelChange"
        >
          <el-option v-for="(item, idx) in modelList" :key="item.id" :label="item.desc" :value="idx"></el-option>
        </el-select>
        <el-input
          class="model-input"
          type="text"
          placeholder="请输入模型名称"
          v-model="modelInfo.desc"
          maxlength="30"
          @blur="emitDesc"
          @keyup.enter.native="emitDesc"
          show-word-limit
          v-else
        >
        </el-input>
        <b style="display:block;">{{modelInfo.type | filterModelType}}</b>
        <div class="score flex">
          <section class="precision-info">
            <i>Precision</i>
            <b>{{modelInfo.precision}}</b>
          </section>
          <section class="recall-info">
            <i>Recall</i>
            <b>{{modelInfo.recall}}</b>
          </section>
        </div>
      </div>
      <div class="flex model-info">
        <section class="info">
          <i>ID:</i>
          <b>{{modelInfo.id}}</b>
        </section><section class="info">
          <i>Datasets ID:</i>
          <b>{{modelInfo.did}}</b>
        </section>
        <section class="info">
          <i>路径</i>
          <b>{{modelInfo.path}}</b>
        </section>
        <section class="info">
          <i>损失:</i>
          <b>{{modelInfo.loss}}</b>
        </section>
        <section class="info">
          <i>训练有几个分类:</i>
          <b>{{modelInfo.n_classes}}</b>
        </section>
        <section class="info">
          <i>训练用了多少张图片:</i>
          <b>{{modelInfo.n_train}}</b>
        </section>
        <section class="info">
          <i>训练准确度:</i>
          <b>{{modelInfo.metric_value}}</b>
        </section>
        <section class="info">
          <i>评估准确度:</i>
          <b>{{modelInfo.evaluate_value}}</b>
        </section>
        <section class="info" v-if="modelInfo.celltypes">
          <i>细胞类型选择:</i>
          <el-checkbox-group v-model="checkboxCell" size="mini" class="cell-checkbox">
            <el-checkbox v-for="(v, i) in modelInfo.celltypes" :key="i" :label="v | filtersCheckbox" :checked="i<=1" border></el-checkbox>
          </el-checkbox-group>
        </section>
        <!-- <section class="info">
          <i>创建时间</i>
          <b>{{modelInfo.created_at}}</b>
        </section>
        <section class="info">
          <i>更新时间</i>
          <b>{{modelInfo.updated_at}}</b>
        </section> -->
      </div>
    </el-card>
  </div>
</template>

<script>
import { modelType, cellsType } from '@/const/const'

export default {
  name: 'Card',
  components: {},
  data() {
    return {
      checkboxCell: [],
      model: 0
    }
  },
  props: {
    modelInfo: {
      type: Object || String
    },
    modelList: {
      type: Array
    },
    predict: {
      type: String
    }
  },
  filters: {
    filterModelType(value) {
      return modelType[value]
    },
    filtersCheckbox(val) {
      return `${val} ${cellsType[val]}`
    }
  },
  methods: {
    modelChange() {
      this.modelInfo = this.modelList[this.model]
    },
    emitDesc() {
      this.$emit('changeDesc', this.trainInfo.desc)
    }
  }
}
</script>

<style lang="scss" scoped>
.card {
  margin-top: 10px;
  i {
    color: #666;
    font-style: normal;
    margin-right: 10px;
  }
  b {
    font-size: 22px;
  }
  .model-input {
    width: 50%;
  }
  .card-header {
    justify-content: space-between;
    .precision-info {
      margin-right: 20px;
    }
  }
  .model-info {
    justify-content: space-between;
    flex-wrap: wrap;
    .info {
      width: 60%;
      overflow: hidden;
      text-overflow: ellipsis;
      margin: 10px 0;
    }
    .info:nth-child(even) {
      width: 40%;
    }
    .percent {
      position: relative;
    }
    .percent-title {
      position: absolute;
      top: 10px;
      left: 30px;
    }
    .el-icon-question {
      position: absolute;
      bottom: 30px;
      left: 55px;
    }
    .recall {
      position: relative;
    }
    .recall-title {
      position: absolute;
      top: 10px;
      left: 40px;
    }
  }
}
</style>
