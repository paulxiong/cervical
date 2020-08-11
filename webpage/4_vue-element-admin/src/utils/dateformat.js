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

// 返回时间“天”的开始处, 如 20200326
export function dateformat4() {
  const _ts = new Date()
  const y = ('' + _ts.getFullYear()).padStart(4, '0')
  const m = ('' + (_ts.getMonth() + 1)).padStart(2, '0')
  const d = ('' + _ts.getDate()).padStart(2, '0')
  return (`${y}${m}${d}`)
}

// 返回时间当前的时间戳，如 20200326155518
export function dateformat5() {
  const _ts = new Date()
  const y = ('' + _ts.getFullYear()).padStart(4, '0')
  const m = ('' + (_ts.getMonth() + 1)).padStart(2, '0')
  const d = ('' + _ts.getDate()).padStart(2, '0')
  const h = ('' + _ts.getHours()).padStart(2, '0')
  const min = ('' + _ts.getMinutes()).padStart(2, '0')
  const s = ('' + _ts.getSeconds()).padStart(2, '0')
  return (`${y}${m}${d}${h}${min}${s}`)
}

// 返回时间当前的时间戳，如 20200811103825164
export function dateformat6() {
  const _ts = new Date()
  const y = ('' + _ts.getFullYear()).padStart(4, '0')
  const m = ('' + (_ts.getMonth() + 1)).padStart(2, '0')
  const d = ('' + _ts.getDate()).padStart(2, '0')
  const h = ('' + _ts.getHours()).padStart(2, '0')
  const min = ('' + _ts.getMinutes()).padStart(2, '0')
  const s = ('' + _ts.getSeconds()).padStart(2, '0')
  const ms = ('' + _ts.getMilliseconds()).padStart(3, '0')
  return (`${y}${m}${d}${h}${min}${s}${ms}`)
}
