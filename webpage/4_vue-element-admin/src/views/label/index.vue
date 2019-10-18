<template>
  <div class="label flex">
    <section class="main">
      321
    </section>
    <section class="info">
      <div class="cell-info">
        <el-badge is-dot class="badge-item">细胞详情</el-badge>
        <el-image class="cell-img" :src="cell_img" />
        <div class="cell">
          LSIL 鳞状上皮细胞低度病变
        </div>
      </div>
      <div class="data-info">
        <el-badge is-dot class="badge-item">数据集</el-badge>
        <div class="list">
          <div class="item">20190523.1807285.N.IMG002x010.JPG</div>
          <div class="item">20190523.1807285.N.IMG002x010.JPG</div>
          <div class="item">20190523.1807285.N.IMG002x010.JPG</div>
          <div class="item">20190523.1807285.N.IMG002x010.JPG</div>
          <div class="item">20190523.1807285.N.IMG002x010.JPG</div>
          <div class="item">20190523.1807285.N.IMG002x010.JPG</div>
          <div class="item">20190523.1807285.N.IMG002x010.JPG</div>
          <div class="item">20190523.1807285.N.IMG002x010.JPG</div>
          <div class="item">20190523.1807285.N.IMG002x010.JPG</div>
          <div class="item">20190523.1807285.N.IMG002x010.JPG</div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'Label',
  components: {},
  data() {
    return {
      fov_img: 'http://medical.raidcdn.cn:3001/unsafe/1000x0/scratch/93jeRNKB/origin_imgs/redhouse.1816953.N.IMG018x024.JPG',
      cell_img: 'http://medical.raidcdn.cn:3001/unsafe/100x0/scratch/93jeRNKB/cells/crop/17P0603.1904165A.N.IMG001x020.JPG_n_5_1111_1394_1211_1494.png'
    }
  }
}
</script>

<style lang="scss" scoped>
.label {
  height: 100%;
  justify-content: space-between;
  align-items: flex-start;
  .main {
    width: 80%;
    height: 100%;
  }
  .info {
    width: 20%;
    height: 100%;
    .cell-info {
      border: 2px solid #ccc;
      height: 50%;
      .cell-img {
        display: block;
        margin: 5px;
      }
      .cell {
        text-align: center;
        line-height: 50px;
        color: #fc4b4e;
        font-size: 20px;
      }
    }
    .data-info {
      border: 2px solid #ccc;
      height: 50%;
      .list {
        margin-top: 5px;
        overflow-x: auto;
        overflow-y: auto;
        .item {
          border-top: 1px solid #000;
          border-bottom: 1px solid #000;
          padding: 5px 0;
        }
      }
    }
  }
}
</style>
