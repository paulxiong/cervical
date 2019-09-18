// for release
export const APIUrl =
  process.env.NODE_ENV === 'production'
    ? 'http://medical.raidcdn.cn:3000'
    : 'http://dev.medical.raidcdn.cn:3000'
export const ImgServerUrl =
  process.env.NODE_ENV === 'production'
    ? 'http://medical.raidcdn.cn:3001'
    : 'http://dev.medical.raidcdn.cn:3001'

// for local debug
// export const APIUrl = 'http://192.168.1.100:9000'
// export const ImgServerUrl = 'http://192.168.1.102:18000'
