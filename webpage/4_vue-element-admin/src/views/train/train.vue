<template>
  <div class="train">
    <section class="header">
      <el-button
        type="danger"
        size="small"
        class="train-btn"
        @click="handleTrain"
        :disabled="checkboxCell.length<2 || startedTrain === 'ok' || jobResult.status >= 6"
      >开始训练</el-button>
      <div class="cellTypes">
        <div class="progress-info">
          <el-badge is-dot class="badge">状态进度</el-badge>
          <el-progress
            :text-inside="true"
            :stroke-width="26"
            :percentage="percentage"
            status="success"
          ></el-progress>
        </div>
        <el-badge is-dot class="badge">选择细胞类型</el-badge>
        <el-checkbox-group v-model="checkboxCell" size="mini" class="cell-checkbox">
          <el-checkbox v-for="(v, i) in jobResult.types" :key="i" :label="v" :checked="i<=1" border></el-checkbox>
        </el-checkbox-group>
      </div>
    </section>
    <section class="model-info">
      <el-badge is-dot class="badge">模型信息</el-badge>
      <el-button
        type="danger"
        size="small"
        class="save-btn"
        :disabled="!trainInfo.desc"
        @click="saveModel"
      >保存模型</el-button>
      <modelCard :trainInfo="trainInfo" @changeDesc="changeDesc"></modelCard>
    </section>
  </div>
</template>

<script>
import modelCard from './components/model-card'
import { createTrain, getTrainresult, savemodel } from '@/api/cervical'

export default {
  name: 'Train',
  components: { modelCard },
  data() {
    return {
      percentage: 50,
      jobResult: JSON.parse(localStorage.getItem('jobResult')) || [],
      checkboxCell: [],
      trainInfo: {},
      startedTrain: ''
    }
  },
  methods: {
    handleTrain() {
      const postCelltypes = []
      this.checkboxCell.map(v => {
        postCelltypes.push(v.celltype)
      })
      createTrain({
        id: parseInt(this.$route.query.id),
        celltypes: postCelltypes
      }).then(res => {
        this.startedTrain = res.data.data
      })
    },
    getTrainresult() {
      getTrainresult({ 'id': this.$route.query.id }).then(res => {
        this.trainInfo = res.data.data
      })
    },
    changeDesc(val) {
      this.trainInfo.desc = val
    },
    saveModel() {
      savemodel({
        'id': this.trainInfo.did,
        'desc': this.trainInfo.desc
      }).then(res => {
        this.$message({
          message: res.data.data,
          type: 'success'
        })
      })
    }
  },
  mounted() {
    this.getTrainresult()
  }
}
</script>

<style lang="scss" scoped>
.train {
  padding: 0 30px;
  .badge {
    font-weight: bold;
    margin-bottom: 5px;
  }
  .header {
    .progress-info {
      margin-bottom: 20px;
    }
    .train-btn {
      margin: 20px 0;
    }
    .cell-checkbox {
      margin-top: 10px;
    }
    .cellTypes {
      margin-bottom: 20px;
    }
  }
  .save-btn {
    margin-left: 10px;
  }
}
</style>
