<template>
  <div class="modelData">
    <el-table :data="modelLists" style="width: 100%;padding-top: 7px;">
      <el-table-column label="模型ID" min-width="50">
        <template slot-scope="scope">
          {{ scope.row.id }}
        </template>
      </el-table-column>
      <el-table-column label="描述" width="300" align="center">
        <template slot-scope="scope">
          {{ scope.row.desc }}
        </template>
      </el-table-column>
      <el-table-column label="类型" width="150" align="center">
        <template slot-scope="scope">
          {{ scope.row.modelType }}
        </template>
      </el-table-column>
      <el-table-column label="准确度" width="150" align="center">
        <template slot-scope="scope">
          {{ scope.row.precision }}
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getListmodel } from '@/api/cervical'
import { modelType } from '@/const/const'

export default {
  name: 'ModelData',
  components: {},
  data() {
    return {
      total: undefined,
      modelLists: [],
      dialogFormVisible: false,
      listQuery: {
        desc: undefined,
        type: undefined
      },
      typeOptions: [
        {
          key: '0',
          name: '全部'
        },
        {
          key: '1',
          name: '训练'
        },
        {
          key: '2',
          name: '预测'
        }
      ]
    }
  },
  created() {
    this.getListmodel(4, 0, 52)
  },
  methods: {
    getListmodel(limit, skip, type) {
      // 0未知 1UNET 2GAN 3SVM 4MASKRCNN 5AUTOKERAS 6MALA 50全部的裁剪模型(没做) 51全部的分类模型 52全部模型
      getListmodel({ 'limit': limit, 'skip': skip, 'type': type }).then(res => {
        res.data.data.models.map(v => {
          v.modelType = modelType[v.type]
        })
        this.modelLists = res.data.data.models
        this.total = res.data.data.total
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.bestModel {
    width: 100%;
    height: 341px;
    background: #fff;
    padding-top: 7px;
}
</style>
