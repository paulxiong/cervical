<template>
  <div class="temps">
    <el-table
      :data="tableData"
      style="width: 100%"
    >
      <el-table-column
        align="center"
        prop="variabletitle"
        label="变量标题"
        width="200"
      />
      <el-table-column align="center" prop="variablevalue" width="720" label="变量值">
        <el-input
          v-model="input"
          placeholder="请输入内容"
          clearable
        />
      </el-table-column>
      <el-table-column
        align="center"
        prop="variablename"
        label="变量名"
      />
    </el-table>
  </div>
</template>

<script>
export default {
  name: 'Temps',
  components: {},
  data() {
    return {
      tableData: [{
        variabletitle: '邮件发送方式',
        variablename: '{$site.mail_type}'
      }, {
        variabletitle: 'SMTP服务器',
        variablename: '{$site.mail_smtp_host}',
        variablevalue: 'xundong.qq.com'
      }, {
        variabletitle: 'SMTP端口',
        variablename: '{$site.mail_smtp_port}'
      }, {
        variabletitle: 'SMTP用户名',
        variablename: '{$site.mail_smtp_user}'
      }, {
        variabletitle: 'SMTP密码',
        variablename: '{$site.mail_smtp_pass}'
      }, {
        variabletitle: 'SMTP验证方式',
        variablename: '{$site.mail_verify_type}'
      }, {
        variabletitle: '发件人邮箱',
        variablename: '{$site.mail_from}'
      }],
      options: [{
        value: '选项1',
        label: 'Please select'
      }, {
        value: '选项2',
        label: 'SMTP'
      }, {
        value: '选项3',
        label: 'Mail'
      }],
      value: '',
      input: ''
    }
  },
  methods: {}
}
</script>

<style lang="scss" scoped>
.temps {
}
</style>
