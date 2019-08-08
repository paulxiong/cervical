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
          <div class="popover-container">
            <div v-for="url in input_datasets_img" :key="url.path">
              <el-popover trigger="hover" placement="top">
                <p>图片链接: {{ url.path }}</p>
                <el-image :src="url.big" class="img-step0" />
                <div slot="reference" class="name-wrapper">
                  <el-image :src="url.small" class="img-step0" />
                </div>
              </el-popover>
            </div>
          </div>
        </el-collapse-item>
        <el-collapse-item title="(step1)  去噪后的数据" name="3">
          <div class="popover-container">
            <div v-for="url in input_datasets_denoising" :key="url.path">
              <el-popover trigger="hover" placement="top">
                <p>图片链接: {{ url.path }}</p>
                <el-image :src="url.big" class="img-step0" />
                <div slot="reference" class="name-wrapper">
                  <el-image :src="url.small" class="img-step0" />
                </div>
              </el-popover>
            </div>
          </div>
        </el-collapse-item>
        <el-collapse-item title="(step2)  mask图片" name="4">
          <div class="popover-container">
            <div v-for="url in middle_mask" :key="url.path">
              <el-popover trigger="hover" placement="top">
                <p>图片链接: {{ url.path }}</p>
                <el-image :src="url.big" class="img-step0" />
                <div slot="reference" class="name-wrapper">
                  <el-image :src="url.small" class="img-step0" />
                </div>
              </el-popover>
            </div>
          </div>
        </el-collapse-item>
        <el-collapse-item title="(step3)  输出数据 crop_preview" name="5">
          <div class="popover-container">
            <div v-for="url in output_datasets_crop_preview" :key="url.path">
              <el-popover trigger="hover" placement="top">
                <p>图片链接: {{ url.path }}</p>
                <el-image :src="url.big" class="img-step0" />
                <div slot="reference" class="name-wrapper">
                  <el-image :src="url.small" class="img-step0" />
                </div>
              </el-popover>
            </div>
          </div>
        </el-collapse-item>
        <el-collapse-item title="(step3)  输出数据 crop N" name="6">
          <div class="popover-container">
            <div v-for="url in output_datasets_crop_n" :key="url.path">
              <el-popover trigger="hover" placement="top">
                <p>图片链接: {{ url.path }}</p>
                <el-image :src="url.big" class="img-step0" />
                <div slot="reference" class="name-wrapper">
                  <el-image :src="url.small" class="img-step0" />
                </div>
              </el-popover>
            </div>
          </div>
        </el-collapse-item>
        <el-collapse-item title="(step3)  输出数据 crop P" name="7">
          <div class="popover-container">
            <div v-for="url in output_datasets_crop_p" :key="url.path">
              <el-popover trigger="hover" placement="top">
                <p>图片链接: {{ url.path }}</p>
                <el-image :src="url.big" class="img-step0" />
                <div slot="reference" class="name-wrapper">
                  <el-image :src="url.small" class="img-step0" />
                </div>
              </el-popover>
            </div>
          </div>
        </el-collapse-item>
        <el-collapse-item title="裁剪log" name="8">
          <el-input v-model="croplog" type="textarea" :rows="2" placeholder="后台log" autosize readonly>1</el-input>
        </el-collapse-item>
        <el-collapse-item title="训练log" name="9">
          <el-input v-model="trainlog" type="textarea" :rows="2" placeholder="训练log" autosize readonly>1</el-input>
        </el-collapse-item>
      </el-collapse>
    </div>
  </div>
</template>

<script>
import { getjobresult, getjoblog } from '@/api/cervical'
import { dateformat2 } from '@/utils/dateformat'
import { ImgServerUrl } from '@/const/config'
export default {
  name: 'Info',
  components: { },
  data() {
    return {
      hosturlpath: ImgServerUrl + '/unsafe/',
      hosturlpath200: '',
      hosturlpath645: '',
      hosturlpath16: '',
      hosturlpath64: '',
      croplog: '',
      trainlog: '',
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
      output_datasets_crop_n: [],
      output_datasets_crop_p: [],
      output_datasets_crop_preview: [],
      activeNames: ['1']
    }
  },
  computed: {
  },
  created() {
    this.id = this.$route.query.id
    this.hosturlpath200 = this.hosturlpath + '200x0/scratch/'
    this.hosturlpath16 = this.hosturlpath + '32x0/scratch/'
    this.hosturlpath645 = this.hosturlpath + '800x0/scratch/'
    this.hosturlpath64 = this.hosturlpath + '64x0/scratch/'
    this.getjobresult(this.id)
    this.getjoblog(this.id)
  },
  methods: {
    handleChange(val) {
      // 清空所有关闭的面板的数据，不然一个页面同时加载上千张图片导致浏览器卡死
      if (val.indexOf('2') > -1 && this.input_datasets_img.length === 0) {
        this.input_datasets_img = this._input_datasets_img
      }
      if (val.indexOf('3') > -1 && this.input_datasets_denoising.length === 0) {
        this.input_datasets_denoising = this._input_datasets_denoising
      }
      if (val.indexOf('4') > -1 && this.middle_mask.length === 0) {
        this.middle_mask = this._middle_mask
      }
      if (val.indexOf('5') > -1 && this.output_datasets_crop_preview.length === 0) {
        this.output_datasets_crop_preview = this._output_datasets_crop_preview
      }
      if (val.indexOf('6') > -1 && this.output_datasets_crop_n.length === 0) {
        this.output_datasets_crop_n = this._output_datasets_crop_n
      }
      if (val.indexOf('7') > -1 && this.output_datasets_crop_p.length === 0) {
        this.output_datasets_crop_p = this._output_datasets_crop_p
      }
    },
    getimgurl(smallurl, bigurl, patharr) {
      var out = []
      for (var i = 0; i < patharr.length; i++) {
        var item = patharr[i]
        var url = smallurl + this.dir + '/' + item
        var url2 = bigurl + this.dir + '/' + item
        out.push({ 'small': url, 'big': url2, 'path': item })
      }
      return out
    },
    getjoblog(id) {
      getjoblog({ 'id': id, 'type': 'c' }).then(response => {
        if (!response || !response.data || !response.data.data || typeof (response.data.data) !== 'string') {
          return
        }
        const { data } = response.data
        this.croplog = data
      })
      getjoblog({ 'id': id, 'type': 't' }).then(response => {
        if (!response || !response.data || !response.data.data || typeof (response.data.data) !== 'string') {
          return
        }
        const { data } = response.data
        this.trainlog = data
      })
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
        this._input_datasets_img = this.getimgurl(this.hosturlpath200, this.hosturlpath645, data.input_datasets_img)
        this._input_datasets_denoising = this.getimgurl(this.hosturlpath200, this.hosturlpath645, data.input_datasets_denoising)
        this._middle_mask = this.getimgurl(this.hosturlpath200, this.hosturlpath645, data.middle_mask)
        this.output_datasets_npy = this.getimgurl(this.hosturlpath200, this.hosturlpath645, data.output_datasets_npy)
        this.output_datasets_slide_npy = this.getimgurl(this.hosturlpath200, this.hosturlpath645, data.output_datasets_slide_npy)
        this._output_datasets_crop_preview = this.getimgurl(this.hosturlpath200, this.hosturlpath645, data.output_datasets_crop_preview)
        this.output_datasets_crop = this.getimgurl(this.hosturlpath16, this.hosturlpath64, data.output_datasets_crop)
        this._output_datasets_crop_n = this.getimgurl(this.hosturlpath16, this.hosturlpath64, data.output_datasets_crop_n)
        this._output_datasets_crop_p = this.getimgurl(this.hosturlpath16, this.hosturlpath64, data.output_datasets_crop_p)
        this.cellcntn = this.output_datasets_crop_n.length
        this.cellcntp = this.output_datasets_crop_p.length
      })
    }
  }
}
</script>

<style lang="scss" scoped>
  .img-step0 {
    border: 1px solid #11b95c;
    margin: 1px 1px 0px 0px;
  }
  .popover-container {
    width: 100%;
    height: 100%;
    display: flex;
    flex-wrap: wrap;
  }
  .dashboard-container {
    margin: 10px 10px 10px 10px;
    max-width: 1050px;
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

