<template>
  <div class="upload flex">
    <div class="change-type">
      <el-form
        ref="args"
        :model="args"
        :rules="rules"
        class="login-container"
        label-position="left"
        label-width="0px"
      >
        <el-form-item prop="description" style="text-align: left" :required="form.inputdesc">
          <span style="color: blue;">{{ $t('workspace.modelUploadDesc') }}</span>
          <el-input
            v-model="args.description"
            prefix-icon="icon iconfont el-icon-qianniu-account"
            type="text"
            autofocus
            auto-complete="off"
            :placeholder="$t('workspace.modelUploadDesc2')"
            show-word-limit
            maxlength="30"
            class="input-name"
            style="margin-right:50px; width: 75%"
            clearable
            @change="inputChange"
          />
        </el-form-item>
        <el-form-item prop="type" style="text-align: left" required>
          <span style="color: blue;">{{ $t('workspace.modelUploadType') }}</span>
          <br>
          <el-select v-model="args.type" :placeholder="$t('workspace.modelUploadType2')" style="margin-right:100px;" :disabled="isSelect" @change="selectChange">
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
        <div class="el-upload__text" style="color: blue;"><b>{{ $t('workspace.modelUploadUp') }}</b></div>
        <el-button style="margin-top: 10px;" size="mini" type="danger" @click.stop="abortUpload">{{ $t('workspace.modelUploadCancel') }}</el-button>
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
        description: [{ required: true, message: this.$t('workspace.modelUploadRuleDesc'), trigger: 'blur' }],
        type: [{ required: true, message: this.$t('workspace.modelUploadRuleType'), trigger: 'blur' }]
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
        label: this.$t('workspace.modelTypeSeg')
      }, {
        type: 6,
        label: this.$t('workspace.modelTypeClassification')
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
        this.$message.error(this.$t('workspace.modelUploadOnlyH5'))
        return isH5
      } else {
        document.querySelector('.el-upload-list').className += ' list-container'
      }
    },
    onError(response, file, fileList) {
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
