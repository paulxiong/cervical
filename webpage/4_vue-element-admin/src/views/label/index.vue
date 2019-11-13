<template>
  <div class="label flex">
    <section class="main">
      <section class="tools flex">
        <div class="btn-box-left" style="margin-right:20px;">
          <el-select
            v-model="labelType"
            placeholder="类型"
            clearable
            size="mini"
            class="filter-type"
            style="width: 100px"
            @change="changeLabeltype"
          >
            <el-option
              v-for="item in typeOptions"
              :key="item.key"
              :label="item.name"
              :value="item.key"
            />
          </el-select>
          <el-button type="primary" size="mini" icon="el-icon-refresh-left" @click="getAll">刷新</el-button>
          <el-button type="primary" size="mini" icon="el-icon-finished" @click="saveAll">保存</el-button>
        </div>
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
          @vmarker:onUpdated="onUpdate"
        />
      </section>
    </section>
    <section class="info">
      <div class="cells-type">
        <el-divider content-position="left">
          <el-badge is-dot class="badge-item">请先选择细胞标记类型</el-badge>
        </el-divider>
        <el-radio-group v-model="cellType" size="mini" class="list" @change="changeCelltype">
          <el-radio v-for="(cell, idx) in cellsType" :key="idx" :label="idx" class="item">{{ cell }}</el-radio>
        </el-radio-group>
      </div>
    </section>
  </div>
</template>

<script>
import { getBatchInfo, getMedicalIdInfo, getLabelByImageId, getImgbymid, updateLabel } from '@/api/cervical'
import { AIMarker } from '@/components/vue-picture-bd-marker/label.js'
import { cellsType } from '@/const/const'
import { APIUrl } from '@/const/config'
export default {
  name: 'Label',
  components: { AIMarker },
  data() {
    return {
      cellsType: cellsType,
      readOnly: true,
      activeItem: 1,
      cellType: undefined,
      batchList: [],
      currentLabel: [],
      imgInfo: {},
      selectLabel: {},
      labelType: 10,
      postData: [],
      typeOptions: [
        {
          key: 0,
          name: '未审核'
        },
        {
          key: 1,
          name: '已审核'
        },
        {
          key: 2,
          name: '移除'
        },
        {
          key: 10,
          name: '全部'
        }
      ],
      fov_img: '',
      url: APIUrl + '/imgs/',
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
      this.cellType = undefined
      this.readOnly = true
      this.fov_img = this.url + this.currentLabel[2].split('-')[2] + '?width=1000'
      this.imgid = this.currentLabel[2].split('-')[1]
      this.getLabelByImageId(this.imgid, this.labelType)
    },
    changeLabeltype() {
      this.getLabelByImageId(this.imgid, this.labelType)
    },
    changeCelltype() {
      this.readOnly = false
    },
    getAll() {
      this.getLabelByImageId(this.imgid, this.labelType)
    },
    saveAll() {
      const idArr = []
      this.postData.map(v => {
        idArr.push(v.id)
      })
      const addArr = []
      const delArr = []
      const changeArr = []
      console.log(this.postData)
      if (this.postData.length === 0 && this.imgInfo.labels.length > 0) {
        this.imgInfo.labels.map(v => {
          const obj = {
            'imgid': parseInt(this.imgid),
            'labelid': parseInt(v.id),
            'op': 2, // 0未知 1增加 2删除 3修改
            'typeid': parseInt(this.cellType),
            'x1': parseInt((this.imgInfo.imgw * parseFloat(v.position.x)) / 100),
            'x2': parseInt((this.imgInfo.imgw * parseFloat(v.position.x1)) / 100),
            'y1': parseInt((this.imgInfo.imgh * parseFloat(v.position.y)) / 100),
            'y2': parseInt((this.imgInfo.imgh * parseFloat(v.position.y1)) / 100)
          }
          delArr.push(obj)
        })
      } else {
        this.postData.map(v1 => {
          if (!v1.id) {
            const obj = {
              'imgid': parseInt(this.imgid),
              'op': 1, // 0未知 1增加 2删除 3修改
              'typeid': parseInt(this.cellType),
              'x1': parseInt((this.imgInfo.imgw * parseFloat(v1.position.x)) / 100),
              'x2': parseInt((this.imgInfo.imgw * parseFloat(v1.position.x1)) / 100),
              'y1': parseInt((this.imgInfo.imgh * parseFloat(v1.position.y)) / 100),
              'y2': parseInt((this.imgInfo.imgh * parseFloat(v1.position.y1)) / 100)
            }
            addArr.push(obj)
          }
          this.imgInfo.labels.map(v2 => {
            console.log(idArr.includes(v2.id))
            if (!idArr.includes(v2.id)) {
              const obj = {
                'imgid': parseInt(this.imgid),
                'labelid': parseInt(v2.id),
                'op': 2, // 0未知 1增加 2删除 3修改
                'typeid': parseInt(this.cellType),
                'x1': parseInt((this.imgInfo.imgw * parseFloat(v2.position.x)) / 100),
                'x2': parseInt((this.imgInfo.imgw * parseFloat(v2.position.x1)) / 100),
                'y1': parseInt((this.imgInfo.imgh * parseFloat(v2.position.y)) / 100),
                'y2': parseInt((this.imgInfo.imgh * parseFloat(v2.position.y1)) / 100)
              }
              delArr.push(obj)
            } else if (idArr.includes(v2.id) && (v2.tagName !== v1.tagName || v2.position.x !== v1.position.x || v2.position.x1 !== v1.position.x1 || v2.position.y !== v1.position.y || v2.position.y1 !== v1.position.y1)) {
              const obj = {
                'imgid': parseInt(this.imgid),
                'labelid': parseInt(v1.id),
                'op': 3, // 0未知 1增加 2删除 3修改
                'typeid': parseInt(this.cellType),
                'x1': parseInt((this.imgInfo.imgw * parseFloat(v1.position.x)) / 100),
                'x2': parseInt((this.imgInfo.imgw * parseFloat(v1.position.x1)) / 100),
                'y1': parseInt((this.imgInfo.imgh * parseFloat(v1.position.y)) / 100),
                'y2': parseInt((this.imgInfo.imgh * parseFloat(v1.position.y1)) / 100)
              }
              changeArr.push(obj)
            }
          })
        })
      }
      for (let i = 0; i < delArr.length; i++) {
        for (let j = i + 1; j < delArr.length; j++) {
          if (delArr[i]['labelid'] === delArr[j]['labelid']) {
            delArr.splice(j, 1)
            j = j - 1
          }
        }
      }
      if (addArr.length) {
        this.updateLabel(addArr)
      } else if (delArr.length) {
        this.updateLabel(delArr)
      } else if (changeArr.length) {
        this.updateLabel(changeArr)
      }
      this.$message({
        message: '保存成功',
        type: 'success'
      })
    },
    getImgs(bid, mdcid, img, next) {
      this.cellType = undefined
      this.readOnly = true
      getImgbymid({ 'bid': bid, 'mdcid': mdcid, 'limit': 100, 'skip': 0 }).then(res => {
        const imgs = res.data.data.imgs
        /**
         * 索引查找并替换当前标注图片
         */
        if (next) {
          const idx = parseInt(img) + 1
          if (idx === imgs.length) return
          this.fov_img = this.url + imgs[idx].imgpath + '?width=1000'
          this.imgid = imgs[idx].id
          this.currentLabel = [bid, mdcid, idx + '-' + this.imgid + '-' + imgs[idx].imgpath]
          this.getLabelByImageId(this.imgid, this.labelType)
        } else {
          const idx = parseInt(img) - 1
          if (idx < 0) return
          this.fov_img = this.url + imgs[idx].imgpath + '?width=1000'
          this.imgid = imgs[idx].id
          this.currentLabel = [bid, mdcid, idx + '-' + this.imgid + '-' + imgs[idx].imgpath]
          this.getLabelByImageId(this.imgid, this.labelType)
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
      getLabelByImageId({ 'limit': 999, 'skip': 0, 'imgid': id, 'status': status }).then(res => {
        this.imgInfo = res.data.data
        this.imgInfo.labels.map(v => {
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
      })
    },
    onDrawOne(data) {
      if (!this.readOnly) {
        this.$refs['aiPanel-editor'].getMarker().setTag({
          tagName: this.cellType,
          tag: `${this.imgid}-${this.cellType}`
        })
      }
    },
    onUpdate(data) {
      if ((this.readOnly) && (data.length === this.postData.length)) return
      this.postData = data
    },
    updateLabel(postData, msg) {
      updateLabel({
        'labels': postData
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
    .tools {
      justify-content: space-between;
      padding: 0 5px;
      margin: 5px 0;
      .cascader {
        width: 400px;
      }
    }
    .label-img {
      // height: calc(100vh - 90px);
      // overflow: hidden;
      .ai-observer {
        height: calc(100vh - 100px);
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
