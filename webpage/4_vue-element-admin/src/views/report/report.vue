<template>
  <div class="reportData">
    <el-tabs v-model="activeName" class="tabs" @tab-click="handleClick">
      <el-tab-pane label="医生审核" name="doctor">
        <doctorReport />
      </el-tab-pane>
      <el-tab-pane label="管理员审核" name="admin">
        <adminReport />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import adminReport from './components/admin-report'
import doctorReport from './components/doctor-report'

export default {
  name: 'ReportData',
  components: { adminReport, doctorReport },
  data() {
    return {
      activeName: 'doctor'
    }
  },
  mounted() {
    this.activeName = localStorage.getItem('REPORT_TAB') || 'doctor'
  },
  methods: {
    handleClick(tab, event) {
      localStorage.setItem('REPORT_TAB', this.activeName)
    }
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
