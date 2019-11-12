<template>
  <el-dropdown trigger="click" size="mini">
    <div>
      <svg-icon class-name="cells-icon" icon-class="cells" />
    </div>
    <el-dropdown-menu slot="dropdown">
      <el-dropdown-item v-for="(cells, idx) of cellsType" :key="idx">
        {{ cells }}
      </el-dropdown-item>
    </el-dropdown-menu>
  </el-dropdown>
</template>

<script>
import { cellsType } from '@/const/const'

export default {
  data() {
    return {
      cellsType: cellsType
    }
  },
  computed: {
    size() {
      return this.$store.getters.size
    }
  },
  methods: {
    refreshView() {
      // In order to make the cached page re-rendered
      this.$store.dispatch('tagsView/delAllCachedViews', this.$route)

      const { fullPath } = this.$route

      this.$nextTick(() => {
        this.$router.replace({
          path: '/redirect' + fullPath
        })
      })
    }
  }

}
</script>
