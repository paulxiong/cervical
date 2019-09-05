<template>
  <div class="home">
    <h3>我的数据集 <el-button type="primary" @click="goNewTrain">新建数据集</el-button></h3>
    <section class="project-list flex">
      <el-card v-for="(v,i) in dataList" :key="i" class="box-card" shadow="hover">
        <div slot="header" class="clearfix">
          <span>{{v.desc}}</span>
          <el-button style="float: right; padding: 3px 0" type="text" @click="goDetailsTrain(v.id)">查看详情</el-button>
        </div>
        
        <div class="content flex">
          <div class="info">
            <i>id :</i> {{v.id}}<br/>
            <i>目录 :</i> {{v.dir}}<br/>
            <i>创建者 :</i> {{v.created_by}}<br/>
            <i>类型 :</i> {{v.type | filtersType}}<br/>
            <i>状态 :</i> {{v.status | filtersTaskStatus}}<br/>
            <!-- <i>批次 :</i> fujianfuyou<br/>
            <i>病例 :</i> 18237,28374,12943, ...<br/>
            <i>图片 :</i> <el-link type="primary">请进入详情查看</el-link><br/>
            <i>医生标注 :</i> 2345asd.csv<br/>
            <i>细胞类型 :</i> 1_Norm, 7_ASCUS, ...<br/>
            <i>n/p比例 :</i> 0.5 -->
          </div>
          <el-timeline :reverse="reverse" class="timeline">
            <el-timeline-item
              v-for="(activity, index) in v.activities"
              :icon="activity.icon"
              :color="activity.color"
              :type="activity.type"
              :key="index"
              :timestamp="activity.timestamp">
              {{activity.content}}
            </el-timeline-item>
          </el-timeline>
        </div>
      </el-card>
    </section>
  </div>
</template>

<script>
import { listdatasets } from '@/api/cervical'
import { taskStatus, typeStatus } from '@/const/const'
import { dateformat2 } from '@/utils/dateformat'

export default {
  name: "home",
  components: {},
  data() {
    return {
      reverse: true,
      dataList: []
    }
  },
  filters: {
    filtersTaskStatus(value) {
      return taskStatus[value].status
    },
    filtersType(value) {
      return typeStatus[value].status
    }
  },
  methods: {
    goNewTrain() {
      this.$router.push({
        path: '/train/newTrain'
      })
    },
    goDetailsTrain(id) {
      this.$router.push({
        path: `/train/detailsTrain?id=${id}`
      })
    },
    listdatasets(limit, skip) {
      listdatasets({ 'limit': limit, 'skip': skip }).then(res => {
        res.data.data.datasets.map(v => {
          v.activities = [{
            content: taskStatus[v.status].status,
            type: 'success',
            size: 'large',
            icon: 'el-icon-circle-check',
            timestamp: dateformat2(v.start_at)
          }, {
            content: '开始训练',
            type: 'warning',
            size: 'large',
            icon: 'el-icon-timer',
            timestamp: dateformat2(v.start_at)
          }, {
            content: '创建成功',
            type: 'primary',
            size: 'large',
            icon: 'el-icon-s-promotion',
            timestamp: dateformat2(v.created_at)
          }]
          // v.activities = [{
          //   content: '训练完成',
          //   type: 'success',
          //   size: 'large',
          //   icon: 'el-icon-circle-check',
          //   timestamp: dateformat2(v.start_at)
          // }, {
          //   content: '开始训练',
          //   type: 'warning',
          //   size: 'large',
          //   icon: 'el-icon-timer',
          //   timestamp: dateformat2(v.start_at)
          // }, {
          //   content: '创建成功',
          //   type: 'primary',
          //   size: 'large',
          //   icon: 'el-icon-s-promotion',
          //   timestamp: dateformat2(v.created_at)
          // }]
        })
        this.dataList = res.data.data.datasets || []
      })
    }
  },
  mounted() {
    this.listdatasets(100, 0)
  }
}
</script>

<style lang="scss" scoped>
.home {
  padding: 30px;
  i {
    color: #666;
    font-size: 14px;
  }
  .project-list {
    justify-content: flex-start;
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
        margin-right: 50px;
      }
      .timeline {
        padding: 0;
      }
    }
  }
}
</style>
