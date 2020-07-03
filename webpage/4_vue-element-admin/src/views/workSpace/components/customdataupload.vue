<template>
  <div>
    <div class="wrapper">
      <div v-for="(img) in imgs" :key="img.id" class="box">
        <div v-if="img.url" style="height: 100%">
          <el-image style="height: 100%" fit="scale-down" :src="img.url" />
          <div style="position:absolute; z-index:2; left:10px; top:10px">
            <span>{{ img.name }}</span>
            <el-tag v-if="img.uploaded" type="success">{{ $t('workspace.dataCustomUploaded') }}</el-tag>
            <el-tag v-else type="danger">{{ $t('workspace.dataCustomNotUploaded') }}</el-tag>
          </div>
        </div>
        <div v-else class="notload">
          <div class="notload-container">
            <span>{{ $t('workspace.dataCustomFOVUploaded') }}{{ img.id }}</span>
            <input type="file" class="upload" accept="image/png,image/jpeg,image/jpg" @change="addImg($event, img.id)">
          </div>
        </div>
      </div>
    </div>
    <el-button type="primary" :disabled="alluploaded" @click="uploadm">{{ $t('workspace.dataCustomUpload') }}</el-button>
    <!-- <el-button type="primary" @click="resetImage">清空图片重新选择</el-button> -->
  </div>
</template>

<script>
import { getBidMid } from '@/api/cervical'
import { dateformat4, dateformat5 } from '@/utils/dateformat'
import { uploadCustomMedical, makeCustomMedicalScanTxt } from '@/api/cervical'

export default {
  name: 'CustomDataUpload',
  data() {
    return {
      imgs: {
        0: { 'id': 0, 'savename': 'IMG001x001', 'ext': '', 'w': 0, 'h': 0, 'url': '', 'type': '', 'name': '', 'file': null, 'uploaded': false },
        1: { 'id': 1, 'savename': 'IMG001x002', 'ext': '', 'w': 0, 'h': 0, 'url': '', 'type': '', 'name': '', 'file': null, 'uploaded': false },
        2: { 'id': 2, 'savename': 'IMG002x001', 'ext': '', 'w': 0, 'h': 0, 'url': '', 'type': '', 'name': '', 'file': null, 'uploaded': false },
        3: { 'id': 3, 'savename': 'IMG002x002', 'ext': '', 'w': 0, 'h': 0, 'url': '', 'type': '', 'name': '', 'file': null, 'uploaded': false }
      },
      mid: 'mid123',
      bid: 'bid1234',
      w: 0,
      h: 0,
      ext: '.jpg',
      alluploaded: false
    }
  },
  mounted() {
    this.getBidMid()
  },
  methods: {
    resetImage() {
      for (var id in this.imgs) {
        this.imgs[id] = Object.assign({}, { 'id': id, 'savename': 'IMG001x001', 'ext': '', 'w': 0, 'h': 0, 'url': '', 'type': '', 'name': '', 'file': null, 'uploaded': false })
      }
      this.imgs[0].savename = 'IMG001x001'
      this.imgs[1].savename = 'IMG001x002'
      this.imgs[2].savename = 'IMG002x001'
      this.imgs[3].savename = 'IMG002x002'
      this.getBidMid()
      this.alluploaded = false
    },
    addImg(event, id) {
      if (!event || !event.target || !event.target.files || event.target.files.length < 1) {
        return
      }
      this.imgs[id].url = this.getObjectURL(event.target.files[0])
      this.imgs[id].file = event.target.files[0]
      // 读取图片宽高
      this.imgInfo(this.imgs[id].url, (w, h) => {
        this.imgs[id].w = w
        this.imgs[id].h = h
        this.imgs[id].type = event.target.files[0].type
        this.imgs[id].name = event.target.files[0].name
        this.imgs[id].size = event.target.files[0].size
        if (this.imgs[id].type === 'image/png') {
          this.imgs[id].ext = '.png'
        } else if (this.imgs[id].type === 'image/jpeg' || this.imgs[id].type === 'image/jpg') {
          this.imgs[id].ext = '.jpg'
        }
      })
    },
    getObjectURL(file) {
      var url = null
      if (window.createObjectURL !== undefined) { // basic
        url = window.createObjectURL(file)
      } else if (window.URL !== undefined) { // mozilla(firefox)
        url = window.URL.createObjectURL(file)
      } else if (window.webkitURL !== undefined) { // webkit or chrome
        url = window.webkitURL.createObjectURL(file)
      }
      return url
    },
    imgInfo(fileURL, cb) {
      var img = new Image()
      img.src = fileURL
      img.onload = () => {
        return cb && cb(img.width, img.height)
      }
    },
    uploadm() {
      const err = this.checkBeforeUpload()
      if (err) {
        this.$message({ type: 'error', message: err, duration: 5000 })
        return
      }

      this.uploadCustomMedical()
      this.makeCustomMedicalScanTxt()
    },
    checkBeforeUpload() {
      var err = ''
      const w = this.imgs[0].w
      const h = this.imgs[0].h
      const type = this.imgs[0].type
      for (var id in this.imgs) {
        const item = this.imgs[id]
        if (!item.url || !item.name || !item.file || item.w * item.h === 0 || !item.ext) {
          err = this.$t('workspace.dataCustomNotFound')
          return err
        }
        if (w !== item.w || h !== item.h) {
          err = this.$t('workspace.dataCustomSizeNotUniform')
          return err
        }
        if (type !== item.type) {
          err = this.$t('workspace.dataCustomFormatUniform')
          return err
        }
      }
      this.w = w
      this.h = h
      this.ext = this.imgs[0].ext
      return err
    },
    asyncUploadCustomMedical(param, id) {
      return new Promise((resolve, reject) => {
        uploadCustomMedical(param).then(res => {
          this.imgs[id].uploaded = true
          resolve()
        })
      })
    },
    uploadCustomMedical() {
      for (var id in this.imgs) {
        const item = this.imgs[id]
        const param = new FormData() // 创建form对象
        param.append('file', item.file) // 通过append向form对象添加数据
        param.append('mid', this.mid)
        param.append('bid', this.bid)
        param.append('name', item.savename + item.ext)
        this.asyncUploadCustomMedical(param, id)
      }
    },
    makeCustomMedicalScanTxt() {
      makeCustomMedicalScanTxt({ 'bid': this.bid, 'mid': this.mid, 'w': this.w, 'h': this.h, 'ext': this.ext }).then(res => {
        this.$emit('checkUpload', true)
        this.alluploaded = true
      })
    },
    getBidMid(cb) { // 改成同步，因为被upload插件调用
      return new Promise((resolve, reject) => {
        getBidMid({ }).then(res => {
          if (res.data.data && res.data.data.batchid && res.data.data.medicalid) {
            this.bid = res.data.data.batchid
            this.mid = res.data.data.medicalid
          } else {
            this.bid = `b${dateformat4()}`
            this.mid = `m${dateformat5()}`
          }
          // 不提倡的做法
          var postData = { 'batchids': [this.bid], 'medicalids': [this.mid] }
          localStorage.setItem('POST_DATA', JSON.stringify(postData))
          resolve()
        })
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.wrapper {
  background: #fff1ce;
  width: 600px;
  display: grid;
  grid-gap: 0px 0px;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);
  grid-auto-flow: row;
}
.box {
  position: relative;
  width: 300px;
  background-color:#e8f4ff;
  border-radius: 0px;
}
.notload {
  width: 300px;
  height: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px 10px 10px 10px;
  .notload-container {
    width: 100%;
    height: 100%;
    background-color: #909399;
    border-radius: 5px;
  }
}
.el-image {
  display: inline;
}
</style>
