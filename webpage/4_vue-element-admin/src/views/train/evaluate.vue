<template>
  <div class="evaluate">
    <section class="header">
      <div class="title">
        <h2>EVALUATE</h2>
      </div>
    </section>
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
