<template>
  <div class="upload flex">
    <el-upload
      ref="upload"
      class="upload-imgs"
      :action="APIUrl"
      :headers="headers"
      :data="args"
      drag
      multiple
      show-file-list
      :file-list="imgList"
      :before-upload="beforeUpload"
      :on-success="onSuccess"
      :auto-upload="false"
    >
      <i class="el-icon-upload" />
      <div class="el-upload__text">将多张/单张图片文件拖到此处</div>
      <div slot="tip" class="el-upload__tip">只能上传png/jpg/png文件</div>
      <el-button
        style="margin: 10px 0 0 20px;"
        size="mini"
        type="success"
        @click.stop="submitUpload"
      >上传到服务器 {{ finishedFileList }} / {{ fileList }}</el-button>
      <el-button style="margin-left: 10px;" size="mini" type="danger" @click.stop="abortUpload">取消上传</el-button>
    </el-upload>
  </div>
</template>

<script>
import { getToken } from '@/utils/auth'
import { APIUrl } from '@/const/config'

export default {
  name: 'Upload',
  components: {},
  data() {
    return {
      userInfo: JSON.parse(localStorage.getItem('USER_INFO')),
      APIUrl: APIUrl + '/api1/upload',
      headers: {
        'Authorization': getToken()
      },
      args: {},
      finishedFileList: 0,
      fileList: 0,
      postData: {
        'batchids': [],
        'medicalids': []
      }
    }
  },
  created() {
    const y = new Date().getFullYear()
    const m = new Date().getMonth() + 1
    const d = new Date().getDate()
    const nowDate = new Date(`${y}-${m}-${d}`).getTime()
    const now = new Date().getTime()
    this.args = {
      'bid': `b${nowDate}${this.userInfo.id}`,
      'mid': `m${now}${this.userInfo.id}`
    }
  },
  methods: {
    submitUpload() {
      this.postData.batchids = [this.args.bid]
      this.postData.medicalids.push(this.args.mid)
      localStorage.setItem('POST_DATA', JSON.stringify(this.postData))
      this.$nextTick(() => {
        this.$refs.upload.submit()
        console.log(this.APIUrl)
      })
    },
    onSuccess(response, file, fileList) {
      this.fileList = fileList.length
      this.finishedFileList = fileList.filter(v => v.percentage === 100).length
      if (fileList[fileList.length - 1].percentage === 100) {
        this.$emit('checkUpload', true)
      }
    },
    abortUpload() {
      this.$refs.upload.abort()
    },
    beforeUpload(file) {
      const isPNG = file.type === 'image/png'
      const isJPG = file.type === 'image/jpg'
      const isJPEG = file.type === 'image/jpeg'
      if (!isPNG && !isJPG && !isJPEG) {
        this.$message.error('只能上传图片格式')
      }
      return isPNG || isJPG || isJPEG
    },
    uploadSuccess(file) {
      const formData = new FormData()
      formData.append('file', file.file)
      this.filesList = formData
      this.fileName = file.file.name
      return ({
        APIUrl: APIUrl + '/api1/upload',
        headers: { 'Authorization': getToken() },
        data: this.filesList
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.upload {
  .upload-imgs {
    max-height: 500px;
  }
  /deep/.el-upload-list {
    overflow-y: auto;
    height: 360px;
  }
}
</style>
