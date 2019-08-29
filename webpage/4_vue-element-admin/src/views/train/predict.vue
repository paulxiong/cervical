<template>
  <div class="predict">
    <modelSelect></modelSelect>
  </div>
</template>

<script>
import modelSelect from "./components/model-select"

export default {
  name: "predict",
  components: { modelSelect },
  data() {
    return {};
  },
  methods: {}
};
</script>

<style lang="scss" scoped>
.predict {
  padding: 0 30px;
}
</style>
