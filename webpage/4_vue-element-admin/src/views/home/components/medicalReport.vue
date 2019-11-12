<template>
  <div class="medicalReport">{{ value }}</div>
</template>

<script>
export default {
  name: 'MedicalReport',
  components: {},
  data() {
    return {
      value: 'medicalReport'
    }
  },
  methods: {}
}
</script>

<style lang="scss" scoped>
.medicalReport {
    width: 100%;
    height: 341px;
    background: #fff;
    padding-top: 7px;
}
</style>
