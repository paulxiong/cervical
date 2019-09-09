<template>
  <div class="start-train">
    <h2 class="flex">
      请确认训练信息，然后
      <el-button class="start-btn" type="danger" @click="goTrain">开始训练</el-button>
      <i class="errInfo-btn">
        若信息有误，需要
        <el-button type="info" size="mini" @click="goBack">重新编辑</el-button>
      </i>
    </h2>
    <section class="train-box-info flex">
      <section class="img tagContent">
        <el-badge is-dot class="badge">训练集</el-badge>
        <div class="img-list info-list">
          <i>批次 :</i> fujianfuyou
          <br />
          <i>病例 :</i> 18237,28374,12943,34512
          <br />
          <i>图片 :</i>
          <el-link class="link" type="primary">点击查看全部<i class="el-icon-view el-icon--right"></i></el-link>
          <br />
          <i>医生标注 :</i> 2345asd.csv
          <br />
          <i>细胞类型 :</i> 1_Norm, 2_LSIL, 7_ASCUS
          <br />
          <i>N/p比例 :</i> 0.5
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
    }
  },
  methods: {
    goTrain() {
      let postData = JSON.parse(localStorage.getItem('POST_DATA'))
      createdataset(postData).then(res => {
        this.$router.push({
          path: '/'
        })
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
