<template>
  <div class="img-server">
    <div class="setting">
      <div class="setting-en">
        <h4>是否启用图片防盗链</h4>
        <el-switch v-model="referer_en" active-text="开" inactive-text="关" />
      </div>
      <div class="setting-time">
        <h4>设置图片缓存时间</h4>
        <el-select v-model="refererSetting.imgexpires" style="width:100px;" placeholder="请选择">
          <el-option v-for="item in [24, 48, 72]" :key="item" :label="item" :value="item" />
        </el-select>
      </div>
    </div>
    <div class="img-upload" style="display: flex;">
      <div class="setting-401">
        <h4>图片401设置</h4>
        <el-image :src="APIUrl + refererSetting.referer_401_url" />
        <avatar-cropper
          trigger="#pick-401"
          :upload-headers="headers"
          :upload-url="uploadURL"
          @uploaded="handleUploaded401"
        />
        <el-button id="pick-401" type="success" class="upload" style="margin-left:10px;" round>上传</el-button>
      </div>
      <div class="setting-404">
        <h4>图片404设置</h4>
        <el-image :src="APIUrl + refererSetting.referer_404_url" />
        <avatar-cropper
          trigger="#pick-404"
          :upload-headers="headers"
          :upload-url="uploadURL"
          @uploaded="handleUploaded404"
        />
        <el-button id="pick-404" type="success" class="upload" style="margin-left:10px;" round>上传</el-button>
      </div>
    </div>
    <div class="url-add">
      <div class="setting-list">
        <h4>白名单</h4>
        <el-input v-model="refererInput" placeholder="请输入内容" style="width: 500px;">
          <el-button slot="append" type="primary" @click="addUrl">添加</el-button>
        </el-input>
        <div class="list" style="max-height: 300px;overflow-y: auto;">
          <p v-for="(v, i) in refererSetting.referers" :key="i"><span>{{ i }}</span>{{ v }}<i class="el-icon-close" @click="delReferer(v)" /></p>
        </div>
      </div>
    </div>
    <div class="setting-btn" style="margin-top: 10px;">
      <el-button type="primary" @click="saveAll">保存</el-button>
      <el-button>重置</el-button>
    </div>
  </div>
</template>

<script>

import { getReferer, updateReferer } from '@/api/system'
import AvatarCropper from 'vue-avatar-cropper'
import { validURL } from '@/utils/validate'
import { getToken } from '@/utils/auth'
import { APIUrl } from '@/const/config'

export default {
  name: 'ImgServer',
  components: { AvatarCropper },
  data() {
    return {
      APIUrl: APIUrl,
      uploadURL: APIUrl + '/api1/uploadimg',
      refererInput: '',
      referer_en: false,
      headers: {
        'Authorization': getToken()
      },
      refererSetting: {}
    }
  },
  created() {
    this.getReferer()
  },
  methods: {
    addUrl() {
      if (validURL(this.refererInput)) {
        if (!this.refererSetting.referers) {
          this.refererSetting.referers = []
        }
        this.refererSetting.referers.push(this.refererInput)
      } else {
        this.$message.error('请输入正确的超链接')
      }
    },
    delReferer(v) {
      const idx = this.refererSetting.referers.indexOf(v)
      this.refererSetting.referers.splice(idx, 1)
    },
    handleUploaded401(res) {
      this.refererSetting.referer_401_url = res.data
    },
    handleUploaded404(res) {
      this.refererSetting.referer_404_url = res.data
    },
    getReferer() {
      getReferer().then(res => {
        this.refererSetting = res.data.data
        if (this.refererSetting.referer_en === 2) {
          this.referer_en = true
        }
      })
    },
    saveAll() {
      this.refererSetting.referer_en = 1
      if (this.referer_en) {
        this.refererSetting.referer_en = 2
      }
      updateReferer(this.refererSetting).then(res => {
        this.$message({
          message: '图片服务设置保存成功',
          type: 'success'
        })
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.img-server {
  height: 100%;
  padding: 10px 30px;
}
.setting {
  display: flex;
  justify-content: flex-start;
}
// .img-upload {
//   padding-top: 50px;
// }
h4 {
  margin-right: 12px;
}
.setting-list {
  width: 500px;
  padding-top: 50px;
  p {
    background: rgb(239, 238, 238);
    margin: 10px 0;
    display: flex;
    justify-content: space-between;
    i {
      color: red;
      cursor: pointer;
    }
  }
}
.setting-en,
.setting-time,
.setting-401,
.setting-404 {
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
  align-items: center;
  margin: 50px;
}
.setting-btn {
  padding-top: 50px;
}
</style>

