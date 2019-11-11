<template>
  <div class="bestModel">{{ value }}</div>
</template>

<script>
export default {
  name: 'BestModel',
  components: {},
  data() {
    return {
      value: 'bestModel'
    }
  },
  methods: {}
}
</script>

<style lang="scss" scoped>
.bestModel {
    width: 100%;
    height: 340px;
    background: #fff;
    padding-top: 7px;
}
</style>
