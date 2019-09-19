<template>
  <div class="checkImg">
    <section class="next-info flex">
      <h3 class="np">
        选择的批次和病例中
        <br />
        n/p : {{countNP.countn}}/{{countNP.countp}}
      </h3>
      <el-button type="primary" @click="nextStep" class="next-btn" :disabled="!checkList.length">
        下一步
        <i class="el-icon-arrow-right el-icon--right"></i>
      </el-button>
    </section>
    <el-input class="filter-input flex" placeholder="输入关键字进行过滤" v-model="filterText"></el-input>
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
      countNP: {
        countn: 0,
        countp: 0
      },
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
    nextStep() {
      this.$parent.stepNext()
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
    getCheck(checkedNodes, halfCheckedNodes) {
      let postBatchs = []
      let postMedicalIds = []
      this.checkList = this.$refs.tree.getCheckedNodes()
      halfCheckedNodes.checkedNodes.map(v => {
        if (v.children) {
          postBatchs.push(v.label)
        } else {
          postMedicalIds.push(v.label)
        }
      })
      halfCheckedNodes.halfCheckedNodes.map(v => {
        postBatchs.push(v.label)
      })
      // 去重
      postBatchs = Array.from(new Set(postBatchs))
      postMedicalIds = Array.from(new Set(postMedicalIds))
      console.log(postBatchs, postMedicalIds)
      this.getimgnptypebymids(postBatchs, postMedicalIds)
    },
    getimgnptypebymids(postBatchs, postMedicalIds) {
      let postData = {
        'batchids': postBatchs,
        'medicalids': postMedicalIds,
        'type': 1
      }
      localStorage.setItem('POST_DATA', JSON.stringify(postData))
      getimgnptypebymids(postData).then(res => {
        this.countNP = res.data.data
        localStorage.setItem('countNP', JSON.stringify(this.countNP))
      })
    }
  },

  mounted() {
    this.getBatchInfo()
  }
}
</script>

<style lang="scss" scoped>
.checkImg {
  .next-btn {
    width: 150px;
    font-weight: bold;
    margin-left: 20px;
  }
  .np {
    text-align: center;
  }
  .filter-tree {
    align-items: flex-start;
    .el-tree-node__children {
      display: flex;
    }
  }
  .filter-input {
    width: 30%;
    margin: 0 auto;
    margin-bottom: 10px;
  }
}
</style>
