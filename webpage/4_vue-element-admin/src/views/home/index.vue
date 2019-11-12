<template>
  <div class="dashboard-editor-container">
    <panel-group />

    <el-row :gutter="8">
      <el-col :xs="{span: 24}" :sm="{span: 24}" :md="{span: 24}" :lg="{span: 12}" :xl="{span: 12}" style="padding-right:20px;margin-bottom:30px;">
        <transaction-table />
      </el-col>
      <el-col :xs="{span: 24}" :sm="{span: 24}" :md="{span: 24}" :lg="{span: 12}" :xl="{span: 12}" style="padding-left:20px;margin-bottom:30px;">
        <marking-progress />
      </el-col>
      <el-col :xs="{span: 24}" :sm="{span: 24}" :md="{span: 24}" :lg="{span: 12}" :xl="{span: 12}" style="padding-right:20px;margin-bottom:30px;">
        <best-model />
      </el-col>
      <el-col :xs="{span: 24}" :sm="{span: 24}" :md="{span: 24}" :lg="{span: 12}" :xl="{span: 12}" style="padding-left:20px;margin-bottom:30px;">
        <medical-report />
      </el-col>
    </el-row>
  </div>
</template>

<script>
import PanelGroup from './components/PanelGroup'
import TransactionTable from './components/TransactionTable'
import BestModel from './components/bestModel'
import MarkingProgress from './components/MarkingProgress'
import medicalReport from './components/medicalReport'

export default {
  name: 'DashboardAdmin',
  components: {
    PanelGroup,
    TransactionTable,
    BestModel,
    MarkingProgress,
    medicalReport
  }
}
</script>

<style lang="scss" scoped>
.dashboard-editor-container {
  padding: 32px;
  position: relative;
  background-color: rgb(240, 242, 245);

  .chart-wrapper {
    background: #fff;
    padding: 16px 16px 0;
    margin-bottom: 32px;
  }
}

@media (max-width:1024px) {
  .chart-wrapper {
    padding: 8px;
  }
}
</style>
