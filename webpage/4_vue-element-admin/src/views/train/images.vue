<template>
  <div class="images">
    <section class="header">
      <div class="title">
        <h2>IMAGES</h2>
        <section class="info-box">
          <div class="input-info info">
            <el-badge is-dot class="badge">输入信息</el-badge>
            <div class="img-list info-list flex">
              <i>批次 :</i> fujianfuyou
              <i>病例 :</i> 18237,28374,12943,34512
              <i>图片 :</i><el-link class="link" type="primary">点击查看全部</el-link>
              <i>医生标注 :</i> 2345asd.csv
              <i>细胞类型 :</i> 1_Norm, 2_LSIL, 7_ASCUS
              <i>N/p比例 :</i> 0.5
            </div>
          </div>
          <div class="progress-info">
            <el-badge is-dot class="badge">状态进度</el-badge>
            <el-progress class="progress" :text-inside="true" :stroke-width="26" :percentage="percentage"  status="success"></el-progress>
          </div>
        </section>
      </div>
    </section>
    <el-divider><i class="el-icon-picture"></i> 所有图片</el-divider>
    <section class="main">
      <el-tabs tab-position="left" @tab-click="tabClick">
        <el-tab-pane label="(step0) 原始数据">
          <el-image
            class="img"
            v-for="(img,idx) in input_datasets_img"
            :key="idx"
            :src="hosturlpath200 + dir + img"
            lazy
          >
            <div slot="error" class="image-slot">
              <i class="el-icon-picture-outline"></i>
            </div>
          </el-image>
        </el-tab-pane>
        <el-tab-pane label="(step1) 去噪后的数据">
          <el-image
            class="img"
            v-for="(img,idx) in input_datasets_denoising"
            :key="idx"
            :src="hosturlpath200 + dir + img"
            lazy
          >
            <div slot="error" class="image-slot">
              <i class="el-icon-picture-outline"></i>
            </div>
          </el-image>
        </el-tab-pane>
        <el-tab-pane label="(step2) mask图片">
          <el-image
            class="img"
            v-for="(img,idx) in middle_mask"
            :key="idx"
            :src="hosturlpath200 + dir + img"
            lazy
          >
            <div slot="error" class="image-slot">
              <i class="el-icon-picture-outline"></i>
            </div>
          </el-image>
        </el-tab-pane>
        <el-tab-pane label="(step3) 输出数据crop_preview">
          <el-image
            class="img"
            v-for="(img,idx) in output_datasets_crop_preview"
            :key="idx"
            :src="hosturlpath200 + dir + img"
            lazy
          >
            <div slot="error" class="image-slot">
              <i class="el-icon-picture-outline"></i>
            </div>
          </el-image>
        </el-tab-pane>
        <el-tab-pane label="(step3) 输出数据crop N">
          <el-image
            class="img"
            v-for="(img,idx) in output_datasets_crop_n"
            :key="idx"
            :src="hosturlpath200 + dir + img"
            lazy
          >
            <div slot="error" class="image-slot">
              <i class="el-icon-picture-outline"></i>
            </div>
          </el-image>
        </el-tab-pane>
        <el-tab-pane label="(step3) 输出数据crop P">
          <el-image
            class="img"
            v-for="(img,idx) in output_datasets_crop_p"
            :key="idx"
            :src="hosturlpath200 + dir + img"
            lazy
          >
            <div slot="error" class="image-slot">
              <i class="el-icon-picture-outline"></i>
            </div>
          </el-image>
        </el-tab-pane>
      </el-tabs>
    </section>
  </div>
</template>

<script>
import { getjobresult } from "@/api/cervical";
import { ImgServerUrl } from "@/const/config";

export default {
  name: "images",
  components: {},
  data() {
    return {
      percentage: 0,
      dir: 'dsEoM8RR/',
      hosturlpath16: ImgServerUrl + "/unsafe/32x0/scratch/",
      hosturlpath64: ImgServerUrl + "/unsafe/640x0/scratch/",
      hosturlpath200: ImgServerUrl + "/unsafe/200x0/scratch/",
      hosturlpath645: ImgServerUrl + "/unsafe/800x0/scratch/",
      objData: {},
      input_datasets_img: [],
      input_datasets_denoising: [],
      middle_mask: [],
      output_datasets_crop_preview: [],
      output_datasets_crop_n: [],
      output_datasets_crop_p: [],
    };
  },
  methods: {
    getjobresult() {
      getjobresult({ id: this.$route.query.id }).then(res => {
        this.objData = res.data.data
        this.input_datasets_img = this.objData.input_datasets_img
      });
    },
    tabClick(tab, evt) {
      switch (tab.index) {
        case "0":
          this.input_datasets_img = this.objData.input_datasets_img
          break;
        case "1":
          this.input_datasets_denoising = this.objData.input_datasets_denoising
          break;
        case "2":
          this.middle_mask = this.objData.middle_mask          
          break;
        case "3":
          this.output_datasets_crop_preview = this.objData.output_datasets_crop_preview          
          break;
        case "4":
          this.output_datasets_crop_n = this.objData.output_datasets_crop_n          
          break;
        case "5":
          this.output_datasets_crop_p = this.objData.output_datasets_crop_p          
          break;
      }
    },
    finishedImages() {
      this.$emit('finished', this.percentage)
    }
  },
  mounted() {
    this.getjobresult();
    setTimeout(()=>{this.percentage=27},1000)
    setTimeout(()=>{this.percentage=64},3000)
    setTimeout(()=>{this.percentage=88},5000)
    setTimeout(()=>{this.percentage=100;this.finishedImages()},7000)
  }
};
</script>

<style lang="scss" scoped>
.images {
  padding: 0 30px;
  justify-content: space-between;
}
.output-info {
  margin-left: 30px;
}
.time-info {
  margin-left: 30px;
}
.progress-info {
  margin-top: 20px;
}
.info-box {
  justify-content: flex-start;
  align-items: flex-start;
  flex-wrap: wrap;
  margin-bottom: 10px;
  .info-list {
    justify-content: flex-start;
    flex-wrap: wrap;
  }
  .badge {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 10px;
  }
  i {
    color: #666;
    font-size: 14px;
  }
}
.header {
  margin-bottom: 30px;
}
.main {
  .img {
    border: 1px solid #ccc;
    margin-right: 2px;
    border-radius: 5px;
  }
}
</style>
