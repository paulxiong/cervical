export function dateformat1(ts) {
  var hour = parseInt(ts / 3600)
  var mini = parseInt((ts % 3600) / 60)
  var sec = parseInt(ts % 60)
  var ret = ''
  ret = (hour > 0) ? (ret + hour + '时') : ret
  ret = (hour > 0 || mini > 0) ? (ret + mini + '分') : ret
  ret = (hour > 0 || mini > 0 || sec > 0) ? (ret + sec + '秒') : ret
  return ret
}

export function dateformat2(ts) {
  var _ts = new Date(ts)
  return '' + _ts.getFullYear() + '-' +
  (_ts.getMonth() + 1) + '-' +
  _ts.getDate() + ' ' +
  _ts.getHours() + ':' +
  _ts.getMinutes() + ':' +
  _ts.getSeconds()
}

export function dateformat3(ts) {
  var _ts = new Date(ts)
  return ('' + _ts.getHours() + ':' + _ts.getMinutes() + ':' + _ts.getSeconds())
}
