<template>
  <div class="home">
    <el-tabs v-model="activeName" class="tabs" @tab-click="handleClick">
      <el-tab-pane label="项目" name="project">
        <projectData />
      </el-tab-pane>
      <el-tab-pane label="数据集" name="datasets">
        <datasetsData />
      </el-tab-pane>
      <el-tab-pane label="模型" name="model">
        <modelData />
      </el-tab-pane>
      <el-tab-pane label="回收站" name="recycle">
        <recycleData />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import projectData from './components/project-data'
import datasetsData from './components/datasets-data'
import modelData from './components/model-data'
import recycleData from './components/recycle-data'

export default {
  name: 'Home',
  components: { projectData, datasetsData, modelData, recycleData },
  data() {
    return {
      switchVal: true,
      activeName: 'project'
    }
  },
  methods: {
    handleClick(tab, event) {
      console.log(tab, event)
    }
  }
}
</script>

<style lang="scss" scoped>
.home {
  padding: 0 30px;
}
</style>
