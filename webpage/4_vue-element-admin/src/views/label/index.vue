<template>
  <div class="label flex">
    <section class="main">
      <section class="tools flex">
        <div class="btn-box-left">
          <el-button size="mini" type="primary">训练</el-button>
          <el-button size="mini" type="primary">预测</el-button>
        </div>
        <div class="btn-box-right">
          <el-cascader class="cascader" size="mini" placeholder="请选择数据集" clearable :options="batchList" @change="changeBatchList">
            <template slot-scope="{ node, data }">
              <span>{{ data.label }}</span>
              <span v-if="!node.isLeaf">({{ data.children.length }})</span>
            </template>
          </el-cascader>
          <el-button-group>
            <el-button size="mini" type="info" icon="el-icon-arrow-left">上一张</el-button>
            <el-button size="mini" type="info">
              下一张
              <i class="el-icon-arrow-right el-icon--right" />
            </el-button>
          </el-button-group>
        </div>
      </section>
      <section class="label-img">
        <AIMarker
          ref="aiPanel-editor"
          class="ai-observer"
          :read="readOnly"
          :img="fov_img"
          @vmarker:onDrawOne="onDrawOne"
        />
      </section>
    </section>
    <section class="info">
      <div class="cells-type">
        <el-divider content-position="left">
          <el-badge is-dot class="badge-item">请选择细胞标记类型</el-badge>
        </el-divider>
        <el-radio-group v-model="cellType" size="mini" class="list">
          <el-radio v-for="(cell, idx) in cellsType" :key="idx" :label="idx" class="item">{{ cell }}</el-radio>
        </el-radio-group>
      </div>
      <div class="data-info">
        <el-divider content-position="left">
          <el-badge is-dot class="badge-item">标注记录</el-badge>
        </el-divider>
        <div class="list">
          <el-table
            :data="labelLog"
            style="width: 100%"
          >
            <el-table-column
              prop="name"
              label="用户"
            />
            <el-table-column
              prop="log"
              width="110"
              label="操作"
            />
            <el-table-column
              prop="date"
              label="日期"
            />
          </el-table>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { getBatchInfo, getMedicalIdInfo } from '@/api/cervical'
import { getLabelByImageId } from '@/api/cervical'
import { AIMarker } from '@/components/vue-picture-bd-marker/label.js'
import { cellsType } from '@/const/const'
import { formatTime } from '@/utils/index'

export default {
  name: 'Label',
  components: { AIMarker },
  data() {
    return {
      cellsType: cellsType,
      readOnly: true,
      activeItem: 1,
      cellType: '1',
      batchList: [],
      currentData: [],
      labelLog: [],
      imgInfo: {},
      fov_img: 'http://medical.raidcdn.cn:3001/unsafe/1000x0/img/17P0603/1904165B/Images/IMG017x001.JPG'
    }
  },
  created() {
    this.getLabelByImageId()
    this.getBatchInfo()
  },
  methods: {
    changeBatchList(val) {
      this.currentData = val
    },
    getBatchInfo() {
      getBatchInfo().then(res1 => {
        const data1 = res1.data.data
        data1.batchs.map(v => {
          const obj = {}
          obj['label'] = v
          obj['value'] = v
          getMedicalIdInfo({ 'batchid': v }).then(res2 => {
            const data2 = res2.data.data
            const medicalids = []
            data2.medicalids.map(item => {
              item = {
                'label': item,
                'value': item,
                'children': [
                  {
                    'label': '20190523.1807285.N.IMG002x011.JPG',
                    'value': '20190523.1807285.N.IMG002x011.JPG'
                  },
                  {
                    'label': '20190523.1807285.N.IMG002x012.JPG',
                    'value': '20190523.1807285.N.IMG002x012.JPG'
                  },
                  {
                    'label': '20190523.1807285.N.IMG002x013.JPG',
                    'value': '20190523.1807285.N.IMG002x013.JPG'
                  }
                ]
              }
              medicalids.push(item)
            })
            obj['children'] = medicalids
            this.batchList.push(obj)
          })
        })
      })
    },
    getLabelByImageId() {
      getLabelByImageId({ 'limit': 100, 'skip': 0, 'imgid': 5 }).then(res => {
        this.imgInfo = res.data.data
        this.imgInfo.labels.map(v => {
          v.tag = `${v.imgid}-${v.type}`
          v.tagName = this.cellsType[v.type]
          v.position = {
            x: parseFloat(v.x / this.imgInfo.imgw) * 100 + '%',
            x1: parseFloat(v.x / this.imgInfo.imgw) * 100 + parseFloat(v.h / this.imgInfo.imgh) * 100 + '%',
            y: parseFloat(v.y / this.imgInfo.imgh) * 100 + '%',
            y1: parseFloat(v.y / this.imgInfo.imgh) * 100 + parseFloat(v.h / this.imgInfo.imgh) * 100 + '%'
          }
          v.uuid = v.id
        })
        this.renderLabel()
        this.readOnly = false
      })
    },
    onDrawOne(data, currentMovement) {
      if (!this.readOnly) {
        this.$refs['aiPanel-editor'].getMarker().setTag({
          tagName: this.cellsType[this.cellType],
          tag: `5-${this.cellType}`
        })
      }
      const dataList = this.$refs['aiPanel-editor'].getMarker().getData()
      const log = {
        name: JSON.parse(localStorage.getItem('USER_INFO')).name,
        log: `${dataList[dataList.length - 1].tag}(${parseFloat(dataList[dataList.length - 1].position.x).toFixed(1)},${parseFloat(dataList[dataList.length - 1].position.y).toFixed(1)})`,
        date: formatTime(dataList[dataList.length - 1].updated_time || new Date())
      }
      this.labelLog.unshift(log)
    },
    renderLabel() {
      this.$refs['aiPanel-editor'].getMarker().renderData(this.imgInfo.labels)
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
    .tools {
      justify-content: space-between;
      padding: 0 5px;
      margin: 5px 0;
      .cascader {
        width: 400px;
      }
    }
    .label-img {
      height: calc(100vh - 90px);
      overflow: hidden;
      .ai-observer {
        height: calc(100vh - 90px);
      }
    }
  }
  .info {
    width: 20%;
    height: 100%;
    .cells-type {
      border: 2px solid #ccc;
      height: 50%;
      overflow: auto;
      padding-left: 5px;
      padding-top: 5px;
      .list {
        display: block;
        .item {
          display: block;
          margin: 5px 0;
        }
      }
    }
    .data-info {
      border: 2px solid #ccc;
      padding-top: 5px;
      .list {
        margin-top: 5px;
        max-height: calc(100vh - 485px);
        overflow: auto;
        .item {
          border-top: 1px solid #000;
          border-bottom: 1px solid #000;
          font-size: 12px;
          padding: 5px;
          cursor: pointer;
        }
        .active-item {
          border-top: 1px solid #0088f9;
          border-bottom: 1px solid #0088f9;
          background: #0088f9;
          color: #fff;
        }
      }
    }
  }
}
</style>
