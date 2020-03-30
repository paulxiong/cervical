<template>
  <div class="leaflet flex" style="width:100%;height:100%;">
    <lmap
      v-if="mapargs.batchid"
      ref="map"
      :args="mapargs"
    />

    <div class="cells-box">
      <div class="img-div" style="max-height:600px;overflow-y: auto;">
        <el-image
          v-for="(img) in predictsList"
          :key="img.id"
          class="img"
          :src="hosturlpath32 + img.cellpath + '?width=64'"
          @click="imgclicked(img)"
        >
          <div slot="error" class="image-slot">
            <i class="el-icon-picture-outline" />
          </div>
        </el-image>
      </div>
      <el-pagination
        v-if="total"
        class="page"
        :current-page.sync="currentPage"
        :page-size="currentPageSize"
        layout="total, pager, jumper"
        :total="total"
        @current-change="handleCurrentChange"
        @size-change="handleSizeChange"
      />
    </div>
  </div>
</template>

<script>
import lmap from '@/components/leafletMap/leafletMap'
import { getScantxtByDID, getPredictsByPID2 } from '@/api/cervical'
import { APIUrl } from '@/const/config'

export default {
  components: { lmap },
  data() {
    return {
      did: 0,
      pid: 0,
      loading: false,
      mapargs: { },
      predictsList: [],
      total: 0,
      currentPage: 1,
      currentPageSize: 30,
      hosturlpath32: '' + APIUrl + '/imgs/'
    }
  },
  created() {
    this.$nextTick(() => {
      this.did = this.$route.query.did ? parseInt(this.$route.query.did) : undefined
      this.pid = this.$route.query.pid ? parseInt(this.$route.query.pid) : undefined
      this.getScantxtByDID(this.did, 1)
      this.getPredictsByPID2(this.currentPageSize, (this.currentPage - 1) * this.currentPageSize, this.pid)
    })
  },
  methods: {
    getScantxtByDID(did, type) {
      this.loading = true
      getScantxtByDID({ 'did': did, 'type': type }).then(res => {
        this.mapargs = res.data.data
        this.loading = false
      })
    },
    getPredictsByPID2(limit, skip, pid) {
      getPredictsByPID2({ 'limit': limit, 'skip': skip, 'pid': pid, 'status': 0, 'type': 51, 'order': 0 }).then(res => {
        this.predictsList = res.data.data.predicts
        this.total = res.data.data.total
      })
    },
    handleCurrentChange(val) {
      this.currentPage = val
    },
    handleSizeChange(val) {
      this.currentPageSize = val
    },
    imgclicked(img) {
      var arr = img.cellpath.split('IMG')
      arr = arr[1].split(this.mapargs.imgext)
      arr = arr[0].split('x')
      var x = parseInt(arr[1])
      var y = parseInt(arr[0])
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
    width: 500px;
    margin-left: 10px;
    overflow: hidden;
  }
  .img-div {
    .img {
      margin: 0 3px;
    }
  }
}
</style>
