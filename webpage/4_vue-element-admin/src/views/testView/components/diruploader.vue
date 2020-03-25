<template>
  <div>
    <uploader
      ref="uploader"
      :options="options"
      class="uploader-example"
      @files-submitted="onfilesSubmitted"
      @complete="complete"
    >
      <uploader-unsupport />
      <uploader-drop>
        <p>Drop files here to upload or</p>
        <el-link href="https://github.com/simple-uploader/vue-uploader/blob/master/README_zh-CN.md">上传组件文档地址</el-link>
        <uploader-btn>select files</uploader-btn>
        <uploader-btn :attrs="attrs">select images</uploader-btn>
        <uploader-btn :directory="true">select folder</uploader-btn>
      </uploader-drop>
      <uploader-list />
    </uploader>
  </div>
</template>

<script>
import { getToken } from '@/utils/auth'

export default {
  data() {
    return {
      options: {
        // https://github.com/simple-uploader/Uploader/tree/develop/samples/Node.js
        target: '//localhost:9000/api1/uploaddir',
        query: { 'mid': '', 'bid': '' },
        headers: {
          'Authorization': getToken()
        },
        testChunks: false
      },
      attrs: {
        accept: 'image/*'
      },
      uploaderInstance: null
    }
  },
  created() {
    this.options.query = { 'mid': 3, 'bid': 4 }
  },
  mounted() {
    this.$nextTick(() => {
      this.uploaderInstance = this.$refs.uploader.uploader
    })
  },
  methods: {
    onfilesSubmitted(files, fileList, event) {
      console.log(files)
    },
    complete() {
      console.log(this.uploaderInstance.File.name)
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
