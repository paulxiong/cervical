<template>
  <div class="newProject">
    <section class="main">
      <div class="start-train">
        <h2 class="title flex">
          <el-input
            v-model="inputName"
            autofocus
            placeholder="输入描述"
            show-word-limit
            maxlength="30"
            class="input-name"
            @keyup.enter.native="createProject"
          />
          <el-button
            class="start-btn"
            type="danger"
            :disabled="!inputName.length"
            @click="createProject"
          >开始处理</el-button>
        </h2>
      </div>
      <div class="data-model">
        <div class="info flex">
          <section class="param">
            <h4>新建类型</h4>
            <el-radio-group v-model="predictType" size="mini">
              <el-radio-button label="训练" />
              <el-radio-button label="预测" />
            </el-radio-group>
          </section>
          <section class="param">
            <h4>是否有标注</h4>
            <el-radio-group v-model="predictWay" size="mini">
              <el-radio-button label="没标注的图" />
              <el-radio-button label="有标注的图" />
            </el-radio-group>
          </section>
          <section class="param">
            <h4>裁剪大小(像素)</h4>
            <el-radio-group v-model="cutInput" size="mini">
              <el-radio-button label="100" />
              <el-radio-button label="120" />
              <el-radio-button label="150" />
            </el-radio-group>
          </section>
          <section class="param">
            <h4>最长用时(秒)</h4>
            <el-radio-group v-model="useTime" size="mini">
              <el-radio-button label="1800" />
              <el-radio-button label="2400" />
              <el-radio-button label="3000" />
            </el-radio-group>
          </section>
        </div>
        <datasetsCard
          :datasets-info="datasetsInfo"
          :datasets-list="datasetsList"
          @datasetsChange="datasetsChange"
          @cellsTypeChange="cellsTypeChange"
        />
        <modelCard
          v-show="predictType === '预测'"
          :model-info="modelInfo"
          :model-list="modelList"
          @modelChange="modelChange"
        />
      </div>
    </section>
  </div>
</template>

<script>
import modelCard from './model-card'
import datasetsCard from './datasets-card'
import { listdatasets, getListmodel, createProject } from '@/api/cervical'
import { taskStatus, createdBy } from '@/const/const'

export default {
  name: 'Newproject',
  components: { modelCard, datasetsCard },
  data() {
    return {
      predictType: '预测',
      predictWay: '没标注的图',
      cutInput: 100,
      useTime: '1800',
      inputName: '',
      modelList: [],
      cellsList: [],
      modelInfo: {},
      datasetsInfo: {},
      datasetsList: [],
      postCelltypes: [],
      postDatasetsInfo: {},
      postModelInfo: {}
    }
  },
  created() {
    this.getListmodel(10, 0, 1)
    this.getListdatasets(20, 0, 1)
  },
  methods: {
    getListmodel(limit, skip, type) {
      getListmodel({ 'limit': limit, 'skip': skip, 'type': 51 }).then(res => {
        if (res.data.data.total > 0) {
          this.modelList = res.data.data.models
          this.modelInfo = this.modelList[0]
        }
      })
    },
    getListdatasets(limit, skip, order) {
      listdatasets({ 'limit': limit, 'skip': skip, 'order': order }).then(res => {
        if (res.data.data.total > 0) {
          res.data.data.datasets.map(v => {
            v.created_by = createdBy[v.created_by] || '普通用户'
            v.status = taskStatus[v.status]
            v.parameter_cache = v.parameter_cache === 1 ? '使用' : '不使用'
            v.parameter_gray = v.parameter_gray === 1 ? '灰色' : '彩色'
            if (v.status === '完成') {
              this.datasetsList.push(v)
            }
          })
          this.datasetsInfo = this.datasetsList[0]
        }
      })
    },
    createProject() {
      console.log(this.cellsList)
      const postData = this.predictType === '预测' ? {
        celltypes: this.cellsList.length ? this.cellsList : this.datasetsInfo.types,
        desc: this.inputName,
        did: parseInt(this.datasetsInfo.id),
        parameter_mid: parseInt(this.modelInfo.id),
        parameter_resize: parseInt(this.cutInput),
        parameter_time: parseInt(this.useTime),
        parameter_type: this.predictWay === '没标注的图' ? 0 : 1,
        type: 3
      } : {
        celltypes: this.cellsList.length ? this.cellsList : this.datasetsInfo.types,
        desc: this.inputName,
        did: parseInt(this.datasetsInfo.id),
        parameter_resize: parseInt(this.cutInput),
        parameter_time: parseInt(this.useTime),
        parameter_type: this.predictWay === '没标注的图' ? 0 : 1,
        type: 2
      }
      createProject(postData).then(res => {
        this.$router.push({
          path: `/workSpace/details?pid=${res.data.data}&did=${this.datasetsInfo.id}&type=${this.predictType === '预测' ? 3 : 2}`
        })
      })
    },
    datasetsChange(val) {
      this.datasetsInfo = val
    },
    cellsTypeChange(val) {
      this.cellsList = val
    },
    modelChange(val) {
      this.modelInfo = val
    }
  }
}
</script>

<style lang="scss" scoped>
.newProject {
  .info {
    flex-wrap: wrap;
    justify-content: flex-start;
    .param {
      margin-right: 15px;
      h4 {
        margin: 5px 0;
      }
    }
  }
}
</style>
