<template>
  <div class="upload flex">
    <div class="change-type">
      <span style="display: flex; justify-content:center; align-items:center font-size=: 15px; color: blue; margin-bottom: 5px; margin-right:80px;">*1.请输入上传模型描述信息</span>
      <el-input
        v-model="args.description"
        autofocus
        placeholder="请输入模型描述"
        show-word-limit
        maxlength="30"
        class="input-name"
        style="margin-bottom: 50px; margin-right:50px;"
        clearable
      />
      <span style="display: flex; justify-content:center; align-items:center font-size=: 15px; color: blue; margin-bottom: 5px; margin-top:5px; margin-right:100px;">*2.请选择上传模型类型</span>
      <el-select v-model="args.type" placeholder="请选择类型" style="margin-right:100px;">
        <el-option
          v-for="item in options"
          :key="item.type"
          :label="item.label"
          :value="item.type"
        />
      </el-select>
    </div>
    <el-upload
      ref="upload"
      class="upload-models"
      accept=".h5,.H5"
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
      <div class="el-upload__text" style="color: red;"><b>*3.将模型文件拖到此处或点击上传,只能上传h5/H5文件</b></div>
      <el-button
        style="margin: 10px 0 0 20px;"
        size="mini"
        type="success"
        @click.stop="submitUpload"
      >上传到服务器并创建模型 {{ finishedFileList }} / {{ fileList }}</el-button>
      <el-button style="margin-left: 10px;" size="mini" type="danger" @click.stop="abortUpload">取消上传</el-button>
    </el-upload>
    <div class="successupload">
      <el-button
        type="primary"
        :disabled="!uploadServer"
        @click="closeWindows"
      >确定</el-button>
    </div>
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
        'type': undefined,
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
      uploadServer: false,
      modelChecked: false,
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
      this.uploadServer = true
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
    closeWindows() {
      this.$refs.upload.clearFiles()
      this.$router.go({ path: '/workSpace' })
    },
    uploadSuccess(file) {
      this.uploadServer = true
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
  .upload-models {
    max-height: 500px;
  }
  /deep/.list-container {
    overflow-y: auto;
    height: 300px;
  }
  .change-type {
    margin-right: 5%;
  }
  .successupload {
    position: absolute;
    right: 0px;
    bottom: 0px;
  }
}
</style>
