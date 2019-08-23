<template>
  <div class="home">
    <tabBar></tabBar>
  </div>
</template>

<script>
import tabBar from "./components/tabBar";
export default {
  name: "temp",
  components: { tabBar },
  data() {
    return {
      value: "temp"
    };
  },
  methods: {}
};
</script>

<style lang="scss" scoped>
.temp {
}
</style>