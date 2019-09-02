<template>
  <div class="checkImg">
    <el-input class="filter-input flex" placeholder="输入关键字进行过滤" v-model="filterText"></el-input>
      {{checkList}}
    <el-tree
      class="filter-tree flex"
      :data="batchList"
      :props="defaultProps"
      show-checkbox
      @check="getCheck"
      highlight-current
      :filter-node-method="filterNode"
      ref="tree"
    ></el-tree>
  </div>
</template>

<script>
import { getBatchInfo, getMedicalIdInfo, getimgnptypebymids } from '@/api/cervical'
export default {
  name: "checkImg",
  watch: {
    filterText(val) {
      this.$refs.tree.filter(val);
    }
  },
  data() {
    return {
      filterText: "",
      batchList: [],
      checkList: [],
      defaultProps: {
        children: "children",
        label: "label"
      }
    }
  },

  methods: {
    filterNode(value, data) {
      if (!value) return true;
      return data.label.indexOf(value) !== -1;
    },
    getBatchInfo() {
      getBatchInfo().then(res1 => {
        const data1 = res1.data.data
        data1.batchs.map(v => {
          let obj = {}
          obj['label'] = v
          getMedicalIdInfo({ 'batchid': v }).then(res2 => {
            const data2 = res2.data.data
            let medicalids = []
            data2.medicalids.map(item => {
              item = {
                'label': item
              }
              medicalids.push(item)
            })
            obj['children'] = medicalids
            this.batchList.push(obj)
          })
        })
      })
    },
    getCheck(checkedNodes,halfCheckedKeys) {
      console.log(checkedNodes, halfCheckedKeys)
      // console.log(this.$refs.tree.getCheckedNodes())
      this.checkList = this.$refs.tree.getCheckedNodes()
    }
  },

  mounted() {
    this.getBatchInfo()
  }
}
</script>

<style lang="scss" scoped>
.checkImg {
  .filter-tree {
    align-items: flex-start;
    .el-tree-node__children {
      display: flex;
    }
  }
  .filter-input {
    width: 500px;
    margin: 0 auto;
    margin-bottom: 30px;
  }
}
</style>
