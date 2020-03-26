<template>
  <div class="expandtwo">
    <div class="temp-box flex">
      <el-table
        ref="multipleTable"
        :data="predicts"
        tooltip-effect="dark"
        style="width: 75%"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column label="ID" prop="id" width="120" />
        <el-table-column label="预测结果" prop="predict_str" width="200" />
        <el-table-column label="初审核结果" prop="true_str" width="200" />
        <el-table-column label="预测得分" prop="predict_score" width="100" />
        <el-table-column label="细胞图" prop="cellpath" width="200">
          <template slot-scope="scope2">
            <img :src="hosturlpath64 + scope2.row.cellpath + '?width=100'" width="100" height="100">
          </template>
        </el-table-column>
      </el-table>
      <div class="select-box" style="width:25%;">
        <h3>分配给</h3>
        <el-select v-model="vid" placeholder="请选择" @change="memeberChange">
          <el-option
            v-for="item in userList"
            :key="item.id"
            :label="item.name"
            :value="item.id"
          >
            <img :src="item.image" style="float: left;width:25px;height:25px;">
            <span style="float: right; color: #8492a6; font-size: 13px">{{ item.name }}</span>
          </el-option>
        </el-select>
        <el-button type="primary" :disabled="isChange" @click="setPredictsReview(scope.row)">确定</el-button>
      </div>
    </div>

    <el-pagination
      v-if="total != 0"
      class="page"
      :current-page.sync="page"
      :page-sizes="[10, 20, 30, 50]"
      :page-size="pagesize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="total"
      @current-change="handleCurrentChange"
      @size-change="handleSizeChange"
    />
  </div>
</template>
<script>
import { APIUrl } from '@/const/config'
import { getUserLists } from '@/api/user'
import { getPredictsByPID2, setPredictsReview } from '@/api/cervical'
import { cellsType } from '@/const/const'

export default {
  name: 'App',
  props: {
    // predicts: {
    //   type: Array,
    //   default: () => {
    //     return []
    //   }
    // },
    pid: {
      type: Number,
      default: () => {
        return 0
      }
    },
    // page: {
    //   type: Number,
    //   default: () => {
    //     return 0
    //   }
    // },
    pagesize: {
      type: Number,
      default: () => {
        return 0
      }
    },
    total: {
      type: Number,
      default: () => {
        return 0
      }
    }
  },
  data() {
    return {
      hosturlpath64: APIUrl + '/imgs/',
      cpage: 1,
      cpagesize: 10,
      cpredicts: [],
      vid: '请选择分配对象',
      userList: [],
      isChange: true
    }
  },
  computed: {
    predicts: {
      // getter
      get: function() {
        return this.cpredicts
      },
      // setter
      set: function(newValue) {

      }
    },
    page: {
      // getter
      get: function() {
        return 0
      },
      // setter
      set: function(newValue) {

      }
    }
  },
  watch: {
    predicts: function(value, newValue) {
      console.log(value, newValue)
    }
  },
  mounted() {
    this.getPredictsByPID2(this.cpagesize, (this.cpage - 1) * this.cpagesize, this.pid)
  },
  created() {
    this.getUserLists(100, 0, 1)
  },
  methods: {
    memeberChange(val) {
      console.log(val)
      this.isChange = false
    },
    getPredictsByPID2(limit, skip, pid) {
      getPredictsByPID2({ 'limit': limit, 'skip': skip, 'pid': pid, 'status': 0, 'type': 50, 'order': 0 }).then(res => {
        res.data.data.predicts.map(item => {
          item.predict_str = cellsType[item.predict_type]
          item.true_str = cellsType[item.true_type]
        })
        this.cpredicts = res.data.data.predicts
        // console.log(this.cpredicts, 'cpredicts')
      })
    },
    handleCurrentChange(val) {
      this.cpage = val
      // console.log(this.cpage, this.cpagesize, this.pid)
      this.getPredictsByPID2(this.cpagesize, (this.cpage - 1) * this.cpagesize, this.pid)
    },
    handleSizeChange(val) {
      this.cpagesize = val
      // console.log(this.cpage, this.cpagesize, this.pid)
      this.getPredictsByPID2(this.cpagesize, (this.cpage - 1) * this.cpagesize, this.pid)
    },
    setPredictsReview(project) {
      console.log(project)
      this.loading = true
      const postData = {
        'pid': project.id,
        'predicts': this.selectedList,
        'vid': project.id
      }
      setPredictsReview(postData).then(res => {
        this.loading = false
        this.getPredictsByPID2(project.currentPageSize, (project.currentPage - 1) * project.currentPageSize, project.id)
      })
    },
    getUserLists(limit, skip, order) {
      getUserLists({ 'limit': limit, 'skip': skip, 'order': order }).then(res => {
        this.userList = res.data.data.users
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.expandtwo {
  overflow: auto;
  height: 100%;
  .temp-box {
    justify-content: flex-start;
    align-items: flex-start;
  }
  .tools {
    background: #fff;
    justify-content: space-around;
    bottom: 0px;
    position: fixed;
    left: 0;
    right: 0;
    margin-left: auto;
    margin-right: auto;
  }
  .table-expand {
    font-size: 0;
  }
  .table-expand label {
    width: 90px;
    color: #99a9bf;
  }
  .table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: calc(100% / 4);
  }
}
</style>
