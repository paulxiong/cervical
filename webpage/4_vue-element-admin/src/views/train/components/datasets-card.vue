<template>
  <div class="card">
    <el-card class="box-card" shadow="hover">
      <div slot="header" class="flex card-header">
        <el-select
          v-if="predict === 'predict'"
          v-model="datasets"
          class="model-option"
          clearable
          placeholder="请选择"
          @change="datasetsChange"
        >
          <el-option v-for="(item, idx) in datasetsList" :key="item.id" :label="item.desc" :value="idx" />
        </el-select>
        <b v-else>{{ datasetsInfo.desc }}</b>
        <b style="display:block;">{{ datasetsInfo.type | filtersStatus }}</b>
        <div class="score">
          {{ datasetsInfo.created_by | filterCreated }}
        </div>
      </div>
      <div class="flex model-info">
        <section class="info">
          <i>ID:</i>
          <b>{{ datasetsInfo.id }}</b>
        </section>
        <section class="info">
          <i>路径:</i>
          <b>{{ datasetsInfo.dir }}</b>
        </section>
        <section class="info">
          <i>状态:</i>
          <b>{{ datasetsInfo.status | filtersTaskStatus }}</b>
        </section>
        <section class="info">
          <i>进度:</i>
          <b>{{ datasetsInfo.percent }}%</b>
        </section>
        <section class="info">
          <i>创建时间:</i>
          <b>{{ datasetsInfo.created_at | filtersTime }}</b>
        </section>
        <section class="info">
          <i>训练时间:</i>
          <b>{{ datasetsInfo.traintime | filtersTime }}</b>
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
    },
    predict: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      datasets: 0
    }
  },
  methods: {
    datasetsChange() {
      this.datasetsInfo = this.datasetsList[this.datasets]
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
    margin-right: 15px;
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
