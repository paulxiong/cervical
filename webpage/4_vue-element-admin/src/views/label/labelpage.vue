<template>
  <div class="leafletmap flex" style="width:100%;height:100%;">
    <lmap
      v-if="mapargs.batchid"
      ref="map"
      :args="mapargs"
      @dragend="dragend"
      @labeladd="labeladd"
      @labelupdate="labelupdate"
      @labeldelete="labeldelete"
      @labelinited="labelinited"
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
        <labelpannel
          ref="labelpannel"
          :scantxt="mapargs"
          @imgclicked="imgclicked"
          @updatereviewcnt="updatereviewcnt"
          @importpredict="importpredict"
          @labelclicked="labelclicked"
          @cancellabelclicked="cancellabelclicked"
          @gotolatlng="gotolatlng"
        />
      </div>
    </div>
  </div>
</template>

<script>
import lmap from '@/components/leafletMap/leafletMap'
import Mapx from '@/components/mapx/index'
import labelpannel from '@/components/CellsList/labelpannel'
import { getScantxtByDID, updateLabel2, getlabel2sbypid } from '@/api/cervical'
import { medicalURL } from '@/api/filesimages'
import { cellInFovPosation, celltypekeys } from '@/utils/label'

export default {
  components: { lmap, labelpannel, Mapx },
  data() {
    return {
      tabPosition: 'top',
      did: 0,
      pid: 0,
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
      tabwidth: 70,
      labels: {},
      celltypes: {}
    }
  },
  created() {
    this.did = this.$route.query.did ? parseInt(this.$route.query.did) : undefined
    this.pid = this.$route.query.pid ? parseInt(this.$route.query.pid) : undefined
    this.getScantxtByDID(this.did, 1)
    this.celltypes = celltypekeys()
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
        this.mapargs.labletool = true // 表示需要初始化标注工具
        this.mapargs.pid = this.pid
        this.mapargs.did = this.did
        this.resultimg = medicalURL.resultImagePath(data.batchid, data.medicalid, data.result) + '?width=300'
        this.preview = medicalURL.previewImagePath(data.batchid, data.medicalid, data.preview) + '?width=240'
        this.loading = false
      })
    },
    getlabel2sbypid(pid, status) {
      getlabel2sbypid({ 'limit': 1000, 'skip': 0, 'pid': pid, 'status': status }).then(res => {
        this.labelinfo = res.data.data
        var imported = false
        this.labelinfo.Label2s.map(v => {
          v.points = []
          v.points.push([-v.y1, v.x1]) // 在第4象限所以y是负数
          v.points.push([-v.y2, v.x2])
          v.predict_type = v.typeid
          v.fromdb = true
          // this.celltypes[v.typeid].
          if (this.$refs.map) {
            this.$refs.map.drawrectangle(v)
          }
          if (!imported && v.preid > 0) {
            imported = true
          }
        })
        if (imported) {
          this.$refs.labelpannel.importedfunc()
        }
      })
    },
    updateLabel2(labels) {
      updateLabel2({
        'label2s': labels
      })
    },
    labelinited() { // 标注初始化完成自动触发
      this.getlabel2sbypid(this.pid, 0)
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
    },
    importpredict(_cellsList) {
      _cellsList.map(v => {
        // predict信息添加在全图的points位置，方便画图
        const cellinfo = cellInFovPosation(v, this.mapargs.realimgheight, this.mapargs.realimgwidth, this.mapargs.imgext)
        cellinfo.fromdb = false // 从预测来，要在标注的库里面新建条目
        this.$refs.map.drawrectangle(cellinfo)
      })
    },
    labelclicked() {
      this.$refs.map.clickDrawRec()
    },
    cancellabelclicked() {
      this.$refs.map.clickDrawCancel()
    },
    gotolatlng(xy) {
      this.$refs.map.gotolatLng(xy.x, xy.y)
    },
    _savelabel(labelinfo) { // 同时把标注信息存到全局量, 用来作面板展示
      if (!this.labels[labelinfo.typeid]) {
        this.labels[labelinfo.typeid] = {}
      }
      // 树状结构存储，方便分类
      for (var level1 in this.labels) {
        for (var level2 in this.labels[level1]) {
          if (this.labels[level1][level2].labelid !== labelinfo.labelid) {
            continue
          }
          this.labels[level1][level2] = undefined
          delete this.labels[level1][level2]
          break
        }
      }
      var _label = Object.assign({}, labelinfo)
      _label.shortname = this.celltypes[_label.typeid].shortname
      _label.label = this.celltypes[_label.typeid].label
      this.labels[labelinfo.typeid][labelinfo.labelid] = _label
      this.$refs.labelpannel.updateLabelTable(this.labels)
    },
    _updatelabelinfo(labelinfo) {
      labelinfo.did = this.did
      labelinfo.pid = this.pid
      labelinfo.y1 = -labelinfo.y1
      labelinfo.y2 = -labelinfo.y2
      this._savelabel(labelinfo)
      return labelinfo
    },
    labeladd(labelinfo, alreadyindb) {
      labelinfo.op = 1 // 0未知 1增加 2删除 3修改
      labelinfo = this._updatelabelinfo(labelinfo)
      if (!alreadyindb) {
        this.updateLabel2([labelinfo])
      }
    },
    labelupdate(labelinfo) {
      labelinfo.op = 3
      labelinfo = this._updatelabelinfo(labelinfo)
      this.updateLabel2([labelinfo])
    },
    labeldelete(labelinfo) {
      labelinfo.op = 2
      labelinfo = this._updatelabelinfo(labelinfo)
      this.updateLabel2([labelinfo])
    }
  }
}
</script>

<style lang="scss" scoped>
.leafletmap {
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
