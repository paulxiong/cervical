<template>
  <div class="leaflet flex" style="width:100%;height:100%;">
    <lmap
      v-if="mapargs.batchid"
      ref="map"
      :args="mapargs"
      @dragend="dragend"
    />

    <div class="cells-box">
      <div class="slt-box flex">
        <mapx
          ref="thumbmapx"
          :url="resultimg"
          :col="mapargs.colcnt"
          :row="mapargs.rowcnt"
          @updatexy="thumbclicked"
        />
        <div class="text-box">
          <el-button icon="el-icon-arrow-left" size="medium" type="primary" class="text-box-btn" @click="goBack">返回上一页</el-button>
          <img :src="preview" class="bpt-img">
          <el-table
            :data="checkTableData"
            border
            size="mini"
          >
            <el-table-column
              label="总数"
              :min-width="tabwidth"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.total }}</span>
              </template>
            </el-table-column>
            <el-table-column
              label="未审核"
              :min-width="tabwidth"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.total - scope.row.checked_num }}</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="checked_num"
              label="已审核"
              :min-width="tabwidth"
            />
          </el-table>
        </div>
      </div>
      <div class="reviewbox">
        <cellsList @imgclicked="imgclicked" @updatereviewcnt="updatereviewcnt" />
      </div>
    </div>
  </div>
</template>

<script>
import lmap from '@/components/leafletMap/leafletMap'
import Mapx from '@/components/mapx/index'
import cellsList from '@/components/CellsList/projectcelllists'
import { getScantxtByDID } from '@/api/cervical'
import { medicalURL } from '@/api/filesimages'

export default {
  components: { lmap, cellsList, Mapx },
  data() {
    return {
      tabPosition: 'top',
      did: 0,
      pid: 0,
      curHeight: (window.innerHeight - 200) + 'px',
      cellsboxHeight: '200px',
      checkTableData: [
        {
          type: '待审核',
          total: 0,
          checked_num: 0
        }
      ],
      loading: false,
      resultimg: '',
      preview: '',
      mapargs: {},
      tabwidth: 70
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
    rowStyle({ row, rowIndex }) {
      if (row.total === row.checked_num) {
        return 'background:rgba(19, 206, 102, 0.2)'
      }
    },
    getScantxtByDID(did, type) {
      this.loading = true
      getScantxtByDID({ 'did': did, 'type': type }).then(res => {
        const data = res.data.data
        this.mapargs = data
        this.resultimg = medicalURL.resultImagePath(data.batchid, data.medicalid, data.result) + '?width=300'
        this.preview = medicalURL.previewImagePath(data.batchid, data.medicalid, data.preview) + '?width=240'
        this.loading = false
      })
    },
    thumbclicked(xy) {
      const x = parseInt(this.mapargs.realimgheight * this.mapargs.rowcnt * xy.xpercent)
      const y = parseInt(this.mapargs.realimgwidth * this.mapargs.colcnt * xy.ypercent)
      if (this.$refs.map) {
        this.$refs.map.gotolatLng(x, y, false)
      }
    },
    thumbmouseMoveToXY(xpercent, ypercent) {
      if (this.$refs.thumbmapx) {
        this.$refs.thumbmapx.mouseMoveToXY(xpercent, ypercent)
      }
    },
    imgclicked(img) {
      let arr = img.cellpath.split('IMG')
      arr = arr[1].split(this.mapargs.imgext)
      arr = arr[0].split('x')
      let x = parseInt(arr[1])
      let y = parseInt(arr[0])
      y = (y - 1) * this.mapargs.realimgheight + img.y1
      x = (x - 1) * this.mapargs.realimgwidth + img.x1
      this.thumbmouseMoveToXY(x / (this.mapargs.realimgwidth * this.mapargs.colcnt), y / (this.mapargs.realimgheight * this.mapargs.rowcnt))
      if (this.$refs.map) {
        this.$refs.map.gotolatLng(x, y, true)
      }
    },
    updatereviewcnt(reviewedcnt) {
      this.checkTableData = []
      this.checkTableData.push({
        type: '审核细胞',
        total: reviewedcnt.notreviewed + reviewedcnt.reviewed,
        checked_num: reviewedcnt.reviewed
      })
    },
    dragend(xy) {
      const y = (xy.y + 0.5) * this.mapargs.realimgheight // 传过来的y是从0开始所以不需要减一,0.5表示移动到中心
      const x = (xy.x + 0.5) * this.mapargs.realimgwidth
      this.thumbmouseMoveToXY(x / (this.mapargs.realimgwidth * this.mapargs.colcnt), y / (this.mapargs.realimgheight * this.mapargs.rowcnt))
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
    width: 225px;
    padding-top: 1px;
    padding-left: 2px;
    .text-box-btn {
      width:222px;
      height: 50px;
      margin: 2px 0px 2px 0px;
    }
  }

  .slt-img {
    width: 200px;
    height: 200px;
  }

  .bpt-img {
    width: 222px;
    margin: 1px 0px 0px 0px;
  }

  /deep/ th {
    padding: 4px 0;
  }
  /deep/ td {
    padding: 4px 0;
  }
  .reviewbox{
    margin: 2px 0px 0px 0px;
  }
}
</style>
