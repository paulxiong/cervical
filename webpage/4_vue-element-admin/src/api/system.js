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

export function updateEmail(data) {
  return request({
    url: '/api1/emailcfg',
    method: 'post',
    data
  })
}

export function getEmail(query) {
  return request({
    url: '/api1/emailcfg',
    method: 'get',
    params: query
  })
}
