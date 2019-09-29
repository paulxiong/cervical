<template>
  <div class="card">
    <el-card class="box-card" shadow="hover">
      <div slot="header" class="flex card-header">
        <b v-if="predict === 'predict'">{{trainInfo.desc || `第${trainInfo.id}个模型`}}</b>
        <el-input
          class="model-input"
          type="text"
          placeholder="请输入模型名称"
          v-model="trainInfo.desc"
          maxlength="30"
          @blur="emitDesc"
          @keyup.enter.native="emitDesc"
          show-word-limit
          v-else
        >
        </el-input>
        <b style="display:block;">{{trainInfo.type | filterModelType}}</b>
        <div class="score flex">
          <section class="precision-info">
            <i>Precision</i>
            <b>{{trainInfo.precision}}</b>
          </section>
          <section class="recall-info">
            <i>Recall</i>
            <b>{{trainInfo.recall}}</b>
          </section>
        </div>
      </div>
      <div class="flex model-info">
        <section class="info">
          <i>ID:</i>
          <b>{{trainInfo.id}}</b>
        </section><section class="info">
          <i>Datasets ID:</i>
          <b>{{trainInfo.did}}</b>
        </section>
        <section class="info">
          <i>路径</i>
          <b>{{trainInfo.path}}</b>
        </section>
        <section class="info">
          <i>损失:</i>
          <b>{{trainInfo.loss}}</b>
        </section>
        <section class="info">
          <i>训练有几个分类</i>
          <b>{{trainInfo.n_classes}}</b>
        </section>
        <section class="info">
          <i>训练用了多少张图片</i>
          <b>{{trainInfo.n_train}}</b>
        </section>
        <section class="info">
          <i>训练准确度</i>
          <b>{{trainInfo.metric_value}}</b>
        </section>
        <section class="info">
          <i>评估准确度</i>
          <b>{{trainInfo.evaluate_value}}</b>
        </section>
        <!-- <section class="info">
          <i>创建时间</i>
          <b>{{trainInfo.created_at}}</b>
        </section>
        <section class="info">
          <i>更新时间</i>
          <b>{{trainInfo.updated_at}}</b>
        </section> -->
      </div>
    </el-card>
  </div>
</template>

<script>
import { modelType } from '@/const/const'

export default {
  name: 'Card',
  components: {},
  data() {
    return {
      modelDesc: ''
    }
  },
  props: {
    trainInfo: {
      type: Object
    },
    predict: {
      type: String
    }
  },
  filters: {
    filterModelType(value) {
      return modelType[value]
    }
  },
  methods: {
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
    justify-content: space-around;
    flex-wrap: wrap;
    .info {
      width: 50%;
      margin: 10px 0;
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
