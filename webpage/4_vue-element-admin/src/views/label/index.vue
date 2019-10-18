<template>
  <div class="label flex">
    <section class="img-block flex">
      <div class="btn-box flex">
        <el-button type="primary">选择/导入数据</el-button>
        <el-button type="primary">选择标注细胞类型</el-button>
        <el-button type="info">去训练</el-button>
        <el-button type="info">去预测</el-button>
      </div>
      <el-checkbox-group v-model="checkedCells" class="cell-type">
        <el-checkbox v-for="cell in cells" :key="cell" :label="cell" />
      </el-checkbox-group>
      <img id="hallstatt" class="img-result" :src="imgResult">
    </section>
    <section class="info-block flex">
      <div class="label-info">
        <b class="title">标记信息</b>
        <el-image :src="img" />
      </div>
      <div class="data-list">
        <b class="title">数据集</b>
        <ul class="list">
          <li v-for="(item, idx) in dataList" :key="idx">{{ item }}</li>
        </ul>
      </div>
    </section>
  </div>
</template>

<script>
import { getLabelByImageId } from '@/api/cervical'
// import { setaddAnnotation } from '@/utils/setaddAnnotation'

export default {
  name: 'Label',
  components: {},
  data() {
    return {
      cells: ['1 Norm 正常细胞', '2 LSIL 鳞状上皮细胞低度病变', '3 HSIL 鳞状上皮细胞高度病变'],
      checkedCells: [],
      dataList: [
        '20190523.1807206.N.IMG001x019.JPG',
        '20190523.1807206.N.IMG001x019.JPG',
        '20190523.1807206.N.IMG001x019.JPG',
        '20190523.1807206.N.IMG001x019.JPG',
        '20190523.1807206.N.IMG001x019.JPG',
        '20190523.1807206.N.IMG001x019.JPG',
        '20190523.1807206.N.IMG001x019.JPG'
      ],
      ptg: 0,
      started: false,
      imgResult: 'http://dev.medical.raidcdn.cn:3001/unsafe/1000x0/scratch/DDzCz2KF/origin_imgs/20190523.1807206.P.IMG006x017.JPG',
      img: 'http://dev.medical.raidcdn.cn:3001/unsafe/400x0/scratch/DDzCz2KF/cells/crop/20190523.1807206.N.IMG004x011.JPG_n_5_1837_616_1936_716.png',
      imgInfo: {}
    }
  },
  mounted() {
    setTimeout(() => {
      this.getLabelByImageId()
    }, 1e3)
  },
  methods: {
    getLabelByImageId() {
      getLabelByImageId({ 'limit': 100, 'skip': 0, 'imgid': 5 }).then(res => {
        this.imgInfo = res.data.data
        this.setaddAnnotation(this.imgResult, this.imgInfo.labels, this.imgInfo.imgw ? this.imgInfo.imgw / 1000 : 3)
      })
    },
    setaddAnnotation(url, labels, divide) {
      window.anno.makeAnnotatable(document.getElementById('hallstatt'))
      // window.anno.setProperties({
      //   outline: 'yellow',
      //   outline_width: 2,
      //   hi_outline: 'yellow',
      //   hi_outline_width: 2,
      //   stroke: 'yellow'
      // })
      // 遍历获取snapshot表里图片头像框坐标信息并等比换算处理到页面上展示
      for (let i = 0; i < labels.length; i++) {
        const annotation = {
          src: url,
          text: labels[i].typeout,
          units: 'pixel',
          editable: true,
          shapes: [
            {
              type: 'rect',
              units: 'pixel',
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
        }
        // 添加头像框到画布里
        window.anno.addAnnotation(annotation)
      }
    }
  },
  mounted() {
    this.getLabelByImageId()
  }
}
</script>

<style lang="scss" scoped>
@import "../../styles/annotorious-dark.css";

.label {
  padding: 0 10px;
  justify-content: flex-start;
  align-items: flex-start;
  padding-top: 20px;
  .img-block {
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
    .btn-box {
      justify-content: space-between;
    }
  }
  .cell-type {
    margin: 10px 0;
  }
  .info-block {
    margin-left: 20px;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
    .label-info, .data-list {
      padding: 10px;
      border: 1px solid #ccc;
    }
    .data-list {
      width: 350px;
      margin-top: 10px;
      .list {
        list-style-type: none;
        margin: 0;
        padding: 0;
        height: 90%;
        max-height: 360px;
        overflow: auto;
        li {
          overflow: hidden;
          text-overflow: ellipsis;
          margin: 5px 0;
        }
      }
    }
  }
}
</style>
