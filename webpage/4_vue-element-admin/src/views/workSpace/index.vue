<template>
  <div class="home">
    <el-tabs v-model="activeName" class="tabs" @tab-click="handleClick">
      <el-tab-pane label="项目" name="project">
        <el-button type="primary" @click="goNewTrain">新建数据集</el-button>
        <el-switch
          v-model="switchVal"
          class="switch-btn"
          active-text="训练"
          inactive-text="预测"
          @change="switchChange"
        />
        <section class="project-list">
          <datasetsCard :datalist="dataList" />
        </section>
      </el-tab-pane>
      <el-tab-pane label="模型" name="model">配置管理</el-tab-pane>
      <el-tab-pane label="数据集" name="datasets">角色管理</el-tab-pane>
      <el-tab-pane label="回收站" name="recycle">定时任务补偿</el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import datasetsCard from './components/datasets-card'
import { listdatasets } from '@/api/cervical'
import { taskStatus, typeStatus, taskType, createdBy } from '@/const/const'
import { dateformat3 } from '@/utils/dateformat'

export default {
  name: 'Home',
  components: { datasetsCard },
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
  data() {
    return {
      switchVal: true,
      activeName: 'project',
      dataList: []
    }
  },
  mounted() {
    this.listdatasets(100, 0, 1)
  },
  methods: {
    handleClick(tab, event) {
      console.log(tab, event)
    },
    goNewTrain() {
      this.$router.push({
        path: '/train/newTrain'
      })
    },
    switchChange() {
      this.listdatasets(100, 0, this.switchVal ? 1 : 2)
    },
    listdatasets(limit, skip, type) {
      listdatasets({ 'limit': limit, 'skip': skip, 'type': type }).then(res => {
        res.data.data.datasets.map(v => {
          v.activities = [{
            content: taskStatus[v.status],
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
  padding: 0 30px;
  i {
    color: #666;
    font-size: 14px;
    font-style: normal;
  }
}
</style>
