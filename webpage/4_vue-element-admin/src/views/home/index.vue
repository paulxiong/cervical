<template>
  <div class="home">
    <tabBar></tabBar>
  </div>
</template>

<script>
import tabBar from "./components/tabBar";
export default {
  name: "home",
  components: { tabBar },
  data() {
    return {
      value: "home"
    };
  },
  methods: {}
};
</script>

<style lang="scss" scoped>
.home {
}
</style>
