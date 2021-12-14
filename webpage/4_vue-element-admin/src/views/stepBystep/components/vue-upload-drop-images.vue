<script>
//this file replaced customDataUpload.vue <- newCustomDatasets.vue  <-
import { getBidMid } from '@/api/cervical'
import { dateformat4, dateformat5 } from '@/utils/dateformat'
import { uploadCustomMedical, makeCustomMedicalScanTxt } from '@/api/cervical'

export default {
  name: "UploadImages", // vue component name
  data() {
    return {
      error: "",
      files: [],
      dropped: 0,
      Imgs: [],
      /* this is cervial ai definition  imgs: {
        0: { 'id': 0, 'savename': 'IMG001x001', 'ext': '', 'w': 0, 'h': 0, 'url': '', 'type': '', 'name': '', 'file': null, 'uploaded': false },
        1: { 'id': 1, 'savename': 'IMG001x002', 'ext': '', 'w': 0, 'h': 0, 'url': '', 'type': '', 'name': '', 'file': null, 'uploaded': false },
        2: { 'id': 2, 'savename': 'IMG002x001', 'ext': '', 'w': 0, 'h': 0, 'url': '', 'type': '', 'name': '', 'file': null, 'uploaded': false },
        3: { 'id': 3, 'savename': 'IMG002x002', 'ext': '', 'w': 0, 'h': 0, 'url': '', 'type': '', 'name': '', 'file': null, 'uploaded': false }
      },*/      
      imgs:[],
      mid: 'mid123',
      bid: 'bid1234'
    };
  },
  props: {
    max: Number,
    uploadMsg: String,
    maxError: String,
    fileError: String,
    clearAll: String,
  },
  mounted() {
  this.getBidMid()
  this.canvas = this.$refs.thumbnail
  this.ctx = this.canvas.getContext('2d')
  },
  //boostx:
  //created() {
  //  this.$root.$refs.A = this;
  //},
  methods: {
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
          console.log("boostx in vue-upload-drop-images.vue, this.mid=", this.mid)
          var postData = { 'batchids': [this.bid], 'medicalids': [this.mid] }
          localStorage.setItem('POST_DATA', JSON.stringify(postData))
          resolve()
        })
      })
    },    
    convertBase64UrlToBlob(urlData, type) { /* 将base64转换成可用formdata提交的文件,urlData base64的url,type 0图片 1视频 */
      var bytes = window.atob(urlData.split(',')[1]) // 去掉url的头，并转换为byte
      // 处理异常,将ascii码小于0的转换为大于0
      var ab = new ArrayBuffer(bytes.length)
      var ia = new Uint8Array(ab)
      for (var i = 0; i < bytes.length; i++) {
        ia[i] = bytes.charCodeAt(i)
      }
      return new Blob([ab], { type: type === 0 ? 'image/png' : 'image/mp4' })
    },
    thumbnail() {
      const width = 200
      this.canvas.width = width
      this.canvas.height = width
      var xy = {
        0: { x1: 0, y1: 0, w: this.canvas.width / 2, h: this.canvas.height / 2 },
        1: { x1: this.canvas.width / 2, y1: 0, w: this.canvas.width / 2, h: this.canvas.height / 2 },
        2: { x1: 0, y1: this.canvas.height / 2, w: this.canvas.width / 2, h: this.canvas.height / 2 },
        3: { x1: this.canvas.width / 2, y1: this.canvas.height / 2, w: this.canvas.width / 2, h: this.canvas.height / 2 }
      }
      for (var id in this.imgs) {
        const item = this.imgs[id]
        if (!item.img) {
          continue
        }
        this.ctx.drawImage(item.img, xy[id].x1, xy[id].y1, xy[id].w, xy[id].h)
      }
    },
    addImg(event, id) {
      if (!event || !event.target || !event.target.files || event.target.files.length < 1) {
        return
      }
      this.imgs[id].url = this.getObjectURL(event.target.files[0])
      this.imgs[id].file = event.target.files[0]
      // 读取图片宽高
      this.imgInfo(id, this.imgs[id].url, (img, w, h) => {
        this.imgs[id].w = w
        this.imgs[id].h = h
        this.imgs[id].img = img
        this.imgs[id].type = event.target.files[0].type
        this.imgs[id].name = event.target.files[0].name
        this.imgs[id].size = event.target.files[0].size
        if (this.imgs[id].type === 'image/png') {
          this.imgs[id].ext = '.png'
        } else if (this.imgs[id].type === 'image/jpeg' || this.imgs[id].type === 'image/jpg') {
          this.imgs[id].ext = '.jpg'
        }

        this.thumbnail(id, img)
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
    /* uploadmx() {console.log("boostx: uploadmx")},
     */
    uploadm() {
      console.log("boostx: enter uploadm.")
      const err = this.checkBeforeUpload()
      if (err) {
        this.$message({ type: 'error', message: err, duration: 5000 })
        return
      }
      // var _mself = this

      this.uploadCustomMedical()
      //boostx
      console.log("makeCustomeMedicalScanTxt is called.")
      this.makeCustomMedicalScanTxt()
      this.uploadThumbnail()
      this.uploadPreview()
     },
    checkBeforeUpload() {
      //boostx debug
      return ''
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
    uploadCustomMedical() {
      for (var  id in this.imgs){
        const item = this.imgs[id]
        console.log("boostx uploadCustomMedical", item)


        const param = new FormData() // 创建form对象
        // param.append('file', item.file) // 通过append向form对象添加数据
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
    uploadThumbnail() {
      const param = new FormData() // 创建form对象
      const base64 = this.canvas.toDataURL('image/jpg')
      const file = this.convertBase64UrlToBlob(base64, 0)

      param.append('file', file) // 通过append向form对象添加数据
      param.append('mid', this.mid)
      param.append('bid', this.bid)
      param.append('name', 'Result-c.jpg')
      this.asyncUploadCustomMedical(param, 100) // <4 的时候表示传的是FOV, 100认为是缩略图
    },
    uploadPreview() {
      var ctx = this.$refs.preview.getContext('2d')
      this.$refs.preview.width = 240
      this.$refs.preview.height = 81

      var img = new Image()
      img.onload = () => {
        ctx.drawImage(img, 0, 0)

        const param = new FormData() // 创建form对象
        const base64 = this.$refs.preview.toDataURL('image/jpg')
        const file = this.convertBase64UrlToBlob(base64, 0)

        param.append('file', file) // 通过append向form对象添加数据
        param.append('mid', this.mid)
        param.append('bid', this.bid)
        param.append('name', 'Preview-c.jpg')
        this.asyncUploadCustomMedical(param, 100) // <4 的时候表示传的是FOV, 100认为是缩略图
      }
      img.src = '/img/Preview-c.jpg'
    },
    asyncUploadCustomMedical(param, id) {
      return new Promise((resolve, reject) => {
        uploadCustomMedical(param).then(res => {
          console.log("boostx:asyncUploadCustomMedical " + id)
          if (id < 4) {
            console.log("boostx:this.files=" + this.imgs[id].file.name)
            this.imgs[id].uploaded = true
            console.log("boostx: uploadCustomMedical")
          }
          resolve()
        })
      })
    },
    dragOver() {
      this.dropped = 2;
    },
    dragLeave() {},
    drop(e) {
      let status = true;
      let files = Array.from(e.dataTransfer.files)
      if (e && files) {
        files.forEach((file) => {
          if (file.type.startsWith("image") === false) status = false;
        });
        if (status == true) {
          if (
            this.$props.max &&
            files.length + this.files.length > this.$props.max
          ) {
            this.error = this.$props.maxError
              ? this.$props.maxError
              : `Maximum files is` + this.$props.max;
          } else {
            this.files.push(...files);
            this.previewImgs();
          }
        } else {
          this.error = this.$props.fileError
            ? this.$props.fileError
            : `Unsupported file type`;
        }
      }
      this.dropped = 0;
    },
    append() {
      this.$refs.uploadInput.click();
    },
    readAsDataURL(file) {
      return new Promise(function (resolve, reject) {
        let fr = new FileReader();
        fr.onload = function () {
          resolve(fr.result);
        };
        fr.onerror = function () {
          reject(fr);
        };
        fr.readAsDataURL(file);
      });
    },
    deleteImg(index) {
      this.Imgs.splice(index, 1);
      this.files.splice(index, 1);
      this.$emit("changed", this.files);
      this.$refs.uploadInput.value = null;
      //boostx
      if (!this.Imgs.length){
        this.$emit('checkUpload', false)
      }
      else{
        this.imgs.splice(index,1)
      }
      console.log("boostx in deleteImg:", this.imgs)
    },
    previewImgs(event) {
      if (
        this.$props.max &&
        event &&
        event.currentTarget.files.length + this.files.length > this.$props.max
      ) {
        this.error = this.$props.maxError
          ? this.$props.maxError
          : `Maximum files is` + this.$props.max;
        return;
      }
      //? don't know why the object event.currentTarget.file cannot be printed correctly? 
      console.log("boostx previewImgs ", event.currentTarget.files);
      // if (this.dropped == 0) this.files.push(...event.currentTarget.files); //* merge two arrays
      if (this.dropped == 0) this.files.push(...event.target.files); //* merge two arrays
      this.error = "";
      this.$emit("changed", this.files);
      let readers = [];
      if (!this.files.length) {
         this.$emit('checkUpload', false)  //* disable Next in file datasets-data.vue
         return;
      }
      this.$emit('checkUpload', true)   //*enabled Next in file dataset-data.vue
      
      for (let i = 0; i < this.files.length; i++) {
        let imgx = { 'id': 0, 'savename': 'IMG001x00', 'ext': '.jpg', 'w': 0, 'h': 0, 'url': '', 'type': '', 'name': '', 'file': null, 'uploaded': false }
        readers.push(this.readAsDataURL(this.files[i])); //!this. here is refer to event itself, not class 
        imgx.url =this.getObjectURL(this.files[i]);
        imgx.file=this.files[i];
        imgx.savename = imgx.savename + i.toString()
        this.imgs.push(imgx);
      }
        console.log("boostx imgs=", this.imgs);
      

      Promise.all(readers).then((values) => {
        //boostx: this.imgs = values;
          // console.log("boostx debug reached here 3 readers=" + JSON.stringify(values));
          this.Imgs= values;
      });
    },
    reset() {
      this.$refs.uploadInput.value = null;
      this.Imgs = [];
      this.files = [];
      this.imgs = [];
      this.$emit("changed", this.files);
      this.$emit('checkUpload', false)
    },
  },
};
</script>

<template>
  <div
    class="container"
    @dragover.prevent="dragOver"
    @dragleave.prevent="dragLeave"
    @drop.prevent="drop($event)"
  >
    <div class="drop" v-show="dropped == 2"></div>
    <!-- Error Message -->
    <div v-show="error" class="error">
      {{ error }}
    </div>

    <!-- To inform user how to upload image -->
    <div v-show="Imgs.length == 0" class="beforeUpload"> 
      <input
        type="file"
        style="z-index: 1"
        accept="image/*"
        ref="uploadInput"
        accept="image/png,image/jpeg,image/jpg"
        @change="previewImgs"
        multiple
      />
      <svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
        <title>Upload Image</title>
        <g id="Upload_Image" data-name="Upload Image">
          <g id="_Group_" data-name="&lt;Group&gt;">
            <g id="_Group_2" data-name="&lt;Group&gt;">
              <g id="_Group_3" data-name="&lt;Group&gt;">
                
                <!-- boostx -->
                <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
                  viewBox="0 0 512.024 512.024" style="enable-background:new 0 0 512.024 512.024;" xml:space="preserve">
                <polygon style="fill:#0D91BA;" points="176.896,67.3 150.88,36.084 52.032,36.084 20.808,67.3 20.808,108.924 437.04,108.924 
                  437.04,67.3 "/>
                <rect y="108.924" style="fill:#25B6D2;" width="457.84" height="299.2"/>
                <rect x="46.824" y="88.092" style="fill:#FFFFFF;" width="364.2" height="20.808"/>
                <circle style="fill:#E04F5F;" cx="426.32" cy="390.236" r="85.704"/>
                <g>
                  <rect x="381.672" y="386.252" style="fill:#FFFFFF;" width="89.248" height="8"/>
                  <rect x="422.296" y="345.612" style="fill:#FFFFFF;" width="8" height="89.248"/>
                </g>
                </svg>
            </g>
          </g>
        </g>
      </svg>

      <p class="mainMessage">
        {{ uploadMsg ? uploadMsg : "Click to upload or drop your images here" }}
      </p>
   </div>
  <!-- boostx 
  <el-button type="primary" :disabled="alluploaded" @click="uploadm">{{ $t('workspace.dataCustomUpload') }}</el-button>
  -->
    <div class="imgsPreview" v-show="Imgs.length > 0">
      <p>
        <button type="button" class="clearButton" @click="reset">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
  <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
  <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
</svg>
          {{ clearAll ? clearAll : "clear All" }}
        </button>
      </p>
      <p align="left">
        <canvas ref="thumbnail" width="200px" height="200px" style="border:1px solid #000000; display: none;" />
        <canvas ref="preview" width="200px" height="200px" style="border:1px solid #000000; display: none;" />

        <!-- boostx 
        <button type="button" class="uploadallButton" @click="uploadm">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-upload" viewBox="0 0 16 16">
  <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"></path>
  <path d="M7.646 1.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 2.707V11.5a.5.5 0 0 1-1 0V2.707L5.354 4.854a.5.5 0 1 1-.708-.708l3-3z"></path>
</svg>
                upload All
        </button>
        -->
      </p>
      
      <div class="imageHolder" v-for="(img,i) in Imgs" :key="i">
        <img :src="img" />
        <span class="delete" style="color: white" @click="deleteImg(--i)">
          <svg
            class="icon"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
            />
          </svg>
        </span>
        <div class="plus" @click="append" v-if="++i == Imgs.length">+</div>

      </div>
    </div>
  </div>
</template>



<style scoped>
.container {
  width: 100%;
  height: 100%;
  background: #f7fafc;
  border: 0.5px solid #a3a8b1;
  border-radius: 10px;
  padding: 30px;
  position: relative;
}
.drop {
  width: 100%;
  height: 100%;
  top: 0;
  border-radius: 10px;
  position: absolute;
  background-color: #f4f6ff;
  left: 0;
  border: 3px dashed #a3a8b1;
}
.error {
  text-align: center;
  color: red;
  font-size: 15px;
}
.beforeUpload {
  position: relative;
  text-align: center;
}
.beforeUpload input {
  width: 100%;
  margin: auto;
  height: 100%;
  opacity: 0;
  position: absolute;
  background: red;
  display: block;
}
.beforeUpload input:hover {
  cursor: pointer;
}
.beforeUpload .icon {
  width: 150px;
  margin: auto;
  display: block;
}
.imgsPreview .imageHolder {
  width: 150px;
  height: 150px;
  background: #fff;
  position: relative;
  border-radius: 10px;
  margin: 5px 5px;
  display: inline-block;
}
.imgsPreview .imageHolder img {
  object-fit: cover;
  width: 100%;
  height: 100%;
}
.imgsPreview .imageHolder .delete {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 29px;
  height: 29px;
  color: #fff;
  background: red;
  border-radius: 50%;
}
.imgsPreview .imageHolder .delete:hover {
  cursor: pointer;
}
.imgsPreview .imageHolder .delete .icon {
  width: 66%;
  height: 66%;
  display: block;
  margin: 4px auto;
}
.imgsPreview .imageHolder .plus {
  color: #2d3748;
  background: #f7fafc;
  border-radius: 50%;
  font-size: 21pt;
  height: 30px;
  width: 30px;
  text-align: center;
  border: 1px dashed;
  line-height: 23px;
  position: absolute;
  right: -42px;
  bottom: 43%;
}
.plus:hover {
  cursor: pointer;
}
.clearButton {
  color: #2d3748;
  position: absolute;
  top: 7px;
  right: 7px;
  background: none;
  border: none;
  cursor: pointer;
}
.uploadallButton {
  color: #2d3748;
  position: absolute;
  top: 7px;
  left: 7px;
  background: none;
  border: none;
  cursor: pointer;
}
</style>