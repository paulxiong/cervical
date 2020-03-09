<template>
  <div class="review">
    <keep-alive>
      <router-view v-if="$route.meta.keepAlive" />
    </keep-alive>
    <router-view v-if="!$route.meta.keepAlive" />
    <el-tabs v-model="activeName" class="tabs">
      <el-tab-pane label="细胞类型审核" name="review">
        <reviewPage :activename="activeName" />
      </el-tab-pane>
      <el-tab-pane label="分配任务" name="assignment">
        <reviewAssignment :activename="activeName" />
      </el-tab-pane>
      <el-tab-pane label="按得分分配任务" name="assignment2">
        <reviewAssignment2 :activename="activeName" />
      </el-tab-pane>
      <el-tab-pane label="下载已审核" name="download">
        <reviewDownload :activename="activeName" />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import reviewAssignment from './components/reviewassignment'
import reviewAssignment2 from './components/reviewassignment2'
import reviewPage from './components/reviewpage'
import reviewDownload from './components/reviewdownload'

export default {
  name: 'Review',
  components: { reviewAssignment, reviewPage, reviewAssignment2, reviewDownload },
  data() {
    return {
      activeName: 'review'
    }
  }
}
</script>

<style lang="scss" scoped>
.review {
  padding: 0 30px;
}
</style>
