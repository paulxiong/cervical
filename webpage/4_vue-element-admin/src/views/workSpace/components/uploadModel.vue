<template>
  <div class="upload flex">
    <el-input
      v-model="args.description"
      autofocus
      placeholder="输入模型描述"
      show-word-limit
      maxlength="30"
      class="input-name"
    />
    <el-upload
      ref="upload"
      class="upload-models"
      :action="APIUrl"
      :headers="headers"
      :data="args"
      drag
      :limit="parseInt('1')"
      show-file-list
      :on-success="onSuccess"
      :auto-upload="false"
      :on-error="onError"
      :on-change="onChange"
    >
      <i class="el-icon-upload" />
      <div class="el-upload__text">将模型文件拖到此处,只能上传h5/H5文件</div>
      <el-button
        style="margin: 10px 0 0 20px;"
        size="mini"
        type="success"
        @click.stop="submitUpload"
      >上传到服务器并创建模型 {{ finishedFileList }} / {{ fileList }}</el-button>
      <el-button style="margin-left: 10px;" size="mini" type="danger" @click.stop="abortUpload">取消上传</el-button>
    </el-upload>
    <el-select v-model="args.type" placeholder="请选择">
      <el-option
        v-for="item in options"
        :key="item.type"
        :label="item.label"
        :value="item.type"
      />
    </el-select>
  </div>
</template>

<script>
import { getToken } from '@/utils/auth'
import { APIUrl } from '@/const/config'

export default {
  name: 'UploadModel',
  components: {},
  data() {
    return {
      userInfo: JSON.parse(localStorage.getItem('USER_INFO')),
      APIUrl: APIUrl + '/api1/uploadmodel',
      headers: {
        'Authorization': getToken()
      },
      args: {
        'type': 0,
        'pid': 0,
        'description': '',
        'precision1': 0.0,
        'recall': 0.0
      },
      finishedFileList: 0,
      fileList: 0,
      postData: {},
      inputName: '',
      modeltype: 0,
      options: [{
        type: 4,
        label: '切割'
      }, {
        type: 6,
        label: '细胞分类'
      }]
    }
  },
  created() {
  },
  methods: {
    submitUpload() {
      this.postData.type = this.modeltype
      this.postData.pid = 0
      this.postData.description = this.inputName
      this.postData.precision1 = 0.0
      this.postData.recall = 0.0
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
    onChange(file) {
      console.log(file.type, file.raw.type)
      const isH5 = file.raw.type === 'application/x-hdf'
      if (!isH5) {
        this.$message.error('只能上传h5/H5文件')
        return isH5
      } else {
        document.querySelector('.el-upload-list').className += ' list-container'
      }
    },
    onError(response, file, fileList) {
      console.log(response, file, fileList)
      console.log('上传失败！')
    },
    abortUpload() {
      this.$refs.upload.abort()
      this.$refs.upload.clearFiles()
      document.querySelector('.el-upload-list').remove('list-container')
    },
    uploadSuccess(file) {
      const formData = new FormData()
      formData.append('file', file.file)
      this.filesList = formData
      this.fileName = file.file.name
      return ({
        APIUrl: APIUrl + '/api1/uploadmodel',
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
  /deep/.list-container {
    overflow-y: auto;
    height: 300px;
  }
}
</style>
