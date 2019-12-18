<template>
  <div class="dashboard-editor-container">
    <panel-group />

    <div class="row-box flex">
      <medical-report style="width: 48%;" />
      <transaction-table style="width: 48%;" />
      <data-sets style="width: 48%; margin: 40px 0;" />
      <best-model style="width: 48%; margin: 40px 0;" />
    </div>
  </div>
</template>

<script>
import PanelGroup from './components/PanelGroup'
import TransactionTable from './components/TransactionTable'
import BestModel from './components/bestModel'
import DataSets from './components/DataSets'
import medicalReport from './components/medicalReport'

export default {
  name: 'DashboardAdmin',
  components: {
    PanelGroup,
    TransactionTable,
    BestModel,
    DataSets,
    medicalReport
  }
}
</script>

<style lang="scss" scoped>
.row-box {
  justify-content: space-around;
  flex-wrap: wrap;
  align-items: flex-start;
}
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
