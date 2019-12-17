<template>
  <div class="emailData">
    <el-tabs v-model="activeName" class="tabs">
      <el-tab-pane label="邮件参数设置" name="setvariable">
        <setvariableEmail />
      </el-tab-pane>
      <el-tab-pane label="注册验证邮件" name="register">
        <registerEmail />
      </el-tab-pane>
      <el-tab-pane label="忘记密码邮件" name="password">
        <passwordEmail />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import registerEmail from './components/register-email'
import passwordEmail from './components/password-email'
import setvariableEmail from './components/setvariable-email'

export default {
  name: 'EmailData',
  components: { registerEmail, passwordEmail, setvariableEmail },
  data() {
    return {
      activeName: 'register'
    }
  }
}
</script>

<style lang="scss" scoped>
.emailData {
  height: 100%;
  padding: 0px 30px;
}
</style>

