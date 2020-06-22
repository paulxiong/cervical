<template>
  <el-header class="login-header flex">
    <img class="logo" src="../../../assets/logo.png" alt="xd-logo">
    <div class="header-right">
      <p class="p">{{ version }}<span>-{{ subversion }}</span></p>
      <SetLang class="header-right-lang" />
    </div>
  </el-header>
</template>

<script>
const config = require('../../../../version.config')
import SetLang from '@/components/setlang'
export default {
  name: 'Loginheader',
  components: { SetLang },
  data() {
    return {
      version: config.version,
      subversion: config.subversion
    }
  },
  methods: {}
}
</script>

<style lang="scss" scoped>
.login-header {
  width: 100%;
  height: 10%;
  background: #fff;
  justify-content: space-between;
  position: fixed;
  padding: 0 30px;
  top: 0;
  .header-right {
    display: flex;
    .header-right-lang {
      display: block;
      margin-block-start: 1em;
      margin-block-end: 1em;
      margin-inline-start: 0px;
      margin-inline-end: 0px;
      margin-left: 10px;
      width: 75px;
    }
  }
  .logo {
    width: 120px;
  }
  .p {
    color: #ccc;
    span {
      font-size: 12px;
    }
  }
}
</style>
