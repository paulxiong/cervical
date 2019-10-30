<template>
  <div class="card">
    <el-card class="box-card" shadow="hover">
      <div slot="header" class="flex card-header">
        <el-badge is-dot class="badge-item">选择数据集</el-badge>
        <el-select
          v-model="datasets"
          class="model-option"
          style="width:220px"
          placeholder="请选择"
          size="mini"
          @change="datasetsChange"
        >
          <el-option v-for="(item, idx) in datasetsList" :key="item.id" :label="item.desc" :value="idx" />
        </el-select>
        <b style="display:block;">{{ datasetsInfo.type | filtersStatus }}</b>
        <div class="score">
          {{ datasetsInfo.created_by | filterCreated }}
        </div>
      </div>
      <div class="flex model-info">
        <section class="info">
          <i>创建者:</i>
          <b>{{ datasetsInfo.created_by }}</b>
        </section>
        <section class="info">
          <i>目录:</i>
          <b>{{ datasetsInfo.dir }}</b>
        </section>
        <section class="info">
          <i>状态:</i>
          <b>{{ datasetsInfo.status }}</b>
        </section>
        <section class="info">
          <i>裁剪模型:</i>
          <b>{{ datasetsInfo.parameter_mid }}</b>
        </section>
        <section class="info">
          <i>裁剪是否用缓存:</i>
          <b>{{ datasetsInfo.parameter_cache }}</b>
        </section>
        <section class="info">
          <i>裁剪采用颜色:</i>
          <b>{{ datasetsInfo.parameter_gray }}</b>
        </section>
        <section class="info">
          <i>裁剪采用大小:</i>
          <b>{{ datasetsInfo.parameter_size }}</b>
        </section>
        <section class="info">
          <i>细胞类型:</i>
          <b>{{ datasetsInfo.types }}</b>
        </section>
      </div>
    </el-card>
  </div>
</template>

<script>
import { taskStatus, typeStatus, taskType, createdBy } from '@/const/const'
import { dateformat3 } from '@/utils/dateformat'

export default {
  name: 'Card',
  components: {},
  filters: {
    filterCreated(value) {
      return createdBy[value]
    },
    filtersTaskType(value) {
      return taskType[value]
    },
    filtersTaskStatus(value) {
      return taskStatus[value]
    },
    filtersStatus(value) {
      return typeStatus[value]
    },
    filtersTime(value) {
      return dateformat3(value)
    }
  },
  props: {
    datasetsInfo: {
      type: Object || String,
      default: ''
    },
    datasetsList: {
      type: Array,
      default() {
        return []
      }
    }
  },
  data() {
    return {
      datasets: 0
    }
  },
  methods: {
    datasetsChange() {
      this.$emit('datasetsChange', this.datasetsList[this.datasets])
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
    font-size: 14px;
  }
  b {
    font-size: 14px;
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
    justify-content: space-around;
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
