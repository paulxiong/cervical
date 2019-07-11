<template>
  <div class="dashboard-container">
    <div class="box1-container">
      <el-collapse v-model="activeNames" @change="handleChange">
        <el-collapse-item title="详细信息" name="1">
          <div>
            <p>ID: {{ id }} / 目录名: {{ dir }}</p>
            <p>描述: {{ desc }}</p>
            <p>状态: {{ status }}</p>
            <p>输入数量N: {{ cntn }} / P: {{ cntp }} 输出细胞数量N: {{ cellcntn }} / P: {{ cellcntp }}</p>
            <p>批次: {{ batchids }}</p>
            <p>病例: {{ medicalids }}</p>
            <p>创建时间: {{ createdatts }} / 开始处理时间: {{ starttimets }}</p>
          </div>
        </el-collapse-item>
        <el-collapse-item title="(step0)  原始数据" name="2">
          <el-table :data="input_datasets_img" style="width: 100%">
            <el-table-column label="图片链接" width="900">
              <template slot-scope="scope">
                <el-popover trigger="hover" placement="top">
                  <p>图片链接: {{ scope.row }}</p>
                  <img id="hallstatt" src="http://9201.gpu.raidcdn.cn:9700/unsafe/645x0/20190523/1813330/Images/IMG001x014.JPG" class="annotatable">
                  <div slot="reference" class="name-wrapper">
                    <p size="medium">{{ scope.row }}</p>
                  </div>
                </el-popover>
              </template>
            </el-table-column>
            <el-table-column label="操作">
              <template slot-scope="scope">
                <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-collapse-item>
        <el-collapse-item title="(step1)  去噪后的数据" name="3">
          <el-table :data="tableData" style="width: 100%">
            <el-table-column label="图片链接" width="900">
              <template slot-scope="scope">
                <el-popover trigger="hover" placement="top">
                  <p>住址: {{ scope.row.address }}</p>
                  <img id="hallstatt" src="http://9201.gpu.raidcdn.cn:9700/unsafe/645x0/20190523/1813330/Images/IMG001x014.JPG" class="annotatable">
                  <div slot="reference" class="name-wrapper">
                    <el-tag size="medium">{{ scope.row.address }}</el-tag>
                  </div>
                </el-popover>
              </template>
            </el-table-column>
            <el-table-column label="操作">
              <template slot-scope="scope">
                <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-collapse-item>
        <el-collapse-item title="(step2)  mask图片" name="4">
          <el-table :data="tableData" style="width: 100%">
            <el-table-column label="图片链接" width="900">
              <template slot-scope="scope">
                <el-popover trigger="hover" placement="top">
                  <p>住址: {{ scope.row.address }}</p>
                  <img id="hallstatt" src="http://9201.gpu.raidcdn.cn:9700/unsafe/645x0/20190523/1813330/Images/IMG001x014.JPG" class="annotatable">
                  <div slot="reference" class="name-wrapper">
                    <el-tag size="medium">{{ scope.row.address }}</el-tag>
                  </div>
                </el-popover>
              </template>
            </el-table-column>
            <el-table-column label="操作">
              <template slot-scope="scope">
                <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-collapse-item>
        <el-collapse-item title="(step3)  输出数据" name="5">
          <el-table :data="tableData" style="width: 100%">
            <el-table-column label="图片链接" width="900">
              <template slot-scope="scope">
                <el-popover trigger="hover" placement="top">
                  <p>住址: {{ scope.row.address }}</p>
                  <img id="hallstatt" src="http://9201.gpu.raidcdn.cn:9700/unsafe/645x0/20190523/1813330/Images/IMG001x014.JPG" class="annotatable">
                  <div slot="reference" class="name-wrapper">
                    <el-tag size="medium">{{ scope.row.address }}</el-tag>
                  </div>
                </el-popover>
              </template>
            </el-table-column>
            <el-table-column label="操作">
              <template slot-scope="scope">
                <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-collapse-item>
      </el-collapse>
    </div>
  </div>
</template>

<script>
import { getjobresult } from '@/api/cervical'
import { dateformat2 } from '@/utils/dateformat'
export default {
  name: 'Info',
  components: { },
  data() {
    return {
      id: 0,
      desc: '',
      dir: '',
      status: 0,
      cntn: 0,
      cntp: 0,
      cellcntn: 0,
      cellcntp: 0,
      batchids: [],
      medicalids: [],
      createdatts: 0,
      starttimets: 0,
      input_datasets_img: [],
      input_datasets_denoising: [],
      middle_mask: [],
      output_datasets_npy: [],
      output_datasets_slide_npy: [],
      output_datasets_crop: [],
      activeNames: ['1'],
      tableData: [{
        date: '2016-05-02',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }, {
        date: '2016-05-04',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1517 弄'
      }, {
        date: '2016-05-01',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1519 弄'
      }, {
        date: '2016-05-03',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1516 弄'
      }]
    }
  },
  computed: {
  },
  created() {
    this.id = this.$route.query.id
    this.getjobresult(this.id)
  },
  methods: {
    handleChange(val) {
      console.log(val)
    },
    getjobresult(id) {
      getjobresult({ 'id': id }).then(response => {
        if (!response || !response.data || !response.data.data || typeof (response.data.data) !== 'object') {
          return
        }
        const { data } = response.data
        console.log(data)
        this.id = data.id
        this.desc = data.desc
        this.dir = data.dir
        this.status = data.status
        this.cntn = data.cntn
        this.cntp = data.cntp
        this.cellcntn = data.cellcntn
        this.cellcntp = data.cellcntp
        this.batchids = data.batchids
        this.medicalids = data.medicalids
        this.createdatts = dateformat2(data.createdatts)
        this.starttimets = dateformat2(data.starttimets)
        this.input_datasets_img = [].concat(data.input_datasets_img)
      })
    }
  }
}
</script>

<style lang="scss" scoped>
  .dashboard-container {
    margin: 10px 10px 10px 10px;
    max-width: 1024px;
  }
  .box1-container {
    padding: 12px;
    border: 1px solid #ebebeb;
    border-radius: 10px;
    transition: .2s;
    margin: 10px, 10px, 10px, 10px;
    width: 100%;
  }
</style>

