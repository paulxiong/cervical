<template>
  <div class="checkImg">
    <el-input class="filter-input flex" placeholder="输入关键字进行过滤" v-model="filterText"></el-input>

    <el-tree
      class="filter-tree flex"
      :data="data"
      :props="defaultProps"
      show-checkbox
      highlight-current
      default-expand-all
      :filter-node-method="filterNode"
      ref="tree"
    ></el-tree>
  </div>
</template>

<script>
export default {
  name: "checkImg",
  watch: {
    filterText(val) {
      this.$refs.tree.filter(val);
    }
  },

  methods: {
    filterNode(value, data) {
      if (!value) return true;
      return data.label.indexOf(value) !== -1;
    }
  },

  data() {
    return {
      filterText: "",
      data: [{
        id: 1,
        label: "一级 1",
        children: [{
          id: 4,
          label: "二级 1-1",
        }, {
          id: 4,
          label: "二级 1-2",
        }]
      }, {
        id: 2,
        label: "一级 2",
        children: [{
          id: 5,
          label: "二级 2-1"
        }, {
          id: 6,
          label: "二级 2-2"
        }]
      }, {
        id: 3,
        label: "一级 3",
        children: [{
          id: 7,
          label: "二级 3-1"
        }, {
          id: 8,
          label: "二级 3-2"
        }]
      }],
      defaultProps: {
        children: "children",
        label: "label"
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.checkImg {
  .filter-input {
    width: 500px;
    margin: 0 auto;
    margin-bottom: 30px;
  }
}
</style>
