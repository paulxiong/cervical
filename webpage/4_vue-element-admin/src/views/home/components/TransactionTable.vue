<template>
  <div class="VerificationcntData">
    <el-table :data="verificationcnt" max-height="300">
      <el-table-column width="100" :label="$t('dashboard.reviewID')" prop="id" />
      <el-table-column :label="$t('dashboard.reviewOwner')">
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
      <el-table-column width="200" :label="$t('dashboard.reviewUsername')" prop="name" />
      <el-table-column :label="$t('dashboard.review1')" prop="status1" />
      <el-table-column :label="$t('dashboard.review0')" prop="status0" />
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
      dialogFormVisible: false
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

