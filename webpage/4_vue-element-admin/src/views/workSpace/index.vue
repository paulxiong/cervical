<template>
  <div class="home">
    <el-tabs v-model="activeName" class="tabs" @tab-click="handleClick">
      <el-tab-pane label="项目" name="project">
        <el-table
          :data="projectList"
          style="width: 100%"
        >
          <el-table-column type="expand">
            <template slot-scope="props">
              <el-form label-position="left" inline class="table-expand">
                <el-form-item label="项目 ID">
                  <span>{{ props.row.id }}</span>
                </el-form-item>
                <el-form-item label="描述">
                  <span>{{ props.row.desc }}</span>
                </el-form-item>
                <el-form-item label="创建者">
                  <span>{{ props.row.created_by }}</span>
                </el-form-item>
                <el-form-item label="模型 ID">
                  <span>{{ props.row.model_id }}</span>
                </el-form-item>
                <el-form-item label="数据集 ID">
                  <span>{{ props.row.datasets_id }}</span>
                </el-form-item>
                <el-form-item label="状态">
                  <span>{{ props.row.status }}</span>
                </el-form-item>
                <el-form-item label="得分">
                  <span>{{ props.row.score }}</span>
                </el-form-item>
                <el-form-item label="创建时间">
                  <span>{{ props.row.created_at }}</span>
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>
          <el-table-column
            label="项目 ID"
            prop="id"
          />
          <el-table-column
            label="描述"
            prop="desc"
          />
          <el-table-column
            label="创建者"
            prop="created_by"
          />
          <el-table-column
            label="得分"
            prop="score"
          />
          <el-table-column
            label="状态"
            prop="status"
          />
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="数据集" name="datasets">
        数据集
      </el-tab-pane>
      <el-tab-pane label="模型" name="model">
        模型
      </el-tab-pane>
      <el-tab-pane label="回收站" name="recycle">
        回收站
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
// import datasetsCard from './components/datasets-card'
import { listdatasets } from '@/api/cervical'
import { taskStatus, typeStatus, taskType, createdBy } from '@/const/const'
import { dateformat3 } from '@/utils/dateformat'

export default {
  name: 'Home',
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
  data() {
    return {
      switchVal: true,
      activeName: 'project',
      projectList: [
        {
          'id': '1',
          'desc': '第一个项目',
          'created_by': '管理员',
          'status': '已完成',
          'score': '96.6',
          'created_at': '2019-10-25T10:53:13Z',
          'model_id': '2',
          'datasets_id': '3'
        }
      ],
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
  .table-expand {
    font-size: 0;
  }
  .table-expand label {
    width: 90px;
    color: #99a9bf;
  }
  .table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
  }
}
</style>
