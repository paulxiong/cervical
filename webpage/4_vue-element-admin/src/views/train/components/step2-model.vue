<template>
  <div class="checkModel flex">
    <section class="model-info">
      <h4>模型选择</h4>
      <el-select class="model-option" v-model="value" clearable placeholder="请选择">
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        ></el-option>
      </el-select>      
    </section>

    <section class="param">
      <h4>裁剪大小(单位px)</h4>
      <el-input class="input" v-model="cutInput" placeholder="请输入裁剪大小"></el-input>
    </section>
  </div>
</template> 

<script>
export default {
  name: "checkModel",
  components: {},
  data() {
    return {
      cutInput: 100,
      options: [
        {
          value: "选项1",
          label: "Cell0822019_v2019081220904"
        },
        {
          value: "选项2",
          label: "Aell0822019_v201242304"
        },
        {
          value: "选项3",
          label: "Bell0822019_v20193242342340904"
        },
        {
          value: "选项4",
          label: "Dell0822019_v2012342320904"
        },
        {
          value: "选项5",
          label: "Tell0822019_v2ad213081220904"
        }
      ],
      value: ""
    }
  },
  methods: {}
}
</script>

<style lang="scss" scoped>
.checkModel {
  justify-content: flex-start;
  .model-info {
    margin-right: 30px;
  }
  .input {
    width: 200px;
  }
}
</style>
