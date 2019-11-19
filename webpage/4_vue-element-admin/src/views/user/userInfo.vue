<template>
  <div class="text-center">
    <img v-if="newAvatar" :src="newAvatar+'?width=160'">
    <img v-else :src="avatar+'?width=160'">
    <button id="pick-avatar">上传一张图片作为头像</button>
    <avatar-cropper
      trigger="#pick-avatar"
      :upload-headers="headers"
      :upload-url="uploadURL"
      @uploaded="handleUploaded"
    />

    <el-form ref="ruleForm" :model="ruleForm" :rules="rules" label-width="100px" class="demo-ruleForm">
      <el-form-item label="昵称" prop="name">
        <el-input v-model="ruleForm.name" />
      </el-form-item>
      <el-form-item label="手机" prop="mobile">
        <el-input v-model="ruleForm.mobile" />
      </el-form-item>
      <el-form-item label="介绍" prop="introduction">
        <el-input v-model="ruleForm.introduction" type="textarea" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button>
        <el-button @click="resetForm('ruleForm')">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import AvatarCropper from 'vue-avatar-cropper'
import { APIUrl } from '@/const/config'
import { getToken } from '@/utils/auth'
import { mapGetters } from 'vuex'
import { updateUserInfo } from '@/api/user'

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
        introduction: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入昵称', trigger: 'blur' },
          { min: 2, max: 40, message: '长度在 2 到 40 个字符', trigger: 'blur' }
        ],
        mobile: [
          { required: true, message: '请输入手机号(可以不填)', trigger: 'blur' },
          { min: 0, max: 11, message: '长度在 0 到 11 个字符， 可以不填', trigger: 'blur' }
        ],
        introduction: [
          { required: true, message: '请输入自我介绍', trigger: 'blur' },
          { min: 0, max: 512, message: '长度在 0 到 512 个字符', trigger: 'blur' }
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
  },
  methods: {
    handleUploaded(resp) {
      this.newAvatar = APIUrl + resp.data
      console.log(resp)
    },
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          const postdata = {
            'email': this.email,
            'image': this.newAvatar,
            'mobile': this.$refs[formName].model.mobile,
            'name': this.$refs[formName].model.name,
            'introduction': this.$refs[formName].model.introduction
          }
          updateUserInfo(postdata).then(response => {
            console.log(response)
          }).catch(error => {
            console.log(error)
          })
          console.log(postdata)
          alert('用户信息已经更新')
        } else {
          console.log('请重新填写')
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
