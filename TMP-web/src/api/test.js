import request from '@/utils/request'

//测试项模糊查询组合接口
export function apiTestSearch(requestBody) {
    return request({
      url: '/api/test/search',
      method: 'post',
      data:requestBody
    })
  }

// 调用应用增加/修改统一接口
export function reqCreate(requestBody) {
  return request({
    url: '/api/test/create',
    method: 'post',
    data:requestBody
  })
}

// 获取应用列表，可按照appid 或者 name模糊查询
export function apiAppsIds(value) {
  return request({
    url: '/api/application/options?value=' + value,
    method: 'get'
  })
}