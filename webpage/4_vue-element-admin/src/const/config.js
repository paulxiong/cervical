// for release
export const APIUrl =
  process.env.VUE_APP_API === 'production'
    ? 'http://medical.raidcdn.cn:3000'
    : 'http://dev.medical.raidcdn.cn:3000'
// for local debug
// export const APIUrl = 'http://1668u455y4.imwork.net:9000/'
// export const ImgServerUrl = 'http://192.168.1.102:18000'
