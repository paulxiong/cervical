<template>
  <div class="components-container">
    <aside>
      讯动医疗邮件设置页面
      <el-button type="primary" @click="saveEmailConfig">保存设置</el-button>
    </aside>
    <div class="content flex">
      <tinymce v-model="content" :height="540" style="width: 48%;" />
      <div class="editor-content" style="width: 48%;" v-html="content" />
    </div>
  </div>
</template>

<script>
import Tinymce from '@/components/Tinymce'
import { getRegisterEmail, updateRegisterEmail } from '@/api/system'
export default {
  name: 'TinymceDemo',
  components: { Tinymce },
  data() {
    return {
      loading: true,
      content: ''
    }
  },
  created() {
    this.getRegisterEmail()
  },
  methods: {
    saveEmailConfig() {
      updateRegisterEmail({ 'content': this.content })
    },
    getRegisterEmail() {
      this.loading = true
      getRegisterEmail().then(res => {
        this.content = res.data.data.email_register_content
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
