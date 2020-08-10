<template>
  <div class="upload">
    <el-steps :space="100" direction="vertical" :active="active" finish-status="success" process-status="error">
      <el-step :title="$t('workspace.modelUploadDesc')">
        <template slot="description">
          <el-input
            ref="inputDesc"
            v-model="args.description"
            type="text"
            :autofocus="true"
            auto-complete="off"
            :placeholder="$t('workspace.modelUploadDesc2')"
            show-word-limit
            maxlength="30"
            class="input-name"
            style="margin-right:50px; width: 100%"
            clearable
            @change="inputDescChange"
            @input="inputDescChange"
          />
        </template>
      </el-step>
      <el-step :title="$t('workspace.modelUploadType')">
        <template slot="description">
          <el-select v-model="args.type" :placeholder="$t('workspace.modelUploadType2')" style="margin-right:100px;" :disabled="active<1" @change="selectChange">
            <el-option
              v-for="item in options"
              :key="item.type"
              :label="item.label"
              :value="item.type"
            />
          </el-select>
        </template>
      </el-step>
      <el-step :title="$t('workspace.modelUploadUp')">
        <template slot="description">
          <el-upload
            ref="upload"
            class="upload-models"
            accept=".h5,.H5"
            :action="APIUrl"
            :headers="headers"
            :data="args"
            :limit="parseInt('2')"
            :on-remove="handleRemove"
            :on-change="handleChange"
            :on-success="handleSuccess"
            :file-list="fileList"
            :auto-upload="false"
          >
            <el-button slot="trigger" size="small" type="primary" :disabled="active<2">{{ $t('workspace.modelUploadUp2') }}</el-button>
            <el-button v-if="needFilesNum==2" slot="trigger" style="margin-left: 10px;" size="small" type="primary" :disabled="active<2">选取配置文件</el-button>
            <div slot="tip" class="el-upload__tip">{{ $t('workspace.modelUploadUp3') }}</div>
          </el-upload>
        </template>
      </el-step>
      <el-step :title="$t('workspace.modelUploadUpConfirm')">
        <template slot="description">
          <el-button style="margin-top: 12px;" type="success" :disabled="active!==3" @click="submitUpload">{{ $t(uploadButtonText) }}</el-button>
        </template>
      </el-step>
    </el-steps>
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
      APIUrl: APIUrl + '/api1/uploadmodel',
      headers: {
        'Authorization': getToken()
      },
      args: {
        'type': '',
        'pid': 0,
        'description': '',
        'precision1': 0.0,
        'recall': 0.0
      },
      active: 0,
      uploaded: false,
      uploadButtonText: '确认并上传',
      fileList: [],
      needFilesNum: 1, // 需要上传的文件个数，yolo都是2个，其他是1个
      options: [{
        type: 4,
        label: this.$t('workspace.modelTypeSeg')
      }, {
        type: 6,
        label: this.$t('workspace.modelTypeClassification')
      }]
    }
  },
  mounted() {
    this.reset()
    this.$refs.inputDesc.focus()
  },
  created() {
  },
  methods: {
    reset() {
      this.args = {
        'type': '',
        'pid': 0,
        'description': '',
        'precision1': 0.0,
        'recall': 0.0
      }
      this.active = 0
      this.uploaded = false
      this.uploadButtonText = 'workspace.modelUploadUpConfirm2'
      this.fileList = []
      this.needFilesNum = 1 // 需要上传的文件个数，yolo都是2个，其他是1个
      this.$refs.upload.clearFiles()
    },
    checkActive() {
      if (this.active === 0) {
        if (this.args && this.args.description && this.args.description !== '') {
          this.active++
        }
      } else if (this.active === 1) {
        if (this.args && this.args.type && this.args.type !== '') {
          this.active++
        }
      } else if (this.active === 2) {
        if (this.fileList && this.fileList.length === this.needFilesNum) {
          this.active++
        }
      } else if (this.active === 3) {
        if (this.uploaded) {
          this.active++
        }
      }

      if (!this.args || !this.args.description || this.args.description === '') {
        this.active = 0
      } else if (!this.args || !this.args.type || this.args.type === '') {
        this.active = 1
      } else if (!this.fileList || this.fileList.length !== this.needFilesNum) {
        this.active = 2
      } else if (!this.uploaded) {
        this.active = 3
      }
    },
    inputDescChange() {
      this.checkActive()
    },
    selectChange() {
      if (this.args.type === 7) { // yolo
        this.needFilesNum = 2
      }
      this.checkActive()
    },
    handleChange(file, fileList) {
      this.fileList = fileList
      this.checkActive()
    },
    handleRemove(file, fileList) {
      this.fileList = fileList
      this.checkActive()
    },
    handleSuccess(response, file, fileList) {
      if (response.status === 0) {
        this.uploaded = true
        this.uploadButtonText = 'workspace.modelUploadUpFinished'
      }
      this.checkActive()
    },
    submitUpload() {
      this.$nextTick(() => {
        this.$refs.upload.submit()
        this.active = 4
      })
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
