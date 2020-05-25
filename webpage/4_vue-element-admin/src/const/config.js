// for release
export const APIUrl =
  process.env.VUE_APP_API === 'production'
    ? 'http://medical.raidcdn.cn:3000'
    : 'http://dev.medical.raidcdn.cn:3000'
export const WSURL =
  process.env.VUE_APP_API === 'production'
    ? 'ws://medical.raidcdn.cn:3000'
    : 'ws://dev.medical.raidcdn.cn:3000'
// for local debug
// export const WSURL = 'http://medical.raidcdn.cn:3000'
// export const APIUrl = 'http://medical.raidcdn.cn:3000'
