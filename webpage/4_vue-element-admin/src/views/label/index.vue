<template>
  <div class="label flex">
    <section class="main">
      <section class="tools flex">
        <div class="btn-box-right">
          <el-cascader
            v-model="currentLabel"
            class="cascader"
            size="mini"
            placeholder="请选择数据集"
            clearable
            :props="lazyProps"
            :options="batchList"
            :show-all-levels="false"
            @change="changeBatchList"
          >
            <template slot-scope="{ node, data }">
              <span>{{ data.label }}</span>
              <!-- <span v-if="!node.isLeaf">({{ data.children.length }})</span> -->
            </template>
          </el-cascader>
          <el-button-group>
            <el-button
              size="mini"
              type="info"
              :disabled="!currentLabel.length"
              icon="el-icon-arrow-left"
              @click="previousImg"
            >上一张</el-button>
            <el-button size="mini" type="info" :disabled="!currentLabel.length" @click="nextImg">
              下一张
              <i class="el-icon-arrow-right el-icon--right" />
            </el-button>
          </el-button-group>
        </div>
      </section>
      <section class="label-img">
        <div v-if="!currentLabel.length" style="text-align:center;margin-top:200px;">请选择数据集</div>
        <AIMarker
          v-else
          ref="aiPanel-editor"
          class="ai-observer"
          :style="{width: imgInfo.imgw < 1000 ? imgInfo.imgw + 'px' : 1000 + 'px',height: imgInfo.imgw < 1000 ? imgInfo.imgh + 'px' : (imgInfo.imgh*(1000/imgInfo.imgw)) + 'px'}"
          :read="readOnly"
          :img="fov_img"
          @vmarker:onDrawOne="onDrawOne"
          @vmarker:onSelect="onSelect"
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
          <el-table :data="labelLog" style="width: 100%">
            <el-table-column prop="name" label="用户" />
            <el-table-column prop="log" width="110" label="操作" />
            <el-table-column prop="date" label="日期" />
          </el-table>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { getBatchInfo, getMedicalIdInfo, getLabelByImageId, getImgbymid, updateLabel } from '@/api/cervical'
import { AIMarker } from '@/components/vue-picture-bd-marker/label.js'
import { cellsType } from '@/const/const'
import { ImgServerUrl } from '@/const/config'
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
      currentLabel: [],
      labelLog: [],
      imgInfo: {},
      fov_img: '',
      imgid: undefined,
      url: ImgServerUrl + '/unsafe/1000x0/',
      lazyProps: {
        lazy: true,
        lazyLoad(node, resolve) {
          const { label, level, parent } = node
          if (level === 1) {
            getMedicalIdInfo({ 'batchid': label }).then(res => {
              const medicalids = []
              res.data.data.medicalids.map(v => {
                const obj = {}
                obj['label'] = v
                obj['value'] = v
                medicalids.push(obj)
              })
              resolve(medicalids)
            })
          } else if (level === 2) {
            getImgbymid({ 'bid': parent['label'], 'mdcid': label, 'limit': 100, 'skip': 0 }).then(res => {
              res.data.data.imgs.map((v, i) => {
                v['label'] = v.imgpath
                v['value'] = `${i}-${v.id}-${v.imgpath}`
                v['leaf'] = level >= 2
              })
              resolve(res.data.data.imgs)
            })
          }
        }
      }
    }
  },
  created() {
    this.getBatchInfo()
  },
  methods: {
    previousImg() {
      this.getImgs(this.currentLabel[0], this.currentLabel[1], this.currentLabel[2].split('-')[0])
    },
    nextImg() {
      this.getImgs(this.currentLabel[0], this.currentLabel[1], this.currentLabel[2].split('-')[0], 1)
    },
    changeBatchList(val) {
      this.readOnly = true
      this.fov_img = this.url + this.currentLabel[2].split('-')[2]
      this.imgid = this.currentLabel[2].split('-')[1]
      this.getLabelByImageId(this.imgid, 10)
    },
    getImgs(bid, mdcid, img, next) {
      this.readOnly = true
      getImgbymid({ 'bid': bid, 'mdcid': mdcid, 'limit': 100, 'skip': 0 }).then(res => {
        const imgs = res.data.data.imgs
        /**
         * 索引查找并替换当前标注图片
         */
        if (next) {
          const idx = parseInt(img) + 1
          if (idx === imgs.length) return
          this.fov_img = this.url + imgs[idx].imgpath
          this.imgid = imgs[idx].id
          this.currentLabel = [bid, mdcid, idx + '-' + this.imgid + '-' + imgs[idx].imgpath]
          this.getLabelByImageId(this.imgid, 10)
        } else {
          const idx = parseInt(img) - 1
          if (idx < 0) return
          this.fov_img = this.url + imgs[idx].imgpath
          this.imgid = imgs[idx].id
          this.currentLabel = [bid, mdcid, idx + '-' + this.imgid + '-' + imgs[idx].imgpath]
          this.getLabelByImageId(this.imgid, 10)
        }
      })
    },
    getBatchInfo() {
      getBatchInfo().then(res => {
        res.data.data.batchs.map(v => {
          const obj = {}
          obj['label'] = v
          obj['value'] = v
          this.batchList.push(obj)
        })
      })
    },
    getLabelByImageId(id, status) {
      getLabelByImageId({ 'limit': 100, 'skip': 0, 'imgid': id, 'status': status }).then(res => {
        this.imgInfo = res.data.data
        this.imgInfo.labels.map(v => {
          v.tag = `${v.imgid}-${v.type}`
          v.tagName = v.type
          v.position = {
            x: parseFloat(v.x1 / this.imgInfo.imgw) * 100 + '%',
            x1: parseFloat(v.x2 / this.imgInfo.imgw) * 100 + '%',
            y: parseFloat(v.y1 / this.imgInfo.imgh) * 100 + '%',
            y1: parseFloat(v.y2 / this.imgInfo.imgh) * 100 + '%'
          }
          v.uuid = v.id
        })
        this.renderLabel()
        this.readOnly = false
      })
    },
    onDrawOne(data) {
      if (!this.readOnly) {
        this.$refs['aiPanel-editor'].getMarker().setTag({
          'tagName': this.cellType,
          'tag': `${this.imgid}-${this.cellType}`
        })
        /**
         * 新增标注
         */
        updateLabel({
          'labels': [
            {
              'imgid': parseInt(this.imgid),
              'op': 1, // 0未知 1增加 2删除 3修改
              'typeid': parseInt(this.cellType),
              'x1': parseInt((this.imgInfo.imgw * parseFloat(data.position.x)) / 100),
              'x2': parseInt((this.imgInfo.imgw * parseFloat(data.position.x1)) / 100),
              'y1': parseInt((this.imgInfo.imgh * parseFloat(data.position.y)) / 100),
              'y2': parseInt((this.imgInfo.imgh * parseFloat(data.position.y1)) / 100)
            }
          ]
        }).then(res => {
          this.$message({
            message: '保存成功',
            type: 'success'
          })
          this.readOnly = false
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
    onSelect(data) {
      /**
       * 修改标注
       */
      updateLabel({
        'labels': [
          {
            'imgid': parseInt(this.imgid),
            'labelid': parseInt(data.id),
            'op': 3, // 0未知 1增加 2删除 3修改
            'typeid': parseInt(this.cellType),
            'x1': parseInt((this.imgInfo.imgw * parseFloat(data.position.x)) / 100),
            'x2': parseInt((this.imgInfo.imgw * parseFloat(data.position.x1)) / 100),
            'y1': parseInt((this.imgInfo.imgh * parseFloat(data.position.y)) / 100),
            'y2': parseInt((this.imgInfo.imgh * parseFloat(data.position.y1)) / 100)
          }
        ]
      }).then(res => {
        this.$message({
          message: '修改成功',
          type: 'success'
        })
      })
    },
    renderLabel() {
      this.$refs['aiPanel-editor'].getMarker().clearData()
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
    margin-left: 10px;
    .tools {
      justify-content: space-between;
      margin: 5px 0;
      .cascader {
        width: 400px;
      }
    }
    .label-img {
      // height: calc(100vh - 90px);
      overflow: hidden;
    }
  }
  .info {
    width: 20%;
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
        max-height: calc(100vh - 550px);
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
