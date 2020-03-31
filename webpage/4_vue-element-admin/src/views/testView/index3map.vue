<template>
  <div class="leaflet flex" style="width:100%;height:100%;">
    <lmap
      v-if="mapargs.batchid"
      ref="map"
      :args="mapargs"
    />

    <div class="cells-box">
      <div class="slt-box flex">
        <img src="../../assets/slt.jpg" class="slt-img">
        <div class="text-box">
          <el-button icon="el-icon-arrow-left" size="mini" type="info" @click="goBack">返回上一页</el-button>
          <div class="text-box-total">
            <h3>进度：</h3>
            <p><b>已审核:</b> 36</p>
            <p><b>未审核:</b> 2</p>
          </div>
          <el-button size="mini" type="primary">查看详情</el-button>
        </div>
      </div>
      <el-tabs type="border-card" :style="{'min-height': curHeight}" style="overflow-y:auto;">
        <el-tab-pane label="预测为阳性的细胞">
          <cellsList @imgclicked="imgclicked" />
        </el-tab-pane>
        <el-tab-pane label="预测为阴性的细胞">
          <cellsList @imgclicked="imgclicked" />
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
import lmap from '@/components/leafletMap/leafletMap'
import cellsList from '@/components/CellsList/index'
import { getScantxtByDID } from '@/api/cervical'

export default {
  components: { lmap, cellsList },
  data() {
    return {
      did: 0,
      pid: 0,
      curHeight: (window.innerHeight - 200) + 'px',
      loading: false,
      mapargs: { }
    }
  },
  created() {
    this.$nextTick(() => {
      this.did = this.$route.query.did ? parseInt(this.$route.query.did) : undefined
      this.pid = this.$route.query.pid ? parseInt(this.$route.query.pid) : undefined
      this.getScantxtByDID(this.did, 1)
    })
  },
  methods: {
    goBack() {
      this.$router.back(-1)
    },
    getScantxtByDID(did, type) {
      this.loading = true
      getScantxtByDID({ 'did': did, 'type': type }).then(res => {
        this.mapargs = res.data.data
        this.loading = false
      })
    },
    imgclicked(img) {
      let arr = img.cellpath.split('IMG')
      arr = arr[1].split(this.mapargs.imgext)
      arr = arr[0].split('x')
      let x = parseInt(arr[1])
      let y = parseInt(arr[0])
      y = (y - 1) * this.mapargs.realimgheight + img.y1
      x = (x - 1) * this.mapargs.realimgwidth + img.x1
      this.$refs.map.gotolatLng(x, y)
    }
  }
}
</script>

<style lang="scss" scoped>
.leaflet {
  justify-content: space-between;
  .cells-box {
    width: 425px;
    height: 100%;
    margin: 0 5px;
    overflow: hidden;
  }

  .slt-box {
    height: 200px;
    justify-content: flex-start;
  }

  .text-box {
    height: 100%;
    padding-top: 10px;
    padding-left: 30px;
  }

  .slt-img {
    width: 200px;
    width: 200px;
  }
}
</style>
