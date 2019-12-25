<template>
  <div class="review">
    <el-tabs v-model="activeName" class="tabs">
      <el-tab-pane label="分配任务" name="assignment">
        <reviewAssignment :activename="activeName" />
      </el-tab-pane>
      <el-tab-pane label="细胞类型审核" name="review">
        <reviewPage :activename="activeName" />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import reviewAssignment from './components/reviewassignment'
import reviewPage from './components/reviewpage'

export default {
  name: 'Review',
  components: { reviewAssignment, reviewPage },
  data() {
    return {
      activeName: 'assignment'
    }
  }
}
</script>

<style lang="scss" scoped>
.home {
  padding: 0 30px;
}
</style>
