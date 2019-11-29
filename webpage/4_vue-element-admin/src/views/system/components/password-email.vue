<template>
  <div class="components-container">
    <aside>
      <el-button type="primary" size="mini" @click="saveEmailConfig">保存设置</el-button>
      <el-button type="danger" @click="resetForm">初始化邮件格式</el-button>
      设置发送验证码的邮件的样式，验证用000000代替，用户的邮箱用email@gmail.com代替。后台发送的时候通过字符串替换换成对应用户的邮箱和验证码
    </aside>
    <div class="content flex">
      <tinymce v-show="reset" v-model="resetContent" :height="540" style="width: 48%;" />
      <tinymce v-show="!reset" v-model="content" :height="540" style="width: 48%;" />
      <div class="editor-content" style="width: 48%;" v-html="reset ? resetContent : content" />
    </div>
  </div>
</template>

<script>
import Tinymce from '@/components/Tinymce'
import { getEmail, updateEmail } from '@/api/system'
export default {
  name: 'TinymceDemo',
  components: { Tinymce },
  data() {
    return {
      resetContent: '<h1 style="text-align: left;">忘记密码验证码</h1><p>&nbsp;</p><p style="text-align: left;">尊敬的用户:</p><p style="text-align: left;">&nbsp;&nbsp;&nbsp;&nbsp;您好，您正在使用<span style="color: #3366ff;"><a href="mailto:email@gmail.com邮" target="_blank" rel="noopener">email@gmail.com</a></span>邮箱在讯动医疗页面修改密码</p><p style="text-align: left;">&nbsp;&nbsp;&nbsp;&nbsp;您的验证码为：<span style="color: red; font-weight: bold;">000000</span><span style="color: green;"> (10分钟内有效)</span></p><h6 style="text-align: left;">&nbsp; &nbsp; <span style="color: #999999;">如果不是本人操作，请您忽略这封邮件。使用中遇到任何问题，请联系我们为您解决，邮箱：xundong_km1@163.com</span></h6><p>&nbsp;</p><hr /><p style="text-align: right;">谢谢！</p><p style="text-align: right;">讯动医疗团队</p>',
      content: '',
      reset: false
    }
  },
  created() {
    this.getContent()
  },
  methods: {
    saveEmailConfig() {
      updateEmail({ 'content': this.reset ? this.resetContent : this.content, 'type': 2 }).then(res => {
        if (res.data.data === 'ok') {
          this.$message({
            message: '忘记密码邮件格式保存成功',
            type: 'success'
          })
        }
      })
    },
    getContent() {
      getEmail({ 'type': 2 }).then(res => {
        this.content = res.data.data.email_forgot_content || ''
      })
    },
    resetForm() {
      this.reset = true
    }
  }
}
</script>

<style lang="scss" scoped>
.content {
    justify-content: space-between;
    align-items: flex-start;
}
</style>
