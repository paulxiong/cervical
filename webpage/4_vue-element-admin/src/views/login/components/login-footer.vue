<template>
  <el-footer class="login-footer flex">{{ value }}<el-link v-if="env === 'development'" class="link" type="info" :underline="false" href="http://dev.medical.raidcdn.cn:3000/swagger/index.html" target="_blank">Swagger</el-link></el-footer>
</template>

<script>
export default {
  name: 'LoginFooter',
  components: {},
  data() {
    return {
      value: 'feedback | about us | Cervical Cancer AI',
      env: process.env.NODE_ENV
    }
  },
  methods: {}
}
</script>

<style lang="scss" scoped>
.login-footer {
  width: 100%;
  height: 7%;
  background: #fff;
  position: fixed;
  bottom: 0;
  font-size: 14px;
  .link {
    margin-left: 15px;
  }
}
</style>
