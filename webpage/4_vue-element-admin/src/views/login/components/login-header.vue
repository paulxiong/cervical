<template>
  <div class="login-header flex">
    <img class="logo" src="../../../assets/logo.png" alt="xd-logo" />
    <p class="p">{{value}}</p>
  </div>
</template>

<script>
export default {
  name: "login-header",
  components: {},
  data() {
    return {
      value: "讯动科技"
    };
  },
  methods: {}
};
</script>

<style lang="scss" scoped>
.login-header {
  width: 100%;
  height: 80px;
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