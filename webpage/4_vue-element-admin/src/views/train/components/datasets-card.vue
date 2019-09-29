<template>
  <div class="card">
    <el-card class="box-card" shadow="hover">
      <div slot="header" class="flex card-header">
        <b>{{datasets.desc}}</b>
        <b style="display:block;">{{datasets.type | filtersStatus}}</b>
        <div class="score">
          {{datasets.created_by | filterCreated}}
        </div>
      </div>
      <div class="flex model-info">
        <section class="info">
          <i>Datasets ID:</i>
          <b>{{datasets.id}}</b>
        </section>
        <section class="info">
          <i>路径</i>
          <b>{{datasets.dir}}</b>
        </section>
        <section class="info">
          <i>状态</i>
          <b>{{datasets.status | filtersTaskStatus}}</b>
        </section>
        <section class="info">
          <i>进度</i>
          <b>{{datasets.percent}}%</b>
        </section>
        <section class="info">
          <i>创建时间</i>
          <b>{{datasets.created_at | filtersTime}}</b>
        </section>
        <section class="info">
          <i>训练时间</i>
          <b>{{datasets.traintime | filtersTime}}</b>
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
  data() {
    return {
    }
  },
  props: {
    datasets: {
      type: Object
    }
  },
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
