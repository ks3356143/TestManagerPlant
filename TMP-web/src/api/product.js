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

export function apiProductUpdate(requstBody){
  return request({
    url:"/api/product/update",
    method:"post",
    data:requstBody 
  })
}

export function apiProductDelete(id){
  return request({
    url:"/api/product/delete",
    method:"delete",
    params:{
      "id":id
    }
  })
}

// 软删除，更改数据状态
export function apiProductRemove(id) {
  return request({
    url: '/api/product/remove',
    method: 'post',
    params: {
      'id': id
    }
  })
}

// 模糊查询项目名称以及唯一标识（项目编号）
export function apiProductSearch(params) {
  return request({
    url: '/api/product/search',
    method: 'get',
    params: params
  })
}