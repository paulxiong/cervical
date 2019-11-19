import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/user/login',
    method: 'post',
    data
  })
}

export function getUserInfo(query) {
  return request({
    url: '/user/userinfo',
    method: 'get',
    params: query
  })
}

export function getUserLists(query) {
  return request({
    url: '/user/lists',
    method: 'get',
    params: query
  })
}

export function getUserLog(query) {
  return request({
    url: '/user/accesslog',
    method: 'get',
    params: query
  })
}

export function getCode(data) {
  return request({
    url: '/user/emailcode',
    method: 'post',
    data
  })
}

export function register(data) {
  return request({
    url: '/user/register',
    method: 'post',
    data
  })
}

export function getInfo() {
  return request({
    url: '/user/info',
    method: 'get'
  })
}

export function logout() {
  return request({
    url: '/user/logout',
    method: 'get'
  })
}

export function updateUserInfo(data) {
  return request({
    url: '/user/updateinfo',
    method: 'post',
    data
  })
}
