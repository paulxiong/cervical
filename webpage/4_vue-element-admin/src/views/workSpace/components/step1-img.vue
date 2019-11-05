<template>
  <div class="checkImg">
    <section class="next-info flex">
      <h3 class="np">
        选择的批次和病例中
        <hr>
        n/p : {{ countNP.countn }}/{{ countNP.countp }}
      </h3>
    </section>
    <el-cascader
      placeholder="试试搜索: redhouse"
      style="width: 100%;"
      :options="batchList"
      :props="{ multiple: true }"
      clearable
      filterable
      @change="getimgnptypebymids"
    />
  </div>
</template>

<script>
import { getBatchInfo, getMedicalIdInfo, getimgnptypebymids } from '@/api/cervical'
export default {
  name: 'CheckImg',
  data() {
    return {
      filterText: '',
      batchList: [],
      countNP: {
        countn: 0,
        countp: 0
      },
      defaultProps: {
        children: 'children',
        label: 'label'
      },
      postBatchs: [],
      postMedicalIds: []
    }
  },
  watch: {
    filterText(val) {
      this.$refs.tree.filter(val)
    }
  },
  created() {
    this.getBatchInfo()
  },
  methods: {
    filterNode(value, data) {
      if (!value) return true
      return data.label.indexOf(value) !== -1
    },
    nextStep() {
      this.$parent.stepNext()
    },
    getBatchInfo() {
      getBatchInfo().then(res1 => {
        const data1 = res1.data.data
        data1.batchs.map(v => {
          const obj = {}
          obj['label'] = v
          obj['value'] = v
          getMedicalIdInfo({ 'batchid': v }).then(res2 => {
            const data2 = res2.data.data
            const medicalids = []
            data2.medicalids.map(item => {
              item = {
                'label': item,
                'value': item
              }
              medicalids.push(item)
            })
            obj['children'] = medicalids
            this.batchList.push(obj)
          })
        })
      })
    },
    getimgnptypebymids(val) {
      this.$emit('checkImg', true)
      const postData = {
        'batchids': [],
        'medicalids': []
      }
      val.map(v => {
        postData.batchids.push(v[0])
        postData.medicalids.push(v[1])
      })
      localStorage.setItem('POST_DATA', JSON.stringify(postData))
      getimgnptypebymids(postData).then(res => {
        this.countNP = res.data.data
        localStorage.setItem('countNP', JSON.stringify(this.countNP))
      })
    }
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
    font-size: 14px;
    color: #F56C6C;
  }
  .filter-tree {
    align-items: flex-start;
    .el-tree-node__children {
      display: flex;
    }
  }
  .type-raido {
    margin-left: 20px;
  }
  .filter-input {
    width: 30%;
    margin: 0 auto;
    margin-bottom: 10px;
  }
}
</style>
