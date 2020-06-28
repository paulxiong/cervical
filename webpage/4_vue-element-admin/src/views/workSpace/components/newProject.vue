<template>
  <div class="newProject">
    <section class="main">
      <div class="start-train">
        <h2 class="title flex">
          <el-input
            v-model="inputName"
            autofocus
            :placeholder="$t('workspace.projectEnterDesc')"
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
          >{{ $t('workspace.projectStart') }}</el-button>
        </h2>
      </div>
      <div class="data-model">
        <div class="info flex">
          <section class="param">
            <h4>{{ $t('workspace.projectNewType') }}</h4>
            <el-radio-group v-model="predictType" size="mini">
              <el-radio-button :label="$t('workspace.projectNewTypeTrain')" />
              <el-radio-button :label="$t('workspace.projectNewTypePredict')" />
            </el-radio-group>
          </section>
          <section class="param">
            <h4>{{ $t('workspace.projectNewLabel') }}</h4>
            <el-radio-group v-model="predictWay" size="mini">
              <el-radio-button :label="$t('workspace.projectNewNoLabel')" />
              <el-radio-button :label="$t('workspace.projectNewTypeLabelled')" />
            </el-radio-group>
          </section>
          <section class="param">
            <h4>{{ $t('workspace.projectNewSize') }}</h4>
            <el-radio-group v-model="cutInput" size="mini">
              <el-radio-button label="100" />
              <el-radio-button label="150" />
              <el-radio-button label="224" />
            </el-radio-group>
          </section>
          <section class="param">
            <h4>{{ $t('workspace.projectNewTime') }}</h4>
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
          v-if="predictType === $t('workspace.projectNewTypePredict')"
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
      predictType: '',
      predictWay: '',
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
    this.getListmodel(1000, 0, 1)
    this.getListdatasets(10000, 0, 1)
    this.predictType = this.$t('workspace.projectNewTypePredict')
    this.predictWay = this.$t('workspace.projectNewNoLabel')
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
            v.created_by = createdBy[v.created_by] || this.$t('workspace.projectNewUser')
            v.status = taskStatus[v.status]
            v.parameter_cache = v.parameter_cache === 1 ? this.$t('workspace.projectNewCache') : this.$t('workspace.projectNewNoCache')
            v.parameter_gray = v.parameter_gray === 1 ? this.$t('workspace.projectNewGray') : this.$t('workspace.projectNewColor')
            if (v.status === taskStatus[4]) {
              this.datasetsList.push(v)
            }
          })
          this.datasetsInfo = this.datasetsList[0]
        }
      })
    },
    createProject() {
      const postData = this.predictType === this.$t('workspace.projectNewTypePredict') ? {
        celltypes: this.cellsList.length ? this.cellsList : this.datasetsInfo.types,
        desc: this.inputName,
        did: parseInt(this.datasetsInfo.id),
        parameter_mid: parseInt(this.modelInfo.id),
        parameter_resize: parseInt(this.cutInput),
        parameter_time: parseInt(this.useTime),
        parameter_type: this.predictWay === this.$t('workspace.projectNewNoLabel') ? 0 : 1,
        type: 3
      } : {
        celltypes: this.cellsList.length ? this.cellsList : this.datasetsInfo.types,
        desc: this.inputName,
        did: parseInt(this.datasetsInfo.id),
        parameter_resize: parseInt(this.cutInput),
        parameter_time: parseInt(this.useTime),
        parameter_type: this.predictWay === this.$t('workspace.projectNewTypeLabelled') ? 0 : 1,
        type: 2
      }
      createProject(postData).then(res => {
        localStorage.setItem('details_title', this.inputName)
        this.$router.push({
          path: `/workSpace/details?pid=${res.data.data}&did=${this.datasetsInfo.id}&type=${this.predictType === this.$t('workspace.projectNewTypePredict') ? 3 : 2}`
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
