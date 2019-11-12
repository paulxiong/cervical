<template>
  <div class="markingProgress">{{ value }}</div>
</template>

<script>
export default {
  name: 'MarkingProgress',
  components: {},
  data() {
    return {
      value: 'markingProgress'
    }
  },
  methods: {}
}
</script>

<style lang="scss" scoped>
.markingProgress {
    width: 100%;
    height: 296px;
    background: #fff;
    padding-top: 7px;
}
</style>
