<template>
  <div class="reportData">
    <keep-alive>
      <router-view v-if="$route.meta.keepAlive" />
    </keep-alive>
    <!-- <router-view v-if="!$route.meta.keepAlive" /> -->
    <el-tabs v-model="activeName" class="tabs" @tab-click="handleClick">
      <el-tab-pane :label="$t('label.label')" name="LabelHome">
        <labellist />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import labellist from './components/labellist'

export default {
  name: 'LabelHome',
  components: { labellist },
  data() {
    return {
      activeName: 'LabelHome'
    }
  },
  mounted() {
    this.activeName = 'LabelHome'
  },
  methods: {
    handleClick(tab, event) {}
  }
}
</script>

<style lang="scss" scoped>
.reportData {
  overflow: auto;
  height: 100%;
  padding: 0 30px;
}
</style>
