<template>
  <div class="expandtwo">
    <div class="temp-box flex">
      <el-table
        ref="multipleTable"
        :data="cpredicts"
        tooltip-effect="dark"
        style="width: 75%"
        @selection-change="handleSelectionChange"
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
        <h3>细胞阴/阳性</h3>
        <el-select v-model="typeid" placeholder="请选择" @change="typeChange">
          <el-option
            v-for="item in typelist"
            :key="item.id"
            :label="item.name"
            :value="item.id"
          >
            <span style="float: right; color: #8492a6; font-size: 13px">{{ item.name }}</span>
          </el-option>
        </el-select>
        <el-button type="primary" @click="getCellList">刷新细胞图列表</el-button>
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
        <el-button type="primary" :disabled="isChange" @click="setPredictsReview">确定</el-button>
      </div>
    </div>

    <el-pagination
      class="page"
      :current-page.sync="cpage"
      :page-sizes="[10, 20, 30, 50]"
      :page-size="cpagesize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="ctotal"
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
    pid: {
      type: Number,
      default: () => {
        return 0
      }
    },
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
      ctotal: 0,
      cpredicts: [],
      selectedList: [],
      vid: '请选择分配对象',
      userList: [],
      isChange: true,
      cellorder: 0,
      celltype: 50,
      typeid: 0,
      typelist: [
        { 'id': 0, 'name': '阴性-得分从低到高', 'type': 50, 'order': 0 },
        { 'id': 1, 'name': '阴性-得分从高到低', 'type': 50, 'order': 1 },
        { 'id': 2, 'name': '阳性-得分从低到高', 'type': 51, 'order': 0 },
        { 'id': 3, 'name': '阳性-得分从高到低', 'type': 51, 'order': 1 }
      ]
    }
  },
  mounted() {
    this.ctotal = this.total
    this.getPredictsByPID2(this.cpagesize, (this.cpage - 1) * this.cpagesize, this.pid)
  },
  created() {
    this.getUserLists(100, 0, 1)
  },
  methods: {
    memeberChange(val) {
      this.isChange = false
    },
    typeChange(val) {
      this.typelist.map(item => {
        if (item.id === val) {
          this.cellorder = item.order
          this.celltype = item.type
        }
      })
    },
    getPredictsByPID2(limit, skip, pid) {
      getPredictsByPID2({ 'limit': limit, 'skip': skip, 'pid': pid, 'status': 0, 'type': this.celltype, 'order': this.cellorder }).then(res => {
        res.data.data.predicts.map(item => {
          item.predict_str = cellsType[item.predict_type]
          item.true_str = cellsType[item.true_type]
        })
        this.cpredicts = res.data.data.predicts
        this.ctotal = res.data.data.total
      })
    },
    handleCurrentChange(val) {
      this.cpage = val
      this.getPredictsByPID2(this.cpagesize, (this.cpage - 1) * this.cpagesize, this.pid)
    },
    handleSizeChange(val) {
      this.cpagesize = val
      this.getPredictsByPID2(this.cpagesize, (this.cpage - 1) * this.cpagesize, this.pid)
    },
    handleSelectionChange(val) {
      this.selectedList = []
      val.map(v => {
        this.selectedList.push(v.id)
      })
    },
    getCellList() {
      this.getPredictsByPID2(this.cpagesize, (this.cpage - 1) * this.cpagesize, this.pid)
    },
    setPredictsReview(project) {
      this.loading = true
      const postData = {
        'pid': this.pid,
        'predicts': this.selectedList,
        'vid': this.vid
      }
      setPredictsReview(postData).then(res => {
        this.loading = false
        this.getPredictsByPID2(this.cpagesize, (this.cpage - 1) * this.cpagesize, this.pid)
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
