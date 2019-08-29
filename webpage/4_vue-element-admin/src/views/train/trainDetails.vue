<template>
  <div class="trainDetails">
    <tabBar></tabBar>
  </div>
</template>

<script>
import tabBar from "./components/tabBar";
export default {
  name: "trainDetails",
  components: { tabBar },
  data() {
    return {
      value: "trainDetails"
    };
  },
  methods: {}
};
</script>

<style lang="scss" scoped>
.trainDetails {
}
</style>
