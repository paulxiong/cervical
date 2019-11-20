import request from '@/utils/request'

export function postErrlog(data) {
  return request({
    url: '/api1/errorlog',
    method: 'post',
    data
  })
}

export function getErrLog(query) {
  return request({
    url: '/api1/errorlog',
    method: 'get',
    params: query
  })
}

export function updateRegisterEmail(data) {
  return request({
    url: '/api1/registeremailcfg',
    method: 'post',
    data
  })
}

export function getRegisterEmail(query) {
  return request({
    url: '/api1/registeremailcfg',
    method: 'get',
    params: query
  })
}
