<template>
  <div style="width:100%; height:100%;">
    <lmap
      v-if="mapargs.batchid"
      ref="map"
      :args="mapargs"
      style="width: 50%"
    />

    <div class="img-div" style="overflow-y: auto;height:140px;width:1000px">
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
      :page-sizes="[10, 50, 100]"
      :page-size="currentPageSize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="total"
      @current-change="handleCurrentChange"
      @size-change="handleSizeChange"
    />
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
      currentPageSize: 50,
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
      y = (y - 1) * this.mapargs.imgheight + img.y1
      x = (x - 1) * this.mapargs.imgwidth + img.x1
      this.$refs.map.gotolatLng(x, y)
    }
  }
}
</script>

<style>
  .uploader-example {
    width: 880px;
    padding: 15px;
    margin: 40px auto 0;
    font-size: 12px;
    box-shadow: 0 0 10px rgba(0, 0, 0, .4);
  }
  .uploader-example .uploader-btn {
    margin-right: 4px;
  }
  .uploader-example .uploader-list {
    max-height: 440px;
    overflow: auto;
    overflow-x: hidden;
    overflow-y: auto;
  }
</style>
