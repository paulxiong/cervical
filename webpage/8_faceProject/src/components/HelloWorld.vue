<template>
  <div class="nav-header">
   <div class="line">
<el-menu
  :default-active="activeIndex2"
  class="el-menu-demo"
  mode="horizontal"
  @select="handleSelect"
  background-color="#545c64"
  text-color="#fff"
  active-text-color="#ffd04b">
  <el-menu-item index="1">技术能力</el-menu-item>
  <el-submenu index="2">
    <template slot="title">SDK产品</template>
    <el-menu-item index="2-1">选项1</el-menu-item>
    <el-menu-item index="2-2">选项2</el-menu-item>
    <el-menu-item index="2-3">选项3</el-menu-item>
    <el-submenu index="2-4">
      <template slot="title">选项4</template>
      <el-menu-item index="2-4-1">选项1</el-menu-item>
      <el-menu-item index="2-4-2">选项2</el-menu-item>
      <el-menu-item index="2-4-3">选项3</el-menu-item>
    </el-submenu>
  </el-submenu>
  <el-menu-item index="3">解决方案</el-menu-item>
  <el-menu-item index="4" disabled>价格方案</el-menu-item>
  <el-menu-item index="5">开发者</el-menu-item>
  <el-menu-item index="6">联系我们</el-menu-item>
  <el-button type="primary" class="register">注册</el-button>
</el-menu>
   </div>
   <div class="lunbo-box">
     <el-carousel height="600px">
      <el-carousel-item v-for="item in pics" :key="item.url">
        <img :src="item.url" class="imgset"/>
      </el-carousel-item>
    </el-carousel>
  </div>
  <div class="title">
    <h1>我们的技术</h1>
  </div>
  <div class="content">
    <el-tabs v-model="activeName" @tab-click="handleClick">
    <el-tab-pane label="人脸识别" name="first" >人脸识别</el-tab-pane>
    <el-tab-pane label="人体识别" name="second" >人体识别</el-tab-pane>
    <el-tab-pane label="人像处理" name="third" >人像处理</el-tab-pane>
    <el-tab-pane label="文字识别" name="fourth" >文字识别</el-tab-pane>
    <el-tab-pane label="图像识别" name="fifth" >图像识别</el-tab-pane>
  </el-tabs>
  </div>
  <div class="content">
    <h1>接入方式 & 价格方案</h1>
    <h2>多种产品形式，灵活适用各类业务场景</h2>
  </div>
  <div class="content0">
    <el-row class="picture">
  <el-col :span="8" v-for="(o, index) in 2" :key="o" :offset="index > 0 ? 2 : 0">
    <el-card :body-style="{ padding: '0px' }">
      <img src="../assets/img/picture1.png" class="image">
      <div style="padding: 14px;">
        <span>根据您的业务需求在线灵活调用 Web API，轻松拥有 Face++ 最新的所有识别能力</span>
        <div class="bottom clearfix">
          <time class="time">{{ currentDate }}</time>
          <el-button type="text" class="button">操作按钮</el-button>
        </div>
      </div>
    </el-card>
  </el-col>
</el-row>
  </div>
  <div class="content1">
    <h1>我们的优势</h1>
  </div>
  <div class="content2">
    <h1>准备好开始使用了吗？</h1>
    <p>现在注册，免费使用Face++所有开放能力，让你的应用读懂世界</p>
    <a href="#" target="_blank" class="btn solid" data-v-3172dc60="" ho-click="homepage_try">免费体验</a>
    <a href="#" target="_blank" class="btn ghost" data-v-3172dc60="">联系我们</a>
  </div>
  <div class="footer">

  </div>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data() {
      return {
        activeIndex: '1',
        activeIndex2: '1',
        pics: [
        { url: require("../assets/img/banner.jpg") },
        { url: require("../assets/img/banner.jpg") },
        { url: require("../assets/img/banner.jpg") },
        { url: require("../assets/img/banner.jpg") }
      ],
     currentDate: new Date()
      };
    },
    methods: {
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
      }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.nav-header {

}
.register {
  float: right;
  margin-right: 10px;
  margin-top: 10px;
}
.imgset {
  width: 100%;
  height: 100%;
}
.title {
  text-align: center;
  margin-top: 30px;
  margin-bottom: 30px;
}
.content {
  margin-left: 15%;
  margin-right: 15%;
  /* width: 70%; !import
  display: flex; */
}
.time {
    font-size: 13px;
    color: #999;
  }
  
  .bottom {
    margin-top: 13px;
    line-height: 12px;
  }

  .button {
    padding: 0;
    float: right;
  }

  .image {
    width: 100%;
    display: block;
  }

  .clearfix:before,
  .clearfix:after {
      display: table;
      content: "";
  }
  
  .clearfix:after {
      clear: both
  }
  .picture {
    margin-left: 20%;
  }
  .content0 {
    padding-bottom: 50px;
  }
  .content1 {
    height: 300px;
    padding: 80px 0;
    background-image: url(https://cdn.faceplusplus.com.cn/mc-official/v2.1/img/advantage-bg.6c1ec80.png);
    background-size: cover;
    background-position: 50%;
    color: #fff;
    text-align: center;
  }
  .content2 {
    text-align: center;
    padding: 80px 0;
    background: #f7faff;
  }
  .solid[data-v-3172dc60] {
    background: #6395ff;
    border: 1px solid #6395ff;
    color: #fff;
  }
  .btn[data-v-3172dc60] {
    height: 36px;
    line-height: 36px;
    display: inline-block;
    font-size: 14px;
    text-align: center;
    width: 136px;
    margin-right: 30px;
  }
  .ghost[data-v-3172dc60] {
    border: 1px solid #263858;
    color: #263858;
    background: transparent;
  }
  .btn[data-v-3172dc60] {
    height: 36px;
    line-height: 36px;
    display: inline-block;
    font-size: 14px;
    text-align: center;
    width: 136px;
    margin-right: 30px;
}
  .footer{
    height: 100px;
    background-color: #1f1f1f;
    border-top: 1px solid hsla(0,0%,100%,.15);
    padding: 20px 0;
    text-align: center;
    color: hsla(0,0%,100%,.5);
    font-size: 12px;
    line-height: 17px;
    font-weight: 400;
  }
</style>