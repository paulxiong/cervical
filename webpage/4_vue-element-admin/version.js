const { execFileSync } = require('child_process')
const fs = require('fs')

function datetime() {
    const date = new Date()
    const year = date.getFullYear()
    const month = date.getMonth() + 1
    const day = date.getDate()
    const hour = date.getHours()
    const minute = date.getMinutes()
    const second = date.getSeconds()
    return '' + year + '' + month + '' + day + '' + hour + '' + minute + '' + second
}

function commitid() {
    const stdout = execFileSync('git', ['rev-parse', '--short', 'HEAD'])
    return stdout.toString().replace(/[\r\n]/g, "")
}

const version = '翠湖v1'
const ts = datetime()
const subversion = commitid()

obj = {
    'version': version,
    'ts': ts,
    'subversion': subversion
}

strobj = 'module.exports = {\n'
strobj = strobj + '\t\'version\': ' + '\'' + version + '\',\n'
strobj = strobj + '\t\'subversion\': ' + '\'' + subversion + '\',\n'
strobj = strobj + '\t\'ts\': ' + '\'' + ts + '\'\n'
strobj = strobj + '}\n'

fs.writeFileSync('version.config.js', strobj)
