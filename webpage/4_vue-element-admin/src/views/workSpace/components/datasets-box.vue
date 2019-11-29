<template>
  <div class="card flex">
    <el-card
      v-for="(v,i) in datalist"
      :key="i"
      class="box-card"
      :style="v.status === 3 || v.status === 5 || v.status === 8 ?'border:1px dashed #fc4b4e;box-shadow: 3px 3px 10px #fc4b4e;':''"
      :shadow="v.status === 3 || v.status === 5 || v.status === 8 ?'always':'hover'"
    >
      <div slot="header" class="clearfix">
        <span>{{ v.desc }}</span>
        <el-button
          style="float: right; padding: 3px 0"
          type="primary"
          @click="goDetails(v)"
        >查看详情</el-button>
      </div>

      <div class="content flex">
        <div class="info">
          <i>id :</i>
          {{ v.id }}
          <br>
          <i>路径 :</i>
          {{ v.dir }}
          <br>
          <i>创建者 :</i>
          {{ v.created_by | filterCreated }}
          <br>
          <i>类型 :</i>
          {{ v.type | filtersStatus }}
          <br>
          <i>状态 :</i>
          <el-tag
            :type="v.status | filtersTaskType"
            effect="dark"
          >{{ v.status | filtersTaskStatus }}</el-tag>
        </div>
        <el-timeline reverse class="timeline">
          <el-timeline-item
            v-for="(activity, index) in v.activities"
            :key="index"
            :icon="activity.icon"
            :color="activity.color"
            :type="activity.type"
            :timestamp="activity.timestamp"
          >{{ activity.content }}</el-timeline-item>
        </el-timeline>
      </div>
    </el-card>
  </div>
</template>

<script>
import { taskStatus, typeStatus, taskType, createdBy } from '@/const/const'
export default {
  name: 'Card',
  components: {},
  filters: {
    filterCreated(value) {
      return createdBy[value] || '普通用户'
    },
    filtersTaskType(value) {
      return taskType[value]
    },
    filtersTaskStatus(value) {
      return taskStatus[value]
    },
    filtersStatus(value) {
      return typeStatus[value]
    }
  },
  props: {
    datalist: {
      type: Array,
      default() {
        return []
      }
    }
  },
  methods: {
    goDetails(v) {
      localStorage.setItem('isPredict', v.type)
      this.$router.push({
        path: `/workSpace/details?id=${v.id}`
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.card {
  justify-content: flex-start;
  align-items: flex-start;
  flex-wrap: wrap;
  .box-card {
    width: 410px;
    margin-right: 30px;
    margin-bottom: 30px;
  }
  .content {
    align-items: flex-start;
    justify-content: flex-start;
    .info {
      line-height: 26px;
    }
    .timeline {
      padding: 0;
      margin-left: 30px;
    }
  }
}
</style>
