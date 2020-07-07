<template>
  <div class="text-center">
    <div class="imgreplace">
      <img v-if="newAvatar" :src="newAvatar+'?width=160'">
      <img v-else :src="avatar+'?width=160'">
      <el-button id="pick-avatar" type="info" class="upload" round>{{ $t('system.usrUploadAvatar') }}</el-button>
    </div>
    <avatar-cropper
      trigger="#pick-avatar"
      :upload-headers="headers"
      :upload-url="uploadURL"
      @uploaded="handleUploaded"
    />
    <div class="info">
      <el-form ref="ruleForm" :model="ruleForm" :rules="rules" label-width="100px" class="demo-ruleForm">
        <el-form-item :label="$t('system.usrNickname')" prop="name">
          <el-input v-model="ruleForm.name" />
        </el-form-item>
        <el-form-item :label="$t('system.usrEmail')" prop="email">
          <el-input v-model="ruleForm.email" :disabled="true" />
        </el-form-item>
        <el-form-item :label="$t('system.usrGender')" prop="sex">
          <el-select v-model="ruleForm.sex" :placeholder="$t('system.usrGenderSelect')" class="sex">
            <el-option :label="$t('system.usrMale')" value="male" />
            <el-option :label="$t('system.usrFemale')" value="female" />
            <el-option :label="$t('system.usrSecrecy')" value="secret" />
          </el-select>
        </el-form-item>
        <el-form-item :label="$t('system.usrPhone')" prop="mobile">
          <el-input v-model="ruleForm.mobile" />
        </el-form-item>
        <el-form-item :label="$t('system.usrCreateAt')" prop="created_at">
          <el-input v-model="ruleForm.created_at" :disabled="true" />
        </el-form-item>
        <el-form-item :label="$t('system.usrIntroduce')" prop="introduction">
          <el-input v-model="ruleForm.introduction" type="textarea" :autosize="{ minRows: 10, maxRows: 20}" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" size="mini" @click="submitForm('ruleForm')">{{ $t('system.usrSave') }}</el-button>
          <el-button @click="resetForm('ruleForm')">{{ $t('system.usrReset') }}</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import AvatarCropper from 'vue-avatar-cropper'
import { APIUrl } from '@/const/config'
import { getToken } from '@/utils/auth'
import { mapGetters } from 'vuex'
import { updateUserInfo, getUserInfo } from '@/api/user'
// import { parseTime } from '@/utils/index'

export default {
  components: { AvatarCropper },
  data() {
    return {
      uploadURL: APIUrl + '/api1/uploadimg',
      newAvatar: this.avatar,
      headers: {
        'Authorization': getToken()
      },
      ruleForm: {
        name: '',
        mobile: '',
        introduction: '',
        created_at: ''
      },
      rules: {
        name: [
          { required: true, message: this.$t('system.usrEnterNickname'), trigger: 'blur' },
          { min: 2, max: 40, message: this.$t('system.usrNicknameTip'), trigger: 'blur' }
        ],
        mobile: [
          { message: this.$t('system.usrEnterPhone'), trigger: 'blur' },
          { min: 0, max: 11, message: this.$t('system.usrPhoneTip'), trigger: 'blur' }
        ],
        introduction: [
          { message: this.$t('system.usrEnterIntroduce'), trigger: 'blur' },
          { min: 0, max: 512, message: this.$t('system.usrIntroduceTip'), trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    ...mapGetters([
      'avatar',
      'introduction',
      'name',
      'mobile',
      'email'
    ])
  },
  created() {
    this.ruleForm.name = this.name
    this.ruleForm.mobile = this.mobile
    this.ruleForm.introduction = this.introduction
    this.newAvatar = this.avatar
    this.ruleForm.email = this.email
    this.ruleForm.created_at = this.created_at
  },
  methods: {
    handleUploaded(resp) {
      this.newAvatar = APIUrl + resp.data
    },
    getUserInfo() {
      getUserInfo().then(res => {
        localStorage.setItem('USER_INFO', JSON.stringify(res.data.data))
      })
    },
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          const postdata = {
            'email': this.email,
            'image': this.newAvatar,
            'mobile': this.$refs[formName].model.mobile,
            'name': this.$refs[formName].model.name,
            'introduction': this.$refs[formName].model.introduction,
            'created_at': this.$refs[formName].model.created_at
          }
          updateUserInfo(postdata).then(response => {
            this.getUserInfo()
          }).catch(error => {
            new Error(error)
          })
          this.$message({
            message: this.$t('system.usrUpdated'),
            type: 'success'
          })
        } else {
          this.$message({
            message: this.$t('system.usrFillAgain'),
            type: 'danger'
          })
          return false
        }
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    }
  }
}
</script>

<style lang="scss" scoped>
.imgreplace {
  overflow: auto;
  float: left;
  margin: 50px;
}
.upload {
  margin-top: 200px;
  position: absolute;
  margin-left: -130px;
}
.sex {
  float: left;
}
.info {
  overflow:hidden;
  width: 40%;
  border-left: 1px solid #ccc;
  margin-top: 100px;
}
</style>
