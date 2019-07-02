<template>
  <div class="dashboard-container">
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
    <p>3 请选择类型和数量：（不选择就默认不查找）</p>
    <div class="box1-container categorys-container">
      <div v-for="category in categorys" :key="category.id" class="categorys-div">
        <span class="categorys-span">{{ category.id }}_{{ category.name }}</span>
        <el-input-number v-model="category.num" :min="0" :max="100000" size="mini">1</el-input-number>
      </div>
      <div class="categorys-div">
        <el-button type="primary" icon="upload" @click="resetCategorysNumber">全部清零</el-button>
      </div>
    </div>
    <p>4 符合上面您选择条件的图片拷贝到哪个目录（默认根目录/）：</p>
    <div class="box1-container">
      <el-input v-model="outpath" placeholder="默认路径是 /">1</el-input>
    </div>
    <p>5 请选择操作：</p>
    <div class="box1-container">
      <el-button type="primary" icon="upload" @click="getBatchInfo">刷新统计信息</el-button>
      <el-button type="primary" icon="upload" @click="getImageList">生成图片列表</el-button>
    </div>
    <p>6 结果输出：</p>
    <div class="box1-container box1-container-result">
      <el-input v-model="textarea" type="textarea" :rows="2" placeholder="请输入内容" autosize readonly>1</el-input>
    </div>
  </div>
</template>

<script>
import { getBatchInfo, getMedicalIdInfo, getCategoryInfo, getImgListOfWanted } from '@/api/cervical'
export default {
  name: 'Info',
  components: { },
  data() {
    return {
      outpath: '/',
      textarea: '',
      categorys: [],
      batchs: [],
      batchs_checked: [],
      medicalids: [],
      medicalids_checked: [],
      wantedimages: [],
      tiTypeList: [{ type_id: 1, description: 'Norm', num: 1 }],
      checkList: ['选中且禁用', '复选框 A'],
      checkTiType: []
    }
  },
  computed: {
  },
  created() {
    this.getBatchInfo()
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
      getMedicalIdInfo(query).then(response => {
        const { data } = response.data
        if (typeof (data) !== 'object') {
          return
        }
        this.medicalids = (data.medicalids) ? data.medicalids.concat([]) : []
        this.getCategoryInfo()
      })
    },
    getCategoryInfo() {
      getCategoryInfo().then(response => {
        const { data } = response.data
        if (typeof (data) !== 'object') {
          return
        }
        this.categorys = (data.categorys) ? data.categorys.concat([]) : []
      })
    },
    getImgListOfWanted(postdata) {
      getImgListOfWanted(postdata).then(response => {
        if (!response || !response.data || !response.data.data || typeof (response.data.data) !== 'object') {
          return
        }
        const { data } = response.data

        if (!data.images || data.images.length < 1) {
          return
        }
        this.wantedimages = (data.images) ? data.images.concat([]) : []
        console.log(data)
        this.textarea = '#!/bin/bash\n'
        for (var i = 0; i < this.wantedimages.length; i++) {
          var filename = this.wantedimages[i].replace(/\//g, '_')
          this.textarea = this.textarea + 'cp -f ' + this.wantedimages[i] + '\t' + this.outpath + filename + '\n'
        }
      })
    },
    resetCategorysNumber() {
      for (var i = 0; i < this.categorys.length; i++) {
        this.categorys[i].num = 0
      }
    },
    getImageList() {
      var categorys_checked = []
      for (var i = 0; i < this.categorys.length; i++) {
        if (this.categorys[i].num > 0) {
          categorys_checked.push({ 'id': this.categorys[i].id, 'num': this.categorys[i].num })
        }
      }
      var postdata = {
        categorys: categorys_checked,
        batchs: this.batchs_checked,
        medicalids: this.medicalids_checked
      }
      console.log(postdata)
      this.getImgListOfWanted(postdata)
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
      console.log(arr)
      this.getMedicalIdInfo({ 'batchid': arr })
    }
  }
}
</script>

<style lang="scss" scoped>
  .dashboard-container {
    margin-left: 10px;
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
    margin-left: 10px;
    width: 950px;
  }
  .box1-container-result {
    width: 100% !important;
  }
</style>

