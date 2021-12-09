<template>
  <div class="start-train">
    <h2 class="title flex">
      <el-input
        v-model="inputName"
        autofocus
        :placeholder="$t('workspace.dataDescription')"
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
      >{{ $t('workspace.dataStartToSegmentate') }}</el-button>
    </h2>
    <section class="train-box-info">
      <el-card shadow="hover">
        <div class="info-header flex">
          <el-badge is-dot class="badge">{{ $t('workspace.dataTrainingSet') }}</el-badge>
          <el-tag
            class="info-tag"
            effect="dark"
            size="small"
            type="info"
          >{{ modelInfo.type }}</el-tag>
        </div>
        <div class="info-list flex">
          <section class="info" style="width: 48%;height: 50px;overflow: auto;margin-right: 2%;">
            <i>{{ $t('workspace.dataBatch') }}</i>
            <b>{{ postData.batchids }}</b>
          </section>
          <section class="info" style="width: 50%;height: 50px;overflow: auto;">
            <i>{{ $t('workspace.dataCase') }}</i>
            <b>{{ postData.medicalids }}</b>
          </section>
          <section class="info">
            <i>{{ $t('workspace.dataDescription2') }}</i>
            <b>{{ inputName }}</b>
          </section>
          <section class="info">
            <i>{{ $t('workspace.dataProportion') }}</i>
            <b>{{ countNP.countn }}/{{ countNP.countp }}</b>
          </section>
        </div>
      </el-card>
      <el-card v-if="modelInfo.model.id" style="margin-top:20px;" shadow="hover">
        <div class="info-header flex">
          <el-badge is-dot class="badge">{{ $t('workspace.dataModelParameters') }}</el-badge>
          <el-tag
            class="info-tag"
            effect="dark"
            size="small"
            type="info"
          >{{ modelInfo.model.type | filterModelType }}</el-tag>
        </div>
        <div class="info-list flex">
          <section class="model-info">
            <i>{{ $t('workspace.dataModelID') }}</i>
            <b>{{ modelInfo.model.id }}</b>
          </section>
          <section class="model-info">
            <i>{{ $t('workspace.dataModel') }}</i>
            <b>{{ modelInfo.model.desc }}</b>
          </section>
          <section class="model-info">
            <i>{{ $t('workspace.dataUseCache') }}</i>
            <b>{{ modelInfo.cache }}</b>
          </section>
          <!-- <section class="model-info">
            <i>损失</i>
            <b>{{ modelInfo.model.loss }}</b>
          </section> -->
          <section class="model-info">
            <i>{{ $t('workspace.dataColor2') }}</i>
            <b>{{ modelInfo.imgColor }}</b>
          </section>
          <section class="model-info">
            <i>{{ $t('workspace.dataSize') }}</i>
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
            <i>{{ $t('workspace.dataUpdateTime') }}</i>
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
      inputName: 'Default Name',
      postData: JSON.parse(localStorage.getItem('POST_DATA')),
      countNP: JSON.parse(localStorage.getItem('countNP')) || {
        countn: 0,
        countp: 0
      },
      modelInfo: JSON.parse(localStorage.getItem('MODEL_INFO'))
    }
  },
  methods: {
    goDetail() {
      this.loading = true
      this.postData['desc'] = this.inputName
      this.postData['parameter_cache'] = this.modelInfo.cache === this.$t('workspace.dataCacheYes') ? 1 : 0
      this.postData['parameter_gray'] = this.modelInfo.imgColor === this.$t('workspace.dataColorGray') ? 1 : 0
      this.postData['parameter_mid'] = this.modelInfo.model.id
      console.log("boostx in goDetail: " + this.modelInfo.model.id)
      this.postData['parameter_size'] = parseInt(this.modelInfo.cutSize)
      this.postData['parameter_type'] = parseInt(this.modelInfo.type.slice(0, 1))
      createdataset(this.postData).then(res => {
        this.$router.push({
          path: `/workSpace/details?did=${res.data.data}`
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
