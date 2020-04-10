<template>
  <div class="upload flex">
    <div class="change-type">
      <el-form
        ref="args"
        v-loading="loading"
        :model="args"
        :rules="rules"
        class="login-container"
        label-position="left"
        label-width="0px"
      >
        <el-form-item prop="description" style="text-align: left" :required="form.inputdesc">
          <span style="color: blue;"> *1.请输入上传模型描述信息：</span>
          <el-input
            v-model="args.description"
            prefix-icon="icon iconfont el-icon-qianniu-account"
            type="text"
            autofocus
            auto-complete="off"
            placeholder="请输入模型描述"
            show-word-limit
            maxlength="30"
            class="input-name"
            style="margin-right:50px; width: 75%"
            clearable
            @change="inputChange"
          />
        </el-form-item>
        <el-form-item prop="type" style="text-align: left" required>
          <span style="color: blue;"> *2.请选择上传模型类型：</span>
          <br>
          <el-select v-model="args.type" placeholder="请选择类型" style="margin-right:100px;" :disabled="isSelect" @change="selectChange">
            <el-option
              v-for="item in options"
              :key="item.type"
              :label="item.label"
              :value="item.type"
            />
          </el-select>
        </el-form-item>
      </el-form>
    </div>
    <div class="uploadmodel">
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
        :auto-upload="true"
        :on-error="onError"
        :before-upload="beforeUpload"
        :on-change="onChange"
        :disabled="isUpload"
      >
        <i class="el-icon-upload" />
        <div class="el-upload__text" style="color: blue;"><b>*3.将模型文件拖到此处或点击上传,只能上传h5/H5文件</b></div>
        <el-button style="margin-top: 10px;" size="mini" type="danger" @click.stop="abortUpload">取消上传</el-button>
      </el-upload>
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
      form: {
        inputdesc: true,
        description: ''
      },
      rules: {
        description: [{ required: true, message: '请输入上传模型描述信息', trigger: 'blur' }],
        type: [{ required: true, message: '请选择上传模型类型', trigger: 'blur' }]
      },
      finishedFileList: 0,
      fileList: 0,
      postData: {},
      inputName: '',
      modeltype: 0,
      uploadServer: false,
      modelChecked: false,
      isSelect: true,
      isUpload: true,
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
    inputChange() {
      this.isSelect = false
    },
    selectChange() {
      this.isUpload = false
    },
    beforeUpload() {
      this.postData.type = this.modeltype
      this.postData.pid = 0
      this.postData.description = this.inputName
      this.postData.precision1 = 0.0
      this.postData.recall = 0.0
      localStorage.setItem('POST_DATA', JSON.stringify(this.postData))
    },
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
      console.log(file)
      const isH5 = file.name.slice(-3) === '.h5' || file.name.slice(-3) === '.H5'
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
      localStorage.setItem('TAB', 'model')
      // this.$router.go({ path: '/workSpace' })
    },
    closeWindows() {
      this.$refs.upload.clearFiles()
      localStorage.setItem('TAB', 'model')
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
    max-height: 300;
  }
  /deep/.list-container {
    overflow-y: auto;
    height: 50px;
  }
  .change-type {
    margin-right: 5%;
    position: relative;
  }
  .successupload {
    position: absolute;
    right: 0px;
    bottom: 0px;
  }
  .upload-models {
    margin-left: -100px;
  }
}
</style>
