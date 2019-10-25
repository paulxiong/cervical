<template>
  <el-header class="login-header flex">
    <img class="logo" src="../../../assets/logo.png" alt="xd-logo">
    <p class="p">{{ value }}</p>
  </el-header>
</template>

<script>
export default {
  name: 'Loginheader',
  components: {},
  data() {
    return {
      value: '讯动科技'
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
  }
}
</style>
