<template>
  <div class="label flex">
    <section class="main">
      321
    </section>
    <section class="info">
      123
    </section>
  </div>
</template>

<script>
export default {
  name: 'Label',
  components: {},
  data() {
    return {
      value: 'label'
    }
  }
}
</script>

<style lang="scss" scoped>
.label {
  padding-top: 20px;
  height: 720px;
  justify-content: space-between;
  align-items: flex-start;
  .main {
    background: #ccc;
    width: 80%;
    height: 100%;
  }
  .info {
    width: 20%;
    height: 100%;
    background: #666;
  }
}
</style>
