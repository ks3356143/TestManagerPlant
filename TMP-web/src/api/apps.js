import request from '@/utils/request'

// 应用搜索接口
export function apiAppsSearch(requestBody) {
  return request({
    url: '/api/application/search',
    method: 'post',
    data: requestBody
  })
}

// 产品选择项目列表
export function apiAppsProduct() {
  return request({
    url: '/api/application/product',
    method: 'get'
  })
}

// 新增/修改配置项/系统列表
export function apiAppsCommit(requestBody){
  return request({
    url:"/api/application/update",
    method:'post',
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