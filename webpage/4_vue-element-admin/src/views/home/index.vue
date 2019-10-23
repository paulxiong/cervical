<template>
  <div class="home">
    <h3>
      我的数据集
      <el-switch
        v-model="switchVal"
        class="switch-btn"
        active-text="训练"
        inactive-text="预测"
        @change="switchChange"
      />
      <el-button type="primary" @click="goNewTrain">新建数据集</el-button>
    </h3>
    <section class="project-list flex">
      <el-card
        v-for="(v,i) in dataList"
        :key="i"
        class="box-card"
        :style="v.status === 3 || v.status === 5 || v.status === 8 ?'border:1px dashed #fc4b4e;box-shadow: 3px 3px 10px #fc4b4e;':''"
        :shadow="v.status === 3 || v.status === 5 || v.status === 8 ?'always':'hover'"
      >
        <div slot="header" class="clearfix">
          <span>{{ v.desc }}</span>
          <el-button
            style="float: right; padding: 3px 0"
            type="text"
            @click="goDetailsTrain(v)"
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
    </section>
  </div>
</template>

<script>
import { listdatasets } from '@/api/cervical'
import { taskStatus, typeStatus, taskType, createdBy } from '@/const/const'
import { dateformat3 } from '@/utils/dateformat'

export default {
  name: 'Home',
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
    }
  },
  data() {
    return {
      switchVal: true,
      dataList: []
    }
  },
  mounted() {
    this.listdatasets(100, 0, 1)
  },
  methods: {
    goNewTrain() {
      this.$router.push({
        path: '/train/newTrain'
      })
    },
    goDetailsTrain(v) {
      localStorage.setItem('isPredict', v.type)
      this.$router.push({
        path: `/train/detailsTrain?id=${v.id}`
      })
    },
    switchChange() {
      this.listdatasets(100, 0, this.switchVal ? 1 : 2)
    },
    listdatasets(limit, skip, type) {
      listdatasets({ 'limit': limit, 'skip': skip, 'type': type }).then(res => {
        res.data.data.datasets.map(v => {
          v.activities = [{
            content: taskStatus[v.status].status,
            type: 'success',
            size: 'large',
            icon: 'el-icon-circle-check',
            timestamp: dateformat3(v.processtime)
          }, {
            content: '开始训练',
            type: 'warning',
            size: 'large',
            icon: 'el-icon-timer',
            timestamp: dateformat3(v.traintime)
          }, {
            content: '创建成功',
            type: 'primary',
            size: 'large',
            icon: 'el-icon-s-promotion',
            timestamp: dateformat3(v.created_at)
          }]
        })
        this.dataList = res.data.data.datasets || []
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.home {
  padding: 30px;
  .switch-btn {
    position: absolute;
    right: 80px;
  }
  i {
    color: #666;
    font-size: 14px;
    font-style: normal;
  }
  .project-list {
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
}
</style>
