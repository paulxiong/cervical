<template>
  <div class="predict">
    <section class="header flex">
      <el-badge is-dot class="badge">预测进度</el-badge>
      <el-progress
        :text-inside="true"
        :stroke-width="26"
        :percentage="percentage"
        class="progress"
        status="success"
      ></el-progress>
      <el-button type="danger" class="predict-btn" @click="createPredict">开始预测</el-button>
    </section>
    <section class="content" v-if="!startPredict">
      <section class="model-info" v-if="modelList.length">
        <el-badge is-dot class="badge">模型信息</el-badge>
        <modelCard
          :modelInfo="modelInfo"
          :predict="predict"
          :modelList="modelList"
          @changeCellTypes="changeCellTypes"
        />
      </section>
      <section class="datasets-info" v-if="datasetsList.length">
        <el-badge is-dot class="badge">数据信息</el-badge>
        <datasetsCard :datasetsInfo="datasetsInfo" :predict="predict" :datasetsList="datasetsList" />
      </section>
    </section>
    <section class="results flex" v-else>
      <div class="img-item" v-for="(item,idx) in predictResult" :key="idx">
        <el-tooltip class="item" effect="dark" :content="`实际${item.type}:预测${item.predict}`" placement="bottom">
          <el-image
            :class="item.type===item.predict?'img-right':'img-wrong'"
            :src="item.url"
            lazy
          >
            <div slot="error" class="image-slot">
              <i class="el-icon-picture-outline"></i>
            </div>
          </el-image>
        </el-tooltip>
      </div>
    </section>
  </div>
</template>

<script>
import modelCard from './components/model-card'
import datasetsCard from './components/datasets-card'
import { ImgServerUrl } from '@/const/config'
import { listdatasets, getListmodel, createPredict } from '@/api/cervical'

export default {
  name: 'Predict',
  components: { modelCard, datasetsCard },
  data() {
    return {
      percentage: 0,
      predict: 'predict',
      startPredict: false,
      modelList: [],
      modelInfo: {},
      datasetsInfo: {},
      datasetsList: [],
      postCelltypes: [],
      hosturlpath200: ImgServerUrl + '/unsafe/200x0/scratch/',
      predictResult: [
        {
          url: 'http://dev.medical.raidcdn.cn:3001/unsafe/200x0/scratch/CHwwYmVD/cells/crop/redhouse.1816740.P.IMG011x029.JPG_p_7_1529_817_1629_917.png',
          type: 1,
          predict: 7
        },
        {
          url: 'http://dev.medical.raidcdn.cn:3001/unsafe/200x0/scratch/CHwwYmVD/cells/crop/redhouse.1816740.N.IMG023x017.JPG_n_1_1394_589_1494_689.png',
          type: 1,
          predict: 1
        },
        {
          url: 'http://dev.medical.raidcdn.cn:3001/unsafe/200x0/scratch/CHwwYmVD/cells/crop/redhouse.1816740.P.IMG011x029.JPG_p_7_1529_817_1629_917.png',
          type: 1,
          predict: 7
        },
        {
          url: 'http://dev.medical.raidcdn.cn:3001/unsafe/200x0/scratch/CHwwYmVD/cells/crop/redhouse.1816740.N.IMG023x017.JPG_n_1_1394_589_1494_689.png',
          type: 1,
          predict: 1
        },
        {
          url: 'http://dev.medical.raidcdn.cn:3001/unsafe/200x0/scratch/CHwwYmVD/cells/crop/redhouse.1816740.P.IMG011x029.JPG_p_7_1529_817_1629_917.png',
          type: 1,
          predict: 7
        },
        {
          url: 'http://dev.medical.raidcdn.cn:3001/unsafe/200x0/scratch/CHwwYmVD/cells/crop/redhouse.1816740.N.IMG023x017.JPG_n_1_1394_589_1494_689.png',
          type: 1,
          predict: 1
        },
        {
          url: 'http://dev.medical.raidcdn.cn:3001/unsafe/200x0/scratch/CHwwYmVD/cells/crop/redhouse.1816740.P.IMG011x029.JPG_p_7_1529_817_1629_917.png',
          type: 1,
          predict: 7
        },
        {
          url: 'http://dev.medical.raidcdn.cn:3001/unsafe/200x0/scratch/CHwwYmVD/cells/crop/redhouse.1816740.N.IMG023x017.JPG_n_1_1394_589_1494_689.png',
          type: 1,
          predict: 1
        },
        {
          url: 'http://dev.medical.raidcdn.cn:3001/unsafe/200x0/scratch/CHwwYmVD/cells/crop/redhouse.1816740.P.IMG011x029.JPG_p_7_1529_817_1629_917.png',
          type: 1,
          predict: 7
        },
        {
          url: 'http://dev.medical.raidcdn.cn:3001/unsafe/200x0/scratch/CHwwYmVD/cells/crop/redhouse.1816740.N.IMG023x017.JPG_n_1_1394_589_1494_689.png',
          type: 1,
          predict: 1
        }
      ]
    }
  },
  methods: {
    getListmodel(limit, skip) {
      getListmodel({ 'limit': limit, 'skip': skip }).then(res => {
        if (res.data.data.total > 0) {
          this.modelList = res.data.data.models
          this.modelInfo = this.modelList[0]
        }
      })
    },
    getListdatasets(limit, skip, type) {
      listdatasets({ 'limit': limit, 'skip': skip, 'type': type }).then(res => {
        this.datasetsList = res.data.data.datasets
        this.datasetsInfo = this.datasetsList[0]
      })
    },
    createPredict() {
      createPredict({ 'did': this.datasetsInfo.id, 'mid': this.modelInfo.id, 'celltypes': this.postCelltypes }).then(res => {
        this.$message({
          message: res.data.data,
          type: 'success'
        })
        this.startPredict = true
        this.percentage = 100
      })
    },
    changeCellTypes(val) {
      this.postCelltypes = val
    }
  },
  mounted() {
    this.getListmodel(10, 0)
    this.getListdatasets(100, 0, 2)
  }
}
</script>

<style lang="scss" scoped>
.predict {
  margin-bottom: 100px;
  .badge {
    font-weight: bold;
  }
  .content {
    padding: 0 30px;
    .badge {
      margin-bottom: 5px;
    }
  }
  .header {
    border: 1px solid #ccc;
    background: #304155;
    min-width: 100%;
    justify-content: flex-end;
    position: fixed;
    bottom: -1px;
    right: -1px;
    padding: 10px 0;
    z-index: 999;
    .badge {
      color: #fff;
    }
    .progress {
      width: 70%;
      margin: 0 10px;
    }
    .predict-btn {
      width: 100px;
      margin-right: 30px;
    }
  }
  .model-option {
    display: block;
  }
  .results {
    justify-content: flex-start;
    flex-wrap: wrap;
    padding: 30px;
    .img-item {
      flex-direction: column;
      margin-right: 30px;
      margin-bottom: 30px;
      .img-right {
        border: 5px solid #27cc6a;
        border-radius: 5px;
      }
      .img-wrong {
        border: 5px solid #fd6e70;
        border-radius: 5px;
      }
    }
  }
  .model-select,
  .datasets-select,
  .progress-info,
  .model-info,
  .datasets-info {
    margin: 20px 0;
  }
}
</style>
