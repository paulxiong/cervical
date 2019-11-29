<template>
  <div class="emailData">
    <el-switch
      v-model="referer_en"
      active-text="开"
      inactive-text="关"
    />
  </div>
</template>

<script>

import { getReferer } from '@/api/system'

export default {
  name: 'ImgServer',
  data() {
    return {
      referer_en: 1,
      referers: [],
      referer_404_url: '',
      referer_401_url: ''
    }
  },
  created() {
    this.getReferer()
  },
  methods: {
    getReferer() {
      getReferer().then(res => {
        const { data } = res.data
        this.referer_en = data.referer_en
        this.referers = data.referers
        this.referer_404_url = data.referer_404_url
        this.referer_401_url = data.referer_401_url
      })
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

