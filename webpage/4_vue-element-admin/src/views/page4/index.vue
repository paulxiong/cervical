<template>
  <div class="dashboard-container">
    <el-tabs type="border-card">
      <el-tab-pane label="已有数据集">
        <p>已经有了的数据集：</p>
        <div class="box1-container">
          <el-table :data="tableData" style="width: 100%">
            <el-table-column label="ID" width="80">
              <template slot-scope="scope">
                <span style="margin-left: 0px">{{ scope.row.id }}</span>
              </template>
            </el-table-column>
            <el-table-column label="描述" width="160">
              <template slot-scope="scope">
                <el-popover trigger="hover" placement="top">
                  <span>{{ scope.row.desc }}</span>
                  <div slot="reference" class="name-wrapper">
                    <span style="margin-left:0px;overflow:hidden;word-break:keep-all;">{{ scope.row.desc }}</span>
                  </div>
                </el-popover>
              </template>
            </el-table-column>
            <el-table-column label="状态" width="90">
              <template slot-scope="scope">
                <el-tag size="medium" :type="scope.row.status_type">{{ scope.row.status }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="开始处理日期" width="150">
              <template slot-scope="scope">
                <span style="margin-left: 0px">{{ scope.row.start_at }}</span>
              </template>
            </el-table-column>
            <el-table-column label="创建日期" width="150">
              <template slot-scope="scope">
                <span style="margin-left: 0px">{{ scope.row.created_at }}</span>
              </template>
            </el-table-column>
            <el-table-column label="操作">
              <template slot-scope="scope">
                <el-button size="mini" type="primary" @click="handleDetail(scope.$index, scope.row)">查看详细信息</el-button>
                <el-button size="mini" type="warning" @click="handleRedo(scope.$index, scope.row)">重新处理</el-button>
                <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-tab-pane>
      <el-tab-pane label="新建数据集">
        <p>1 请选择批次（不选择就默认不查找）：</p>
        <div class="box1-container">
          <el-checkbox-group v-model="batchs_checked" @change="batchChecked">
            <el-checkbox v-for="item in batchs" :key="item" :label="item" checked>{{ item }}</el-checkbox>
          </el-checkbox-group>
        </div>
        <p>2 请选择病历号：（不选择就默认不查找）</p>
        <div class="box1-container">
          <el-checkbox-group v-model="medicalids_checked">
            <el-checkbox v-for="item in medicalids" :key="item" :label="item">{{ item }}</el-checkbox>
          </el-checkbox-group>
        </div>
        <p>3 请选择使用的模型和参数:</p>
        <div class="box1-container">
          <p>描述</p>
          <el-input v-model="desc" placeholder="请输入内容" type="textarea" maxlength="30" show-word-limit />
          <p>选择模型</p>
          <el-select v-model="value" placeholder="请选择">
            <el-option v-for="item in modules" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </div>
        <p>4 请选择操作：</p>
        <div class="box1-container">
          <el-button type="primary" icon="upload" @click="createdataset2">生成并切割数据集</el-button>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { getBatchInfo, getMedicalIdInfo, getimgnptypebymids, createdataset, listdatasets, jobresult } from '@/api/cervical'
import { dateformat2 } from '@/utils/dateformat'
export default {
  name: 'Info',
  components: { },
  data() {
    return {
      countn: 0,
      countp: 0,
      countnp: 0,
      desc: '这是一个数据集',
      categorys: [],
      batchs: [],
      batchs_checked: [],
      medicalids: [],
      medicalids_checked: [],
      tableDataTotal: 0,
      tableData: [],
      value: '',
      modules: [{
        value: '1',
        label: 'UNET 好'
      }, {
        value: '2',
        label: 'UNET 一般'
      }, {
        value: '3',
        label: 'UNET 优秀'
      }, {
        value: '4',
        label: 'UNET 厉害'
      }, {
        value: '5',
        label: 'UNET 差'
      }]
    }
  },
  computed: {
  },
  created() {
    this.getBatchInfo()
    this.listdatasets(100, 0)
  },
  methods: {
    getBatchInfo() {
      getBatchInfo().then(response => {
        const { data } = response.data
        if (typeof (data) !== 'object') {
          return
        }
        this.batchs = (data.batchs) ? data.batchs.concat([]) : []
        console.log(this.batchs)
        if (!this.batchs || this.batchs.length < 1) {
          return
        }
        var arr = ''
        for (var i = 0; i < this.batchs.length; i++) {
          if (arr) {
            arr = arr + '|' + this.batchs[i]
          } else {
            arr = this.batchs[i]
          }
        }
        this.getMedicalIdInfo({ 'batchid': arr })
      })
    },
    getMedicalIdInfo(query) {
      var that = this
      getMedicalIdInfo(query).then(response => {
        const { data } = response.data
        if (typeof (data) !== 'object') {
          return
        }
        that.medicalids = (data.medicalids) ? data.medicalids.concat([]) : []
      })
    },
    getimgnptypebymids(postdata, cb) {
      var that = this
      getimgnptypebymids(postdata).then(response => {
        if (!response || !response.data || !response.data.data || typeof (response.data.data) !== 'object') {
          return cb && cb()
        }
        const { data } = response.data
        if (!data.countn || !data.countp) {
          that.countn = 0
          that.countp = 0
          that.countnp = 0
          return
        }
        that.countn = data.countn
        that.countp = data.countp
        that.countnp = that.countn + that.countp
        return cb && cb()
      })
    },
    createdataset(postdata) {
      createdataset(postdata).then(response => {
        if (!response || !response.data || !response.data.data || typeof (response.data.data) !== 'object') {
          return
        }
      })
    },
    jobresult(postdata) {
      jobresult(postdata).then(response => {
        if (!response || !response.data || !response.data.data || typeof (response.data.data) !== 'object') {
          return
        }
      })
    },
    listdatasets(limit, skip) {
      var that = this
      listdatasets({ 'limit': limit, 'skip': skip }).then(response => {
        if (!response || !response.data || !response.data.data || typeof (response.data.data) !== 'object') {
          return
        }
        const { data } = response.data
        that.tableDataTotal = data.total
        that.tableData = []
        for (var i = 0; i < data.datasets.length; i++) {
          data.datasets[i].created_at = dateformat2(data.datasets[i].created_at)
          data.datasets[i].start_at = dateformat2(data.datasets[i].start_at)
          const info = [
            {'id': 0, 'status': '初始化',         'type': 'info'},
            {'id': 1, 'status': '用户要求开始处理', 'type': 'info'},
            {'id': 2, 'status': '开始处理',        'type': 'info'},
            {'id': 3, 'status': '处理出错',        'type': 'danger'},
            {'id': 4, 'status': '处理完成',        'type': 'success'},
            {'id': 5, 'status': '目录不存在',      'type': 'danger'},
            {'id': 6, 'status': '开始训练',        'type': 'info'},
            {'id': 7, 'status': '训练出错',        'type': 'danger'},
            {'id': 8, 'status': '训练完成',        'type': 'success'}
          ]
          // #0初始化1用户要求开始处理2开始处理3处理出错4处理完成5目录不存在6开始训练7训练出错8训练完成
          var index = Number(data.datasets[i].status)
          if (index < info.length) {
            data.datasets[i].status = info[index].status
            data.datasets[i].status_type = info[index].type
          } else {
            data.datasets[i].status = '未知'
            data.datasets[i].status_type = 'warning'
          }
          that.tableData.push(data.datasets[i])
        }
      })
    },
    createdataset2() {
      var postdata = {
        medicalids: this.medicalids_checked,
        batchids: this.batchs_checked,
        desc: this.desc
      }
      var that = this
      this.getimgnptypebymids(postdata, function() {
        var tip = '准备生成和处理数据集【选中原图数量 N: ' + that.countn + ' / P: ' + that.countp + ' 】, 是否继续?'
        that.$confirm(tip, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          that.createdataset(postdata)
          that.$message({
            type: 'success',
            message: '开始创建和处理数据集!'
          })
        }).catch(() => {
          that.$message({
            type: 'info',
            message: '已取消创建'
          })
        })
      })
    },
    getImageNPCount() {
      var postdata = {
        medicalids: this.medicalids_checked,
        batchids: this.batchs_checked,
        desc: this.desc
      }
      console.log(this.medicalids_checked)
      this.getimgnptypebymids(postdata)
    },
    batchChecked(target) {
      var arr = ''
      for (var i = 0; i < target.length; i++) {
        if (arr) {
          arr = arr + '|' + target[i]
        } else {
          arr = target[i]
        }
      }
      this.getMedicalIdInfo({ 'batchid': arr })
    },
    handleRedo(index, row) {
      console.log(index, row.id)
      this.jobresult({ 'id': row.id, 'status': 1 })
    },
    handleDelete(index, row) {
      console.log(index, row)
    },
    handleDetail(index, row) {
      this.$router.push({ path: '/page4/details' || '/', query: { 'id': row.id }})
      console.log(index, row)
    }
  }
}
</script>

<style lang="scss" scoped>
  .dashboard-container {
    margin: 10px, 10px, 10px, 10px;
  }
  .categorys-container {
    display: flex;
    flex-wrap: wrap;
  }
  .categorys-span {
    text-align: right;
    width: 80px;
    margin-right: 4px;
    line-height: 28px;
  }
  .categorys-div {
    width: 200px;
    display: flex;
    margin: 2px 5px 2px 5px;
  }
  .box1-container {
    padding: 12px;
    border: 1px solid #ebebeb;
    border-radius: 10px;
    transition: .2s;
    margin: 10px, 10px, 10px, 10px;
    width: 100%;
  }
  .box1-container-result {
    width: 100% !important;
  }
</style>

