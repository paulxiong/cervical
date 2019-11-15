<template>
  <div class="train">
    <!-- <section class="header flex">
      <el-badge is-dot class="badge">训练进度</el-badge>
      <el-progress
        :text-inside="true"
        :stroke-width="26"
        :percentage="percentage"
        class="progress"
        status="success"
      />
    </section> -->
    <section v-loading="loading" :element-loading-text="loadingtext" class="model-info">
      <div v-if="modelInfo.path" class="model-box">
        <el-badge is-dot class="badge">模型信息</el-badge>
        <modelCard :model-info="modelInfo" :save="save" />
      </div>
    </section>
  </div>
</template>

<script>
import modelCard from './components/model-card'
import { getTrainresult, getPercent } from '@/api/cervical'
import { cellsType } from '@/const/const'
let timer

export default {
  name: 'Train',
  components: { modelCard },
  filters: {
    filtersCheckbox(val) {
      return `${val.celltype} ${cellsType[val.celltype]}: ${val.labelcnt}`
    }
  },
  data() {
    return {
      percentage: 0,
      save: 'save',
      modelInfo: {},
      startedTrain: '',
      loading: true,
      ETA: 10,
      status: 0,
      loadingtext: '正在执行'
    }
  },
  created() {
    this.getPercent()
    this.getTrainresult()
    this.loopGetPercent()
  },
  methods: {
    getTrainresult() {
      getTrainresult({ 'id': this.$route.query.pid }).then(res => {
        this.modelInfo = res.data.data
      })
    },
    getPercent() {
      // type 0 未知 1 数据集处理 2 训练 3 预测
      getPercent({ id: this.$route.query.pid, type: 2 }).then(res => {
        this.percentage = res.data.data.percent
        this.status = res.data.data.status
        this.ETA = res.data.data.ETA
        if ((this.percentage === 100) || (this.status >= 3) || (this.ETA === 0)) {
          this.loading = false
          clearInterval(timer)
        } else {
          this.loadingtext = '预计还需要' + this.ETA + '秒'
        }
      })
    },
    /**
     * 定时器轮训百分比
     */
    loopGetPercent() {
      timer = setInterval(() => {
        if ((this.percentage === 100) || (this.status >= 3) || (this.ETA === 0)) {
          this.getTrainresult()
          this.getPercent()
          location.reload()
          clearInterval(timer)
        }
      }, 5000)
    }
  },
  beforedestroy() {
    clearInterval(timer)
  }
}
</script>

<style lang="scss" scoped>
.train {
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
    padding: 10px 0;
    z-index: 999;
    .badge {
      color: #fff;
    }
    .progress {
      width: 70%;
      margin: 0 10px;
    }
    .train-btn {
      width: 100px;
      margin-right: 30px;
    }
  }
  .model-info {
    padding: 0 30px;
    margin-top: 7px;
    height: 500px;
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
