<template>
  <div class="testData">
    <el-tabs v-model="activeName" class="tabs">
      <el-tab-pane label="项目" name="project">
        <project :activename="activeName" />
      </el-tab-pane>
      <el-tab-pane label="项目历史记录" name="result">
        <result :activename="activeName" />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import project from './components/project'
import result from './components/result'

export default {
  components: { project, result },
  data() {
    return {
      activeName: localStorage.getItem('TAB') || 'project'
    }
  },
  mounted() {
  },
  methods: {
  }
}
</script>

<style lang="scss" scoped>
.testData {
  overflow: auto;
  height: 100%;
  padding-bottom: 30px;
  .tools {
    background: #fff;
    justify-content: space-around;
    bottom: 0px;
    position: fixed;
    left: 0;
    right: 0;
    margin-left: auto;
    margin-right: auto;
  }
}
</style>
