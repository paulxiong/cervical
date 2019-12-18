<template>
  <div class="VerificationcntData">
    <el-table :data="verificationcnt" max-height="300">
      <el-table-column width="100" label="审核ID" prop="id" />
      <el-table-column label="创建者">
        <template slot-scope="scope">
          <el-tooltip v-if="scope.row.name" :content="scope.row.name" placement="right">
            <el-image
              style="width:35px;height:35px;border-radius:7px;"
              :src="scope.row.image"
              lazy
            >
              <div slot="error" class="image-slot">
                <i class="el-icon-picture-outline" />
              </div>
            </el-image>
          </el-tooltip>
          <el-image
            v-else
            style="width:35px;height:35px;border-radius:7px;"
            :src="scope.row.image"
            lazy
          >
            <div slot="error" class="image-slot">
              <i class="el-icon-picture-outline" />
            </div>
          </el-image>
        </template>
      </el-table-column>
      <el-table-column width="200" label="用户名" prop="name" />
      <el-table-column label="已审核" prop="status0" />
      <el-table-column label="未审核" prop="status1" />
    </el-table>
  </div>
</template>

<script>
import { getVerificationcnt } from '@/api/cervical'

export default {
  name: 'VerificationcntData',
  components: {},
  data() {
    return {
      verificationcnt: [],
      total: undefined,
      dialogFormVisible: false,
      typeOptions: [
        {
          key: '0',
          name: '未知'
        },
        {
          key: '1',
          name: '保留'
        },
        {
          key: '2',
          name: '训练'
        },
        {
          key: '3',
          name: '预测'
        }
      ]
    }
  },
  created() {
    this.getVerificationcnt()
  },
  methods: {
    getVerificationcnt() {
      // this.loading = true
      getVerificationcnt({}).then(res => {
        res.data.data.user.map(v => {
        })
        this.verificationcnt = res.data.data.user
        this.total = res.data.data.total
        // this.loading = false
      })
    }
  }
}
</script>

