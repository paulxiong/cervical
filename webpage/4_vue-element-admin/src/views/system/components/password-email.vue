<template>
  <div class="components-container">
    <aside>
      <el-button type="primary" @click="saveEmailConfig">保存设置</el-button>
      设置发送验证码的邮件的样式，验证用000000代替，用户的邮箱用email@gmail.com代替。后台发送的时候通过字符串替换换成对应用户的邮箱和验证码
    </aside>
    <div class="content flex">
      <tinymce v-model="content" :height="540" style="width: 48%;" />
      <div class="editor-content" style="width: 48%;" v-html="content" />
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
      loading: true,
      content: '',
      type: 2 // 0未知 1注册 2忘记密码
    }
  },
  created() {
    this.getEmail(this.type)
  },
  methods: {
    saveEmailConfig() {
      updateEmail({ 'content': this.content, 'type': this.type })
    },
    getEmail(type) {
      this.loading = true
      getEmail({ 'type': type }).then(res => {
        this.content = res.data.data.email_forgot_content
      })
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
