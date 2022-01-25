import request from '@/utils/request'

export function apiProductList() {
    return request({
      url: '/api/product/list',
      method: 'get',
    })
  }

export function apiProductCreate(requstBody){
  return request({
    url:"/api/product/create",
    method:"post",
    data:requstBody //这里是一个Json格式
  })
}