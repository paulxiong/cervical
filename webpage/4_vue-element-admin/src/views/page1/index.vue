<template>
  <div class="dashboard-container">
    <p>总图片数： {{ totalimg }}, 标注为Norm的图片数: {{ totalimgnorm }}</p>
    <p>总标注次数： {{ totallabel }}, 其中 阴性:{{ totallabelN }} , 阳性 {{ totallabelP }}</p>
    <p>标注分类数： {{ totalcategory }}</p>
    <table class="hovertable">
      <tr><th>ID</th><th>缩写</th><th>标注次数</th><th>标注图片数</th><th>描述</th><th>P/N</th></tr>
      <tr v-for="item in categorylists" :key="item.name">
        <td>{{ item.id }}</td>
        <td class="titleclass">{{ item.name }}</td>
        <td>{{ item.cnt }}</td>
        <td>{{ item.cntimg }}</td>
        <td>{{ item.other }}</td>
        <td v-if="item.p1n0 == 0">N</td>
        <td v-else>阳性</td>
      </tr>
    </table>
    <el-button type="primary" icon="upload" style="margin: 10px 0 20px 0;" @click="getHtml">
      刷新统计信息
    </el-button>
  </div>
</template>

<script>
import { getDatasetLists } from '@/api/cervical'
export default {
  name: 'Info',
  components: { },
  data() {
    return {
      totalimg: 0,
      totallabel: 0,
      totallabelN: 0,
      totallabelP: 0,
      totalcategory: 0,
      totalimgnorm: 0,
      categorylists: []
    }
  },
  computed: {
  },
  created() {
    this.getHtml()
  },
  methods: {
    getHtml() {
      getDatasetLists().then(response => {
        const { data } = response.data
        if (typeof (data) !== 'object') {
          return
        }
        this.totalimg = (data.totalimg) ? data.totalimg : 0
        this.totalimgnorm = (data.totalimgnorm) ? data.totalimgnorm : 0
        this.totallabel = (data.totallabel) ? data.totallabel : 0
        this.totallabelN = (data.totallabeln) ? data.totallabeln : 0
        this.totallabelP = (data.totallabelp) ? data.totallabelp : 0
        this.totalcategory = (data.totalcategory) ? data.totalcategory : 0
        this.categorylists = (data.categorylists) ? data.categorylists.concat([]) : []
      })
    }
  }
}
</script>

<style lang="scss" scoped>
  .dashboard-container {
    margin-left: 10px;
  }
  table.hovertable {
      font-family: verdana,arial,sans-serif;
      color:#333333;
      border-width: 1px;
      border-color: #c3dde0;
      border-collapse: collapse;
      text-align: left;
      width: 350px;
  }
  table.hovertable th {
      background-color:#c3dde0;
      padding: 8px;
      border: 1px solid #000000;
  }

  table.hovertable td {
      border-width: 1px;
      padding: 6px;
      border: 1px solid #000000;
      font-size: 12px;
      font-family: "Helvetica Neue", "Luxi Sans", "DejaVu Sans", Tahoma, "Hiragino Sans GB", STHeiti, "Microsoft YaHei";
  }
  table.hovertable td.titleclass {
      font-size: 12px;
      width: 24%;
      font-family: "Helvetica Neue", "Luxi Sans", "DejaVu Sans", Tahoma, "Hiragino Sans GB", STHeiti, "Microsoft YaHei";
      color: #999 !important;
  }
</style>

