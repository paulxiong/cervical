<template>
  <div>
    <uploader
      ref="uploader"
      :options="options"
      class="uploader-example"
      @files-submitted="onfilesSubmitted"
      @complete="oncomplete"
    >
      <uploader-unsupport />
      <uploader-drop>
        <p>Drop files here to upload or</p>
        <el-link href="https://github.com/simple-uploader/vue-uploader/blob/master/README_zh-CN.md">上传组件文档地址</el-link>
        <uploader-btn>select files</uploader-btn>
        <uploader-btn :attrs="attrs">select images</uploader-btn>
        <uploader-btn :attrs="attrs" :directory="true">select folder</uploader-btn>
      </uploader-drop>
      <uploader-list />
    </uploader>
  </div>
</template>

<script>
import { APIUrl } from '@/const/config'
import { getToken } from '@/utils/auth'
import { dateformat4, dateformat5 } from '@/utils/dateformat'

export default {
  data() {
    return {
      options: {
        target: APIUrl + '/api1/uploaddir',
        query: this.getqueryfunc,
        headers: {
          'Authorization': getToken()
        },
        simultaneousUploads: 1, // 只准有一个上传队列
        testChunks: false
      },
      attrs: {
        accept: 'image/* text/*'
      },
      uploaderInstance: null,
      dirname: ''
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.uploaderInstance = this.$refs.uploader
    })
  },
  methods: {
    getqueryfunc(val, val2) {
      console.log('getqueryfunc', val, val2)
      return { 'mid': `b${dateformat5()}`, 'bid': `b${dateformat4()}`, 'dir': this.dirname }
    },
    // 上传文件开始之前触发，后面这里要检查文件是否完整，不完整就不要上传
    onfilesSubmitted(files, fileList, event) {
      if (fileList[0].name) {
        this.dirname = fileList[0].name // 被上传的文件夹的名字
      }
      var hasScanTxt = false
      files.map(v => {
        console.log(v)
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
      }
    },
    oncomplete() {
    }
  }
}
</script>

<style>
  .uploader-example {
    width: 880px;
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
