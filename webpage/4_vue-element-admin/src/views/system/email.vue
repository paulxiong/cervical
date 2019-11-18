<template>
  <div class="components-container">
    <aside>
      讯动医疗邮件设置页面
      <el-button type="primary">保存设置</el-button>
    </aside>
    <div class="content flex">
      <tinymce v-model="content" :height="540" style="width: 48%;" />
      <div class="editor-content" style="width: 48%;" v-html="content" />
    </div>
  </div>
</template>

<script>
import Tinymce from '@/components/Tinymce'
export default {
  name: 'TinymceDemo',
  components: { Tinymce },
  data() {
    return {
      content:
      `
        <h1 style="text-align: left;">讯动医疗邮箱注册验证码</h1>
        <br/>
        <p style="text-align: left;">您好，您正在使用****xundong@gmail.com注册账号。 您的注册验证码为：000000</p>
        <br/>
        <hr/>
        <p style="text-align: right;">谢谢！</p>
      `
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
