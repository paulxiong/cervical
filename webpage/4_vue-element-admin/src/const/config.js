// for release
export const APIUrl =
  process.env.VUE_APP_API === 'production'
    ? 'http://medical.raidcdn.cn:3000'
    : 'http://192.168.1.100:9000'
export const WSURL =
  process.env.VUE_APP_API === 'production'
    ? 'ws://medical.raidcdn.cn:3000'
    : 'http://192.168.1.100:9000'
// for local debug
// export const WSURL = 'http://medical.raidcdn.cn:3000'
// export const APIUrl = 'http://medical.raidcdn.cn:3000'
