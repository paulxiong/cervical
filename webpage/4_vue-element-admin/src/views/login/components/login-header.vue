<template>
  <el-header class="login-header flex">
    <img class="logo" src="../../../assets/logo.png" alt="xd-logo">
    <p class="p">{{ version }}<span>-{{ subversion }}</span></p>
  </el-header>
</template>

<script>
const config = require('../../../../version.config')
export default {
  name: 'Loginheader',
  components: {},
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
