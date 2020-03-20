<template>
  <div>
    <uploader :options="options" class="uploader-example">
      <uploader-unsupport />
      <uploader-drop>
        <p>Drop files here to upload or</p><el-link href="https://github.com/simple-uploader/vue-uploader/blob/master/README_zh-CN.md">上传组件文档</el-link>
        <uploader-btn>select files</uploader-btn>
        <uploader-btn :attrs="attrs">select images</uploader-btn>
        <uploader-btn :directory="true">select folder</uploader-btn>
      </uploader-drop>
      <uploader-list />
    </uploader>
  </div>
</template>
