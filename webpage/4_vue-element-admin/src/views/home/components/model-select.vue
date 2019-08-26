<template>
  <div class="model">
    <section class="model-select">
      <p>Model</p>
      <el-select class="model-option" v-model="value" clearable placeholder="请选择">
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        ></el-option>
      </el-select>
    </section>
  </div>
</template>

<script>
export default {
  name: "model-select",
  components: {},
  data() {
    return {
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
    };
  },
  methods: {}
};
</script>

<style lang="scss" scoped>
.model {
  .model-select {
    .model-option {
      width: 300px;
    }
  }
}
</style>  