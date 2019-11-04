<template>
  <div class="email">
    <div class="header">
      <el-row>
        <el-button type="text" class="writing1">注册验证码</el-button>
        <el-button type="info" icon="el-icon-message" circle />
        <!-- <el-tag type="success">收件箱</el-tag> -->
      </el-row>
    </div>
    <div class="middle">
      <el-table
        :data="emailList"
        style="width: 100%"
      />
      <p class="middle1">讯动医疗 &lt;system@service.xundong.org&gt; </p>
    </div>
    <div class="middle2">
      <el-dropdown split-button type="primary" @click="handleClick">
        发送至
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item disabled>自己</el-dropdown-item>
          <el-dropdown-item>管理人员</el-dropdown-item>
          <el-dropdown-item>客服人员</el-dropdown-item>
          <el-dropdown-item>其他人员</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
    <div class="middle3">
      <p class="writing2">
        讯动医疗
      </p>
      <el-badge is-dot class="item">账号注册验证码</el-badge>
      <el-badge is-dot class="item">
        <el-button class="share-button" icon="el-icon-share" type="primary" />
      </el-badge>
    </div>
    <div class="footer">
      <span>您好，您正在使用<p class="writing3">****xundong@gmail.com</p>注册账号。</span>
      <span>您的注册验证码为：<p class="writing4">000000</p></span>
    </div>
    <div class="end">
      <span>谢谢！</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Email',
  components: {},
  data() {
    return {
      emailList: [
        {
          'name': '讯动医疗',
          'id': 'xundong@163.com'
        }
      ]
    }
  },
  methods: {
    handleClick() {
      alert('发送成功！')
    }
  }
}
</script>

<style lang="scss" scoped>
.email {
  margin-top: 40px;
  margin-left: 50px;
}
.writing1 {
  color: black;
  font-size: 60px;
  font-weight: bold;
}
.middle1 {
  font-weight: bold;
  font-size: 20px;
}
.writing2 {
  font-size: 40px;
}
.el-dropdown {
  vertical-align: top;
}
.el-dropdown + .el-dropdown {
  margin-left: 15px;
}
.el-icon-arrow-down {
  font-size: 12px;
}
.footer {
  margin-top: 50px;
}
.item {
  margin-top: 10px;
  margin-right: 40px;
}
.item:first-of-type {
  font-size: 60px;
  color: blueviolet;
}
.writing3 {
  color: blue;
  display: inline;
}
.writing4 {
  font-weight: bold;
  font-size: 20px;
  display: inline;
}
.end {
  margin-top: 100px;
}
</style>
