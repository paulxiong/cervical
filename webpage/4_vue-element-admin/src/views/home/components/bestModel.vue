<template>
  <div class="modelData">
    <el-table :data="modelLists">
      <el-table-column
        label="模型ID"
        prop="id"
        width="100"
      />
      <el-table-column
        label="描述"
        prop="desc"
      />
      <el-table-column
        label="类型"
        prop="modelType"
      />
      <el-table-column
        label="准确度"
        prop="precision"
      />
    </el-table>
  </div>
</template>

<script>
import { getListmodel } from '@/api/cervical'
import { taskStatus, taskType, modelType } from '@/const/const'
import { parseTime } from '@/utils/index'

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
    this.getListmodel(5, 0, 52)
  },
  methods: {
    getListmodel(limit, skip, type) {
      // 0未知 1UNET 2GAN 3SVM 4MASKRCNN 5AUTOKERAS 6MALA 50全部的裁剪模型(没做) 51全部的分类模型 52全部模型
      getListmodel({ 'limit': limit, 'skip': skip, 'type': type }).then(res => {
        res.data.data.models.map(v => {
          v.created_at = parseTime(v.created_at)
          v.statusType = taskType[v.status]
          v.status = taskStatus[v.status]
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
    background: #fff;
    padding-top: 7px;
}
</style>
