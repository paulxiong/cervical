import request from '@/utils/request'

export function getPing1(query) {
  return request({
    url: '/api1/ping1',
    method: 'get',
    params: query
  })
}

export function getDatasetLists(query) {
  return request({
    url: '/api1/dtinfo',
    method: 'get',
    params: query
  })
}

export function getBatchInfo(query) {
  return request({
    url: '/api1/batchinfo',
    method: 'get',
    params: query
  })
}

export function getMedicalIdInfo(query) {
  return request({
    url: '/api1/medicalidinfo',
    method: 'get',
    params: query
  })
}

export function getCategoryInfo(query) {
  return request({
    url: '/api1/categoryinfo',
    method: 'get',
    params: query
  })
}

export function getImgListOfWanted(data) {
  return request({
    url: '/api1/imglistsofwanted',
    method: 'post',
    data
  })
}

export function getImgListOneByOne(query) {
  return request({
    url: '/api1/imglistsonebyone',
    method: 'get',
    params: query
  })
}

export function getLabelByImageId(query) {
  return request({
    url: '/api1/getLabelbyimageid',
    method: 'get',
    params: query
  })
}
