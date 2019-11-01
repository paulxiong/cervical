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
        @keyup.enter.native="goDetail"
      />
      <el-button
        class="start-btn"
        type="danger"
        :disabled="!inputName.length"
        :loading="loading"
        @click="goDetail"
      >开始处理</el-button>
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
          >{{ modelInfo.type }}</el-tag>
        </div>
        <div class="info-list flex">
          <section class="info" style="width: 48%;height: 50px;overflow: auto;margin-right: 2%;">
            <i>批次</i>
            <b>{{ postData.batchids }}</b>
          </section>
          <section class="info" style="width: 50%;height: 50px;overflow: auto;">
            <i>病例</i>
            <b>{{ postData.medicalids }}</b>
          </section>
          <section class="info">
            <i>描述</i>
            <b>{{ inputName }}</b>
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
          <section class="model-info">
            <i>模型ID</i>
            <b>{{ modelInfo.model.id }}</b>
          </section>
          <section class="model-info">
            <i>模型</i>
            <b>{{ modelInfo.model.desc }}</b>
          </section>
          <section class="model-info">
            <i>是否使用缓存</i>
            <b>{{ modelInfo.cache }}</b>
          </section>
          <!-- <section class="model-info">
            <i>损失</i>
            <b>{{ modelInfo.model.loss }}</b>
          </section> -->
          <section class="model-info">
            <i>背景色</i>
            <b>{{ modelInfo.imgColor }}</b>
          </section>
          <section class="model-info">
            <i>裁剪大小</i>
            <b>{{ modelInfo.cutSize }}</b>
          </section>
          <!-- <section class="model-info">
            <i>Precision</i>
            <b>{{ modelInfo.model.precision }}</b>
          </section>
          <section class="model-info">
            <i>Recall</i>
            <b>{{ modelInfo.model.recall }}</b>
          </section> -->
          <section class="model-info">
            <i>最后更新时间</i>
            <b>{{ modelInfo.model.updated_at | filterDate }}</b>
          </section>
        </div>
      </el-card>
    </section>
  </div>
</template>

<script>
import { createdataset } from '@/api/cervical'
import { modelType } from '@/const/const'
import { parseTime } from '@/utils/index'

export default {
  name: 'StartTrain',
  components: {},
  filters: {
    filterModelType(value) {
      return modelType[value]
    },
    filterDate(value) {
      return parseTime(value)
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
    goDetail() {
      this.loading = true
      this.postData['desc'] = this.inputName
      this.postData['parameter_cache'] = this.modelInfo.cache === '是' ? 1 : 0
      this.postData['parameter_gray'] = this.modelInfo.imgColor === '灰色' ? 1 : 0
      this.postData['parameter_mid'] = this.modelInfo.model.id
      this.postData['parameter_size'] = parseInt(this.modelInfo.cutSize)
      this.postData['parameter_type'] = parseInt(this.modelInfo.type.slice(0, 1))
      createdataset(this.postData).then(res => {
        this.$router.push({
          path: `/workSpace/details?id=${res.data.data}`
        })
        this.loading = false
      })
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
    justify-content: space-between;
    flex-wrap: wrap;
    i {
      color: #666;
      font-style: normal;
      font-size: 14px;
    }
    b {
      font-size: 14px;
    }
    .model-info {
      width: calc(100%/3);
      overflow: hidden;
      text-overflow: ellipsis;
      margin: 5px 0;
    }
    .info {
      width: 50%;
      overflow: hidden;
      text-overflow: ellipsis;
      margin: 5px 0;
    }
  }
}
</style>
