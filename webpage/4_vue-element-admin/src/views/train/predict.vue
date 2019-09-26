<template>
  <div class="predict">
    <section class="header">
      <div class="title">
        <h2>PREDICT</h2>
      </div>
    </section>
    <modelSelect></modelSelect>
  </div>
</template>

<script>
import modelSelect from './components/model-select'

export default {
  name: 'Predict',
  components: { modelSelect },
  data() {
    return {}
  },
  methods: {}
}
</script>

<style lang="scss" scoped>
.predict {
  padding: 0 30px;
}
</style>
