<template>
  <div class="page3-dashboard-container">
    <div id="left" class="page3-column">
      <img id="hallstatt" :src="imgurl" class="annotatable" />
    </div>

    <div id="right" class="page3-column">
      <el-table
        ref="singleTable"
        stripe
        border
        :data="tableData"
        highlight-current-row
        style="width: 100%"
        @current-change="handleCurrentChange"
      >
        <el-table-column property="id" label="序号" width="80" />
        <el-table-column property="batchid" label="批次" width="120" />
        <el-table-column property="medicalid" label="病历号" width="80" />
        <el-table-column property="imgpath" label="图片路径" />
      </el-table>
      <el-pagination
        class="pagination"
        background
        layout="total, prev, pager, next, jumper"
        :total="totalimg"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange2"
      />
    </div>

    <div id="bottom">
      <!-- <div v-for="item in items" :key="item" class="item imgWrap">
        <p>{{ item }}</p>
      </div>-->
      <div class="item imgWrap" v-for="(img,idx) in objImgs" :key="idx">
        <el-image
          class="imgg img1"
          :src="hosturlpath200 + img.cells_crop"
          lazy
          :data-cellsCropMasked="hosturlpath200 + img.cells_crop_masked"
          data-aaa="aaa"
        >
          <div slot="error" class="image-slot">
            <i class="el-icon-picture-outline"></i>
          </div>
        </el-image>
        <el-image
          class="imgg img2"
          :src="hosturlpath200 + img.cells_crop_masked"
          lazy
          :data-cellsCropMasked="hosturlpath200 + img.cells_crop_masked"
          data-aaa="aaa"
        >
          <div slot="error" class="image-slot">
            <i class="el-icon-picture-outline"></i>
          </div>
        </el-image>
      </div>
    </div>
  </div>
</template>

<script>
import {
  getImgListOneByOne,
  getLabelByImageId,
  getjobresult
} from "@/api/cervical";
import { ImgServerUrl } from "@/const/config";
import { page3ImgWidth } from "@/const/const";

export default {
  name: "Info",
  components: {},
  data() {
    return {
      items: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
      imgurl: "",
      imgw: 0, // 当前图片宽度
      imgh: 0, // 当前图片高度
      scale: 1, // 当前缩放比， 显示的图片宽度=原图宽度/scale
      totalimg: 0,
      tableData: [],
      totallabel: 0,
      labels: [],
      currentRow: null,
      hosturlpath16: ImgServerUrl + "/unsafe/32x0/scratch/",
      hosturlpath64: ImgServerUrl + "/unsafe/640x0/scratch/",
      hosturlpath200: ImgServerUrl + "/unsafe/200x0/scratch/",
      hosturlpath645: ImgServerUrl + "/unsafe/800x0/scratch/",
      objData: { name: "输入信息" },
      objData2: { name: "输出信息" },
      origin_imgs: [],
      cells_crop: [],
      cells_crop_masked: [],
      // objImgs: [{
      //   cells_crop: "",
      //   cells_crop_masked: ""
      // }],
      objImgs: []
    };
  },
  computed: {},
  created() {},
  mounted() {
    this.getImgListOneByOne(10, 0);
    this.getjobresult();
  },
  methods: {
    getjobresult() {
      getjobresult({ id: 71, done: "0" }).then(res => {
        this.objData = Object.assign(this.objData, res.data.data);
        this.origin_imgs = this.objData.origin_imgs;
        this.cells_crop = this.objData.cells_crop;
        this.cells_crop_masked = this.objData.cells_crop_masked;
        let objImgs = [];
        for (let index = 0; index < this.cells_crop.length; index++) {
          const element = this.cells_crop[index];
          // console.log(element)
          let objImg = {
            cells_crop: element
          };
          objImgs.push(objImg);
        }
        console.log("objImgs1", objImgs);
        for (let index = 0; index < this.cells_crop_masked.length; index++) {
          const element = this.cells_crop_masked[index];
          objImgs[index].cells_crop_masked = element;
        }
        console.log("objImgs2", objImgs);
        this.objImgs = objImgs;
        console.log(this.objData);
      });
    },
    setaddAnnotation(url, labels, divide) {
      window.anno.removeAll();
      window.anno.destroy();
      window.anno.setProperties({
        outline: "yellow",
        outline_width: 4,
        hi_outline: "green",
        hi_outline_width: 2,
        stroke: "blue"
      });
      window.anno.makeAnnotatable(document.getElementById("hallstatt"));
      // 遍历获取snapshot表里图片头像框坐标信息并等比换算处理到页面上展示
      // console.log('url: ', url);
      for (let i = 0; i < labels.length; i++) {
        var annotation = {
          src: url,
          text: "" + labels[i].typeout,
          units: "pixel",
          editable: true,
          shapes: [
            {
              type: "rect",
              units: "pixel",
              geometry: {
                x: parseInt(labels[i].x / divide),
                y: parseInt(labels[i].y / divide),
                width:
                  labels[i].w <= divide ? 1 : parseInt(labels[i].w / divide),
                height:
                  labels[i].h <= divide ? 1 : parseInt(labels[i].h / divide)
              }
            }
          ]
        };
        // 添加头像框到画布里
        window.anno.addAnnotation(annotation);
        // window.anno.highlightAnnotation(annotation)
      }
    },
    setCurrent(row) {
      this.$refs.singleTable.setCurrentRow(row);
    },
    handleCurrentChange(val) {
      this.imgurl =
        ImgServerUrl +
        "/unsafe/" +
        page3ImgWidth +
        "x0/img/" +
        val.batchid +
        "/" +
        val.medicalid +
        "/Images/" +
        val.imgpath;
      this.getLabelByImageId(100, 0, val.id);
    },
    handleSizeChange(val) {
      // console.log(`每页 ${val} 条`);
      // this.getImgListOneByOne(Number(val), 0);
    },
    handleCurrentChange2(val) {
      this.getImgListOneByOne(10, (Number(val) - 1) * 10);
    },
    getImgListOneByOne(limit, skip) {
      getImgListOneByOne({ limit: limit, skip: skip }).then(response => {
        if (
          !response ||
          !response.data ||
          !response.data.data ||
          typeof response.data.data !== "object"
        ) {
          return;
        }
        const { data } = response.data;
        this.totalimg = response.data.total;
        this.tableData = data.images ? data.images.concat([]) : [];

        if (this.setCurrent && this.setCurrent.length > 0) {
          this.setCurrent(this.tableData[0]);
        }
      });
    },
    getLabelByImageId(limit, skip, imgid) {
      getLabelByImageId({ limit: limit, skip: skip, imgid: imgid }).then(
        response => {
          if (
            !response ||
            !response.data ||
            !response.data.data ||
            typeof response.data.data !== "object"
          ) {
            return;
          }
          const { data } = response.data;
          this.totallabel = response.data.total;
          this.labels = data.labels ? data.labels.concat([]) : [];
          this.imgw = data.imgw;
          this.imgh = data.imgh;
          if (!this.imgw) {
            this.scale = 3;
          } else {
            this.scale = this.imgw / page3ImgWidth;
          }
          var that = this;
          setTimeout(function() {
            that.setaddAnnotation(that.imgurl, that.labels, that.scale);
          }, 200);
        }
      );
    }
  }
};
</script>

<style scoped lang="scss">
@import "../../styles/annotorious-dark.css";

.page3-dashboard-container {
  max-width: 100%;
  padding: 15px;
  // margin-left: 10px;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  // transform-style: preserve-3d;
}

.page3-column {
  min-width: 645px;
  // position: relative;
  // transition: transform 1s;
}

// #left, #right {
//   min-width: 40vw;
// }

// .page3-column:hover {
//   transform: rotate3d(0, 1, 0, 20deg);
// }

#hallstatt img {
  min-width: 645px;
  min-height: 405px;
}

.pagination {
  margin-top: 15px;
}

#bottom {
  display: flex;
  // flex-direction: column;
  flex-wrap: wrap;
  justify-content: flex-start;
  // align-items: flex-start;
  align-content: space-between;
  min-width: 100%;
  // height: 34vh;
  padding-top: 15px;
  // background-color: lightgray;
}

.imgWrap {
  position: relative;
  width: 150px;
  height: 150px;
  margin: 0px 10px 10px 0px;
  // background-color: lightsalmon;
}

// .imgWrap::before {
//   position: absolute;
//   content: url();
//   // content: url(attr(data-cells_crop_masked));
//   width: 100%;
//   height: 100%;
//   background-color: lightseagreen;
//   transition: visibility 1.5s, opacity 0.6s;
//   visibility: hidden;
//   opacity: 0.3;
// }

// .imgWrap:hover::before {
//   visibility: visible;
//   opacity: 0.9;
// }

.imgg {
  position: absolute;
}

.img1 {
  z-index: 1;
}

.img2 {
  z-index: 2;
  transition: opacity .6s;
  // transition-delay: 1.5s;
  // visibility: hidden;
  opacity: 0;
}

.img2:hover {
  // visibility: visible;
  opacity: 0.9;
  border: 1px solid #000;
  // transform: translateX(20px);
}

.img2::before {
  position: absolute;
	top: 0;
	left: -75%;
	z-index: 3;
	display: block;
	content: '';
	width: 50%;
	height: 100%;
  background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,.3) 100%);
  transform: skewX(-25deg);
}

.img2:hover::before {
  animation: shine 1.75s;
}

// .img2:hover +.imgg::before {
//   animation: shine 1.75s;
// }

@keyframes shine {
	100% {
		left: 125%;
	}
}
</style>

