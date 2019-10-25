<template>
  <div class="home">
    <el-tabs v-model="activeName" class="tabs" @tab-click="handleClick">
      <el-tab-pane label="项目" name="project">
        <projectData :projectlist="projectList" />
      </el-tab-pane>
      <el-tab-pane label="数据集" name="datasets">
        <datasetsData :datasetslist="datasetsList" />
      </el-tab-pane>
      <el-tab-pane label="模型" name="model">
        <modelData :modellist="modelList" />
      </el-tab-pane>
      <el-tab-pane label="回收站" name="recycle">
        <datasetsCard :datalist="datasetsList" />
      </el-tab-pane>
    </el-tabs>
    <!-- <div class="block">
      <el-pagination
        :current-page.sync="currentPage3"
        :page-size="10"
        layout="prev, pager, next, jumper"
        :total="1000"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div> -->
  </div>
</template>

<script>
import projectData from './components/project-data'
import datasetsData from './components/datasets-data'
import modelData from './components/model-data'
import datasetsCard from './components/datasets-card'
import { listdatasets } from '@/api/cervical'
import { taskStatus, createdBy } from '@/const/const'
import { parseTime } from '@/utils/index'

export default {
  name: 'Home',
  components: { projectData, datasetsData, modelData, datasetsCard },
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
        },
        {
          'id': '2',
          'desc': '第二个项目',
          'created_by': '用户一',
          'status': '已完成',
          'score': '98.6',
          'created_at': '2019-10-25T17:00:13Z',
          'model_id': '1',
          'datasets_id': '1'
        },
        {
          'id': '3',
          'desc': '第三个项目',
          'created_by': '管理员',
          'status': '已完成',
          'score': '94.0',
          'created_at': '2019-10-25T11:03:13Z',
          'model_id': '2',
          'datasets_id': '2'
        },
        {
          'id': '4',
          'desc': '第四个项目',
          'created_by': '用户二',
          'status': '未完成',
          'score': '0',
          'created_at': '2019-10-25T06:00:00Z',
          'model_id': '7',
          'datasets_id': '2'
        },
        {
          'id': '5',
          'desc': '第五个项目',
          'created_by': '用户三',
          'status': '已完成',
          'score': '99.0',
          'created_at': '2019-10-25T11:00:13Z',
          'model_id': '1',
          'datasets_id': '1'
        },
        {
          'id': '6',
          'desc': '第六个项目',
          'created_by': '用户四',
          'status': '未完成',
          'score': '0',
          'created_at': '2019-10-25T12:00:13Z',
          'model_id': '3',
          'datasets_id': '4'
        },
        {
          'id': '7',
          'desc': '第七个项目',
          'created_by': '用户五',
          'status': '已完成',
          'score': '98.1',
          'created_at': '2019-10-25T14:53:13Z',
          'model_id': '2',
          'datasets_id': '3'
        },
        {
          'id': '8',
          'desc': '第八个项目',
          'created_by': '管理员',
          'status': '已完成',
          'score': '97.7',
          'created_at': '2019-10-25T15:53:13Z',
          'model_id': '2',
          'datasets_id': '3'
        },
        {
          'id': '9',
          'desc': '第九个项目',
          'created_by': '用户四',
          'status': '已完成',
          'score': '93.6',
          'created_at': '2019-10-25T18:53:13Z',
          'model_id': '2',
          'datasets_id': '3'
        },
        {
          'id': '10',
          'desc': '第十个项目',
          'created_by': '用户六',
          'status': '已完成',
          'score': '98.6',
          'created_at': '2019-10-25T17:53:13Z',
          'model_id': '2',
          'datasets_id': '3'
        },
        {
          'id': '11',
          'desc': '第十一个项目',
          'created_by': '管理员',
          'status': '已完成',
          'score': '93.6',
          'created_at': '2019-10-25T10:00:13Z',
          'model_id': '2',
          'datasets_id': '3'
        },
        {
          'id': '12',
          'desc': '第十二个项目',
          'created_by': '管理员',
          'status': '未完成',
          'score': '0',
          'created_at': '2019-10-25T17:17:13Z',
          'model_id': '2',
          'datasets_id': '3'
        }
      ],
      datasetsList: [],
      modelList: []
    }
  },
  mounted() {
    this.listdatasets(10, 0, 1)
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
    listdatasets(limit, skip, order) {
      listdatasets({ 'limit': limit, 'skip': skip, 'order': order }).then(res => {
        res.data.data.datasets.map(v => {
          v.created_at = parseTime(v.created_at)
          v.updated_at = parseTime(v.updated_at)
          v.processtime = parseTime(v.processtime)
          v.processend = parseTime(v.processend)
          v.created_by = createdBy[v.created_by] || '普通用户'
          v.status = taskStatus[v.status]
          v.parameter_cache = v.parameter_cache === 1 ? '使用' : '不使用'
          v.parameter_gray = v.parameter_gray === 1 ? '灰色' : '彩色'
        })
        this.datasetsList = res.data.data.datasets || []
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.home {
  padding: 0 30px;
}
</style>
