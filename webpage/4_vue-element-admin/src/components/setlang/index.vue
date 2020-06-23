<!-- i18n -->
<template>
  <div>
    <el-dropdown trigger="click" @command="handleCommand">
      <span class="el-dropdown-link">
        {{ $t('navbar.lang') }}<i class="el-icon-arrow-down el-icon--right" />
      </span>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
          :command="item.value"
        >{{ item.label }}</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
  </div>
</template>

<script>
import { getLanguage } from '@/lang'
import getPageTitle from '@/utils/get-page-title'

export default {
  data() {
    return {
      locale: 'en',
      selectValue: '',
      options: [
        {
          value: 'zh',
          label: '中文'
        }, {
          value: 'en',
          label: 'English'
        }
      ]
    }
  },
  created() {
    this.locale = getLanguage()
    this.langChange(this.locale)
  },
  methods: {
    // 语言切换
    langChange(lang) {
      this.$i18n.locale = lang // 切换
      this.$store.dispatch('app/setLanguage', lang) // 结合vuex （vuex的mutations方法结合了cookie）

      document.title = getPageTitle()
    },
    handleCommand(command) {
      this.langChange(command)
    }
  }
}
</script>
