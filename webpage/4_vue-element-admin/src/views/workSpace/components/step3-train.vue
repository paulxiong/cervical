<template>
  <div class="start-train">
    <h2 class="title flex">
      <el-input
        v-model="inputName"
        autofocus
        placeholder="输入描述"
        show-word-limit
        maxlength="30"
        class="input-name"
        @keyup.enter.native="goTrain"
      />
      <el-button
        class="start-btn"
        type="danger"
        :disabled="!inputName.length"
        :loading="loading"
        @click="goTrain"
      >开始处理</el-button>
      <el-button class="errInfo-btn" type="info" size="mini" @click="goBack">重新编辑</el-button>
    </h2>
    <section class="train-box-info">
      <el-card shadow="hover">
        <div class="info-header flex">
          <el-badge is-dot class="badge">训练集</el-badge>
          <el-tag
            class="info-tag"
            effect="dark"
            size="small"
            type="info"
          >{{ postData.type===1?'训练':'预测' }}</el-tag>
        </div>
        <div class="info-list flex">
          <section class="info">
            <i>批次</i>
            <b>{{ postData.batchids }}</b>
          </section>
          <section class="info">
            <i>病例</i>
            <b>{{ postData.medicalids }}</b>
          </section>
          <section class="info">
            <i>细胞类型</i>
            <b>['1_Norm', '7_ASCUS']</b>
          </section>
          <section class="info">
            <i>n/p比例</i>
            <b>{{ countNP.countn }}/{{ countNP.countp }}</b>
          </section>
        </div>
      </el-card>
      <el-card v-if="modelInfo.model.id" style="margin-top:20px;" shadow="hover">
        <div class="info-header flex">
          <el-badge is-dot class="badge">模型及参数</el-badge>
          <el-tag
            class="info-tag"
            effect="dark"
            size="small"
            type="info"
          >{{ modelInfo.model.type | filterModelType }}</el-tag>
        </div>
        <div class="info-list flex">
          <section class="info">
            <i>模型ID</i>
            <b>{{ modelInfo.model.id }}</b>
          </section>
          <section class="info">
            <i>模型</i>
            <b>{{ modelInfo.model.desc }}</b>
          </section>
          <section class="info">
            <i>图片色彩</i>
            <b>{{ modelInfo.imgColor }}</b>
          </section>
          <section class="info">
            <i>裁剪大小</i>
            <b>{{ modelInfo.cutSize }}</b>
          </section>
          <section class="info">
            <i>Precision</i>
            <b>{{ modelInfo.model.precision }}</b>
          </section>
          <section class="info">
            <i>Recall</i>
            <b>{{ modelInfo.model.recall }}</b>
          </section>
        </div>
      </el-card>
    </section>
  </div>
</template>

<script>
import { createdataset } from '@/api/cervical'
import { modelType } from '@/const/const'

export default {
  name: 'StartTrain',
  components: {},
  filters: {
    filterModelType(value) {
      return modelType[value]
    }
  },
  data() {
    return {
      loading: false,
      inputName: '',
      postData: JSON.parse(localStorage.getItem('POST_DATA')),
      countNP: JSON.parse(localStorage.getItem('countNP')),
      modelInfo: JSON.parse(localStorage.getItem('MODEL_INFO'))
    }
  },
  methods: {
    goTrain() {
      this.loading = true
      this.postData['desc'] = this.inputName
      createdataset(this.postData).then(res => {
        this.$router.push({
          path: `/train/detailsTrain?id=${res.data.data}`
        })
        this.loading = false
      })
    },
    goBack() {
      this.$parent.stepBack()
    }
  }
}
</script>

<style lang="scss" scoped>
.start-train {
  .title {
    justify-content: flex-start;
  }
  .input-name {
    width: 500px;
  }
  .badge {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 10px;
  }
  .info-tag {
    margin-left: 10px;
  }
  i {
    color: #666;
    font-style: normal;
    margin-right: 10px;
  }
  b {
    font-size: 22px;
  }
  .link {
    line-height: 20px;
  }
  .errInfo-btn {
    font-size: 12px;
    margin-left: 10px;
  }
  .start-btn {
    margin-left: 10px;
  }
  .info-header {
    justify-content: flex-start;
    align-items: flex-start;
  }
  .info-list {
    justify-content: space-around;
    flex-wrap: wrap;
    .info {
      width: 50%;
      overflow: hidden;
      text-overflow: ellipsis;
      margin: 10px 0;
    }
  }
}
</style>
