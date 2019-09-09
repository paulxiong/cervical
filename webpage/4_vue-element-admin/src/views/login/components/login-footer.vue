<template>
  <el-footer class="login-footer flex">{{value}}</el-footer>
</template>

<script>
export default {
  name: 'loginFooter',
  components: {},
  data() {
    return {
      value: '反馈建议 | 关于我们 | 滇公网安备33043876513123号'
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
}
</style>
