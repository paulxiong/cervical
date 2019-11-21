<template>
  <div class="text-center">
    <div class="imgreplace">
      <img v-if="newAvatar" :src="newAvatar+'?width=160'">
      <img v-else :src="avatar+'?width=160'">
      <el-button id="pick-avatar" type="info" class="upload" round>上传头像</el-button>
    </div>
    <avatar-cropper
      trigger="#pick-avatar"
      :upload-headers="headers"
      :upload-url="uploadURL"
      @uploaded="handleUploaded"
    />
    <div class="info">
      <el-form ref="ruleForm" :model="ruleForm" :rules="rules" label-width="100px" class="demo-ruleForm">
        <el-form-item label="昵称" prop="name">
          <el-input v-model="ruleForm.name" />
        </el-form-item>
        <el-form-item label="邮箱账号" prop="email">
          <el-input v-model="ruleForm.email" :disabled="true" />
        </el-form-item>
        <el-form-item label="性别" prop="sex">
          <el-select v-model="ruleForm.sex" placeholder="请选择您的性别" class="sex">
            <el-option label="男" value="male" />
            <el-option label="女" value="female" />
            <el-option label="保密" value="secret" />
          </el-select>
        </el-form-item>
        <el-form-item label="手机号码" prop="mobile">
          <el-input v-model="ruleForm.mobile" />
        </el-form-item>
        <el-form-item label="创建时间" prop="created_at">
          <el-input v-model="ruleForm.created_at" :disabled="true" />
        </el-form-item>
        <el-form-item label="介绍" prop="introduction">
          <el-input v-model="ruleForm.introduction" type="textarea" :autosize="{ minRows: 10, maxRows: 20}" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm')">保存</el-button>
          <el-button @click="resetForm('ruleForm')">重置</el-button>
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
            'introduction': this.$refs[formName].model.introduction
          }
          updateUserInfo(postdata).then(response => {
            this.getUserInfo()
          }).catch(error => {
            console.log(error)
          })
          this.$message({
            message: '用户信息已经更新',
            type: 'success'
          })
        } else {
          this.$message({
            message: '请重新填写',
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
.text-center {
}
.imgreplace {
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
