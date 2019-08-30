<template>
  <div class="login-footer flex">{{value}}</div>
</template>

<script>
export default {
  name: "login-footer",
  components: {},
  data() {
    return {
      value: "反馈建议 | 关于我们 | 备案号-滇43876513123"
    }
  },
  methods: {}
}
</script>

<style lang="scss" scoped>
.login-footer {
  width: 100%;
  height: 50px;
  background: #fff;
  position: fixed;
  bottom: 0;
  font-size: 14px;
}
</style>
