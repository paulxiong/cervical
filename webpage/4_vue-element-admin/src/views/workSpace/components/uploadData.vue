<template>
  <div>
    <uploader
      ref="uploader"
      :options="options"
      class="uploader-example"
      :show-file-list="true"
      :file-list="dataList"
      @files-submitted="onfilesSubmitted"
      @file-complete="oncomplete"
      @files-added="onfilesAdded"
    >
      <uploader-unsupport />
      <uploader-drop v-show="!once">
        <p>拖动文件到此处或点击上传</p>
        <uploader-btn :attrs="attrs" :directory="true" :single="true">选择文件夹</uploader-btn>
      </uploader-drop>
      <uploader-list />
    </uploader>
  </div>
</template>

<script>
import { APIUrl } from '@/const/config'
import { getBidMid } from '@/api/cervical'
import { getToken } from '@/utils/auth'
import { dateformat4, dateformat5 } from '@/utils/dateformat'

export default {
  data() {
    return {
      options: {
        target: APIUrl + '/api1/uploaddir',
        query: this.getqueryfunc,
        simultaneousUploads: 1, // 只准有一个上传队列
        headers: {
          'Authorization': getToken()
        },
        testChunks: false,
        chunkSize: 4 * 1024 * 1024 // 分块时按照该值来分，文件大于这个值时候居然会把文件传坏！？
      },
      attrs: {
        accept: 'image/* text/*'
      },
      once: false,
      uploaderInstance: null,
      dirname: '',
      bid: '',
      mid: '',
      dataList: []
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.uploaderInstance = this.$refs.uploader
    })
  },
  methods: {
    getqueryfunc(val, val2) {
      return { 'mid': this.mid, 'bid': this.bid, 'dir': this.dirname }
    },
    onfilesAdded(files, fileList, event) {
      if (fileList[0].name) {
        this.dirname = fileList[0].name // 被上传的文件夹的名字
      }
      this.getBidMid()
    },
    // 上传文件开始之前触发，后面这里要检查文件是否完整，不完整就不要上传
    onfilesSubmitted(files, fileList, event) {
      if (this.$refs.uploader.fileList > 1) {
        this.once = true
        return
      }
      var hasScanTxt = false
      files.map(v => {
        if (v.name === 'Scan.txt' && v.size > 0 && v.fileType === 'text/plain' && v.isFolder === false) {
          hasScanTxt = true
          return
        }
      })
      // 没有Scan.txt，直接取消上传，说明病例不对
      if (hasScanTxt === false) {
        this.uploaderInstance.uploader.cancel()
        this.$message.error('所选的病例目录不完整 !')
      } else {
        this.$message({ type: 'success', message: '开始上传' })
        this.once = true
      }
    },
    oncomplete() {
      this.once = true
      this.$emit('checkUpload', true)
    },
    getBidMid() {
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
      })
    }
  }
}
</script>

<style>
  .uploader-example {
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
