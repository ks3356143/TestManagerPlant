import request from '@/utils/request'

//测试项模糊查询组合接口
export function apiTestSearch(requestBody) {
    return request({
      url: '/api/test/search',
      method: 'post',
      data:requestBody
    })
  }