<template>
  <div class="train">
    <section class="header flex">
      <el-badge is-dot class="badge">训练进度</el-badge>
      <el-progress
        :text-inside="true"
        :stroke-width="26"
        :percentage="percentage"
        class="progress"
        status="success"
      ></el-progress>
      <el-button
        type="danger"
        class="train-btn"
        @click="handleTrain"
        :disabled="checkboxCell.length<2 || startedTrain === 'ok' || jobResult.status >= 6"
      >开始训练</el-button>
    </section>
    <section class="model-info">
      <el-badge is-dot class="badge">选择细胞类型</el-badge>
      <el-checkbox-group v-model="checkboxCell" size="mini" class="cell-checkbox">
        <el-checkbox v-for="(v, i) in jobResult.types" :key="i" :label="v | filtersCheckbox" :checked="i<=1" border></el-checkbox>
      </el-checkbox-group>
      <el-badge is-dot class="badge">模型信息</el-badge>
      <el-button
        type="danger"
        size="small"
        class="save-btn"
        :disabled="!trainInfo.desc"
        @click="saveModel"
        v-if="showSaveBtn"
      >保存模型</el-button>
      <modelCard :trainInfo="trainInfo" @changeDesc="changeDesc"></modelCard>
    </section>
  </div>
</template>

<script>
import modelCard from './components/model-card'
import { createTrain, getTrainresult, savemodel } from '@/api/cervical'
import { cellsType } from '@/const/const'

export default {
  name: 'Train',
  components: { modelCard },
  data() {
    return {
      percentage: 50,
      showSaveBtn: true,
      jobResult: JSON.parse(localStorage.getItem('jobResult')) || [],
      checkboxCell: [],
      trainInfo: {},
      startedTrain: ''
    }
  },
  filters: {
    filtersCheckbox(val) {
      return `${cellsType[val.celltype]}: ${val.labelcnt}`
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
        this.showSaveBtn = false
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
  margin-bottom: 100px;
  .badge {
    font-weight: bold;
  }
  .header {
    border: 1px solid #ccc;
    background: #304155;
    width: 100%;
    justify-content: flex-end;
    position: fixed;
    bottom: -1px;
    right: -1px;
    padding: 20px 30px;
    .badge {
      color: #fff;
    }
    .progress {
      width: 70%;
      margin: 0 10px;
    }
    .train-btn {
      width: 10%;
    }
  }
  .model-info {
    padding: 0 30px;
    margin-top: 20px;
    .cell-checkbox {
      margin-top: 5px;
      margin-bottom: 20px;
    }
    .badge {
      margin-bottom: 5px;
    }
  }
  .save-btn {
    margin-left: 10px;
  }
}
</style>
