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
          <p>N={{ countn }} / P={{ countp }} 总计 {{ countnp }} 张FOV图片</p>
          <el-button type="primary" icon="upload" @click="getImageNPCount">统计选中病例图片的数量</el-button>
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
    getimgnptypebymids(postdata) {
      var that = this
      getimgnptypebymids(postdata).then(response => {
        if (!response || !response.data || !response.data.data || typeof (response.data.data) !== 'object') {
          return
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
          // 0初始化1用户要求开始处理2开始处理3处理出错4处理完成5目录不存在
          if (Number(data.datasets[i].status === 0)) {
            data.datasets[i].status = '初始化'
            data.datasets[i].status_type = 'info'
          } else if (Number(data.datasets[i].status === 1)) {
            data.datasets[i].status = '等待处理'
            data.datasets[i].status_type = 'info'
          } else if (Number(data.datasets[i].status === 2)) {
            data.datasets[i].status = '开始处理'
            data.datasets[i].status_type = ''
          } else if (Number(data.datasets[i].status === 3)) {
            data.datasets[i].status = '处理出错'
            data.datasets[i].status_type = 'danger'
          } else if (Number(data.datasets[i].status === 4)) {
            data.datasets[i].status = '处理完成'
            data.datasets[i].status_type = 'success'
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
        desc: this.desc
      }
      this.createdataset(postdata)
    },
    getImageNPCount() {
      var postdata = {
        medicalids: this.medicalids_checked,
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

