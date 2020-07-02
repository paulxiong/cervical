<template>
  <div>
    <div class="wrapper">
      <div v-for="(img) in imgs" :key="img.id" class="box">
        <div v-if="img.url" style="height: 100%">
          <el-image style="height: 100%" fit="scale-down" :src="img.url" />
          <div style="position:absolute; z-index:2; left:10px; top:10px">{{ img.name }}</div>
        </div>
        <div v-else class="notload">
          <div class="notload-container">
            <span>请上传图片{{ img.id }}</span>
            <input type="file" class="upload" accept="image/png,image/jpeg,image/jpg" @change="addImg($event, img.id)">
          </div>
        </div>
      </div>
    </div>
    <el-button type="primary" @click="uploadm">上传这几个图片作为一个病例</el-button>
  </div>
</template>

<script>
import { uploadCustomMedical } from '@/api/cervical'

export default {
  data() {
    return {
      imgs: {
        0: { 'id': 0, 'savename': 'IMG001x001', 'ext': '', 'w': 0, 'h': 0, 'url': '', 'type': '', 'name': '', 'file': null },
        1: { 'id': 1, 'savename': 'IMG001x002', 'ext': '', 'w': 0, 'h': 0, 'url': '', 'type': '', 'name': '', 'file': null },
        2: { 'id': 2, 'savename': 'IMG002x001', 'ext': '', 'w': 0, 'h': 0, 'url': '', 'type': '', 'name': '', 'file': null },
        3: { 'id': 3, 'savename': 'IMG002x002', 'ext': '', 'w': 0, 'h': 0, 'url': '', 'type': '', 'name': '', 'file': null }
      }
    }
  },
  mounted() {
  },
  methods: {
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
    getBase64(file, cb) {
      const reader = new FileReader()
      reader.readAsDataURL(file) // 读出 base64
      reader.onloadend = () => {
        return cb && cb(reader.result)
      }
    },
    uploadm() {
      const err = this.checkBeforeUpload()
      if (err) {
        console.log(err)
        return
      }

      this.uploadCustomMedical()
    },
    checkBeforeUpload() {
      var err = ''
      const w = this.imgs[0].w
      const h = this.imgs[0].h
      const type = this.imgs[0].type
      for (var id in this.imgs) {
        const item = this.imgs[id]
        if (!item.url || !item.name || !item.file || item.w * item.h === 0 || !item.ext) {
          err = '图片文件未找到或格式不对'
          return err
        }
        if (w !== item.w || h !== item.h) {
          err = '图片尺寸不统一'
          return err
        }
        if (type !== item.type) {
          err = '图片格式不统一'
          return err
        }
      }
      return err
    },
    uploadCustomMedical() {
      for (var id in this.imgs) {
        const item = this.imgs[id]
        const param = new FormData() // 创建form对象
        param.append('file', item.file) // 通过append向form对象添加数据
        param.append('mid', 'mid111')
        param.append('bid', 'bid222')
        param.append('name', item.savename + item.ext)
        uploadCustomMedical(param).then(res => {
          console.log(res.data)
        })
      }
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
