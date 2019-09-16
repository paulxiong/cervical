// for release
export const APIUrl =
  process.env.NODE_ENV === 'production'
    ? 'http://medical.raidcdn.cn:3000'
    : 'http://9200.gpu.raidcdn.cn:9700'
export const ImgServerUrl =
  process.env.NODE_ENV === 'production'
    ? 'http://medical.raidcdn.cn:3001'
    : 'http://9201.gpu.raidcdn.cn:9700'

// for local debug
// export const APIUrl = 'http://192.168.1.100:9000'
// export const ImgServerUrl = 'http://192.168.1.102:18000'
