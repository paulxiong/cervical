<template>
  <el-footer class="login-footer flex">{{value}}<el-link class="link"  type="info" :underline="false" v-if="env === 'development'" href="http://dev.medical.raidcdn.cn:3000/swagger/index.html" target="_blank">Swagger</el-link></el-footer>
</template>

<script>
export default {
  name: 'LoginFooter',
  components: {},
  data() {
    return {
      value: '反馈建议 | 关于我们 | 滇公网安备33043876513123号',
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
