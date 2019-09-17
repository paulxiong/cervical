export function dateformat1(ts) {
  const hour = parseInt(ts / 3600)
  const mini = parseInt((ts % 3600) / 60)
  const sec = parseInt(ts % 60)
  let ret = ''
  ret = (hour > 0) ? (ret + hour + '时') : ret
  ret = (hour > 0 || mini > 0) ? (ret + mini + '分') : ret
  ret = (hour > 0 || mini > 0 || sec > 0) ? (ret + sec + '秒') : ret
  return ret
}

export function dateformat2(ts) {
  const _ts = new Date(ts)
  return '' + _ts.getFullYear() + '-' +
  (_ts.getMonth() + 1) + '-' +
  _ts.getDate() + ' ' +
  _ts.getHours() + ':' +
  _ts.getMinutes() + ':' +
  _ts.getSeconds()
}

export function dateformat3(ts) {
  const _ts = new Date(ts)
  return (`${_ts.getFullYear()}-${_ts.getMonth() + 1}-${_ts.getDate()} ${_ts.getHours()}:${_ts.getMinutes()}:${_ts.getSeconds()}`)
}
