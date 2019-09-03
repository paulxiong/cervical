<template>
  <div class="images flex">
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
    }
  },
  created() {
    this.getjobresult();
  }
};
</script>

<style lang="scss" scoped>
.images {
  padding: 0 30px;
  justify-content: space-between;
}
.main {
  width: 100%;
  .img {
    border: 1px solid #ccc;
    margin-right: 2px;
    border-radius: 5px;
  }
}
</style>
