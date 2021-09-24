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
        <p>{{ $t('workspace.projectDataUploadTip') }}</p>
        <uploader-btn :attrs="attrs" :directory="true" :single="true">{{ $t('workspace.projectDataBrowse') }}</uploader-btn>
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
import { scanTxtParse, checkFileList } from '@/utils/scan_txt'

export default {
  data() {
    return {
      options: {
        target: APIUrl + '/api1/uploaddir',
        query: this.getqueryfunc,
        parseTimeRemaining: this.parseTimeRemaining,
        simultaneousUploads: 1, // 只准有一个上传队列
        headers: {
          'Authorization': getToken()
        },
        testChunks: false,
        chunkSize: 4 * 1024 * 1024, // 分块时按照该值来分，文件大于这个值时候居然会把文件传坏！？
        preprocess: this.preprocess
      },
      attrs: {
        accept: 'image/* text/*'
      },
      once: false, // 上传过之后隐藏上传的按钮
      uploaderInstance: null,
      dirname: '',
      bid: '',
      mid: '',
      dataList: [],
      filelist: [], // 检查所有文件是否齐全，保存插件检测到要上传的文件
      lostfiles: [] // 缺失的文件的列表
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.uploaderInstance = this.$refs.uploader
      this.getBidMid()
    })
  },
  methods: {
    getqueryfunc(val, val2) {
      if (!this.mid || !this.bid) {
        this.getBidMid()
      }
      return { 'mid': this.mid, 'bid': this.bid, 'dir': this.dirname }
    },
    parseTimeRemaining(timeRemaining, parsedTimeRemaining) { // 显示时间不对，不显示，直接返回空字符串
      return ''
    },
    onfilesAdded(files, fileList, event) { // 把文件列表做个排序，确保Scan.txt文件第一个处理
      files = files.sort(function(a, b) {
        return (a.name === 'Scan.txt' && a.size > 0 && a.fileType === 'text/plain' && a.isFolder === false) ? -1 : 1
      })
      this.filelist = files
      this.lostfiles = []
      if (fileList[0].name) {
        this.dirname = fileList[0].name // 被上传的文件夹的名字
      }
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
        this.$message.error(this.$t('workspace.projectDataIncomplete'))
      } else {
        this.$message({ type: 'success', message: this.$t('workspace.projectDataStartUpload') })
        this.once = true
      }
    },
    oncomplete() {
      if (this.lostfiles && this.lostfiles.length > 0) {
        this.once = false
      } else {
        this.once = true
        this.$emit('checkUpload', true)
      }
    },
    cancelUploder(msg) {
      this.uploaderInstance.uploader.cancel()
      this.$message({ type: 'error', message: msg, duration: 10000 })
      this.once = false
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
    },
    getFilelist(zenFile, chunkSize) {
      return new Promise((resolve, reject) => {
        const file = zenFile.file
        const fileReader = new FileReader()
        const blobSlice = File.prototype.slice || File.prototype.mozSlice || File.prototype.webkitSlice
        fileReader.onerror = e => reject(e)
        fileReader.onload = e => {
          var ret = scanTxtParse(e.target.result)
          if (ret && ret.filelist) {
            resolve(ret.filelist)
          } else {
            resolve()
          }
        }
        const load = () => {
          var start = 0
          var end = start + chunkSize >= file.size ? file.size : start + chunkSize
          fileReader.readAsText(blobSlice.call(file, start, end))
        }
        load()
      })
    },
    preprocess(chunk) { // 上传之前处理
      const that = this
      if (chunk.file.name === 'Scan.txt') {
        this.getFilelist(chunk.file, this.options.chunkSize).then((filelist) => {
          this.lostfiles = checkFileList(filelist, that.filelist)
          if (this.lostfiles && this.lostfiles.length > 0) {
            if (window._i18n && window._i18n.locale && window._i18n.locale === 'zh') {
              that.cancelUploder(`缺失 ${this.lostfiles[0]} 等${this.lostfiles.length}个文件, 请检查上传的目录`)
            } else {
              that.cancelUploder(`${this.lostfiles.length} files such as ${this.lostfiles[0]} are missing. Please check the uploaded directory`)
            }
          }
          chunk.preprocessFinished()
        })
      } else {
        chunk.preprocessFinished()
      }
    }
  }
}
</script>

<style>
  .uploader-file-actions{
     /* 把操作按钮都藏起来 */
    display: none !important;
  }
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
