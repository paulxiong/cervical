<template>
  <div class="leaflet flex" style="width:100%;height:100%;">
    <lmap
      v-if="mapargs.batchid"
      ref="map"
      :args="mapargs"
    />

    <div class="cells-box">
      <div class="slt-box flex">
        <img :src="resultimg" class="slt-img">
        <div class="text-box">
          <div>
            <el-button size="mini" type="primary">查看详情</el-button>
            <el-button icon="el-icon-arrow-left" size="mini" type="info" @click="goBack">返回上一页</el-button>
          </div>
          <img :src="preview" class="bpt-img">
          <el-table
            :data="checkTableData"
            border
            size="mini"
            :row-style="rowStyle"
          >
            <el-table-column
              label="进度"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.type }} {{ scope.row.total }}</span>
              </template>
            </el-table-column>
            <el-table-column
              label="未审核"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.total - scope.row.checked_num }}</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="checked_num"
              label="已审核"
            />
          </el-table>
        </div>
      </div>
      <div ref="tabsbox" class="tabsbox">
        <el-tabs type="border-card" :style="{'min-height': curHeight}" style="overflow-y:auto;">
          <el-tab-pane label="预测为阳性的细胞">
            <cellsList @imgclicked="imgclicked" />
          </el-tab-pane>
          <el-tab-pane label="预测为阴性的细胞" :disabled="true">
            <cellsList @imgclicked="imgclicked" />
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>
</template>

<script>
import lmap from '@/components/leafletMap/leafletMap'
import cellsList from '@/components/CellsList/index'
import { getScantxtByDID } from '@/api/cervical'
import { medicalURL } from '@/api/filesimages'

export default {
  components: { lmap, cellsList },
  data() {
    return {
      did: 0,
      pid: 0,
      curHeight: (window.innerHeight - 200) + 'px',
      cellsboxHeight: '200px',
      checkTableData: [
        {
          type: '阳性',
          total: 36,
          checked_num: 4
        },
        {
          type: '阴性',
          total: 24,
          checked_num: 23
        }
      ],
      loading: false,
      resultimg: '',
      preview: '',
      mapargs: {}
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
        return 'background:rgba(19, 206, 102, 0.8)'
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
    padding-top: 1px;
    padding-left: 2px;
  }

  .slt-img {
    width: 200px;
    height: 200px;
  }

  .bpt-img {
    width: 200px;
    margin-top: 1px;
    margin-bottom: -2px;
  }

  /deep/ th {
    padding: 4px 0;
  }
  /deep/ td {
    padding: 4px 0;
  }
}
</style>
