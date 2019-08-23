<template>
  <div class="evaluate">
    <modelSelect></modelSelect>
  </div>
</template>

<script>
import modelSelect from "./components/model-select";

export default {
  name: "evaluate",
  components: { modelSelect },
  data() {
    return {};
  },
  methods: {}
};
</script>

<style lang="scss" scoped>
.evaluate {
  padding: 0 30px;
}
</style>