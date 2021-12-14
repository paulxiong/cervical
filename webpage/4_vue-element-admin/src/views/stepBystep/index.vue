<template>
  <div class="home">
    <keep-alive>
      <router-view v-if="$route.meta.keepAlive" />
    </keep-alive>
    <router-view v-if="!$route.meta.keepAlive" />
    <el-tabs v-model="activeName" class="tabs">
      <p> {{activeName}}</p>
      <el-tab-pane :label="$t('workspace.projects')" name="project">
        <projectData :activename="activeName" />
      </el-tab-pane>
      <el-tab-pane :label="$t('workspace.datasets')" name="datasets">
        <datasetsData :activename="activeName" />
      </el-tab-pane>
      <el-tab-pane :label="$t('workspace.models')" name="model">
        <modelData />
      </el-tab-pane>
      <!-- <el-tab-pane label="回收站" name="recycle">
        <recycleData />
      </el-tab-pane> -->
    </el-tabs>
  </div>
</template>

<script>
import projectData from './components/project-data'
import datasetsData from './components/datasets-data'
import modelData from './components/model-data'
// import recycleData from './components/recycle-data'

export default {
  name: 'Home',
  components: { projectData, datasetsData, modelData },
  data() {
    return {
      // activeName: localStorage.getItem('TAB') || 'project'
      activeName: 'datasets'    //*todo  dont know where the 'TAB' assgined. 
      }
  }
}
</script>

<style lang="scss" scoped>
.home {
  padding: 0 30px;
}
</style>
