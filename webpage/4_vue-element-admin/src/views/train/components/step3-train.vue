<template>
  <div class="start-train">
    <h2 class="flex">
      请<el-input v-model="inputName" autofocus placeholder="为数据集取个名字吧" show-word-limit maxlength="10" @keyup.enter.native="goTrain" class="inputName"></el-input>，然后
      <el-button class="start-btn" type="danger" :disabled="!inputName.length" :loading="loading" @click="goTrain">开始处理</el-button>
      <i class="errInfo-btn">
        若信息有误，需要
        <el-button type="info" size="mini" @click="goBack">重新编辑</el-button>
      </i>
    </h2>
    <section class="train-box-info flex">
      <section class="img tagContent">
        <el-badge is-dot class="badge">训练集</el-badge>
        <div class="img-list info-list">
          <i>批次 :</i> {{postData.batchids}}
          <br />
          <i>病例 :</i> {{postData.medicalids}}
          <br />
          <i>图片 :</i>
          <el-link class="link" type="primary">点击查看全部<i class="el-icon-view el-icon--right"></i></el-link>
          <br />
          <i>医生标注 :</i> 20192345asd.csv
          <br />
          <i>细胞类型 :</i> 1_Norm, 2_LSIL, 7_ASCUS
          <br />
          <i>n/p比例 :</i> {{countNP.countn}}/{{countNP.countp}}
        </div>
      </section>

      <section class="box2">
        <section class="model tagContent">
          <el-badge is-dot class="badge">模型及参数</el-badge>
          <div class="model-info info-list">
            <i>模型 :</i> Cell_2012843923923
            <br />
            <i>裁剪大小 :</i> 100
          </div>
        </section>

        <section class="train tagContent">
          <el-badge is-dot class="badge">运行</el-badge>
          <div class="train-info info-list">
            <i>时长 :</i> 15min ~ 20min
            <br />
            <i>服务器 :</i> lambda-computer
          </div>
        </section>
      </section>
    </section>
  </div>
</template>

<script>
import { createdataset } from '@/api/cervical'
export default {
  name: 'start-train',
  components: {},
  data() {
    return {
      loading: false,
      inputName: '',
      postData: JSON.parse(localStorage.getItem('POST_DATA')) || {},
      countNP: JSON.parse(localStorage.getItem('countNP')) || {}
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
.inputName {
  width: 200px;
  margin: 0 7px;
}
.start-train {
  .badge {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 10px;
  }
  i {
    color: #666;
    font-size: 14px;
  }
  .link {
    line-height: 20px;
  }
  .errInfo-btn {
    font-size: 12px;
    margin-left: 30px;
  }
  .start-btn {
    margin-left: 10px;
  }
  .tagContent {
    width: 300px;
    padding: 20px;
    box-shadow: 4px 2px 2px #ccc;
    border: 1px solid #ccc;
    border-radius: 20px;
  }
  .train-box-info {
    flex-wrap: wrap;
    align-items: flex-start;
  }
  .box2 {
    margin-left: 30px;
    .train {
      margin-top: 30px;
    }
  }
  .info-list {
    line-height: 36px;
  }
}
</style>
