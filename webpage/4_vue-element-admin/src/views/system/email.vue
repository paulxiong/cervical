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
        <p style="text-align: left;">尊敬的用户:</p>
        <p style="text-align: left;">&nbsp;&nbsp;&nbsp;&nbsp;您好，您正在使用<span style="color: blue;"><sub>****</sub>xundong@gmail.com</span>注册账号</p>
        <p style="text-align: left;">&nbsp;&nbsp;&nbsp;&nbsp;您的注册验证码为：<span style="color: red; font-weight: bold;">000000</span><span style="color: green;">&nbsp;(10分钟内有效)</span></p>
        <p style="text-align: left;">&nbsp;&nbsp;&nbsp;&nbsp;感谢您本次的使用</p>
        <br/>
        <hr/>
        <p style="text-align: right;">谢谢！</p>
        <p style="text-align: right;">讯动医疗团队</p>
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
