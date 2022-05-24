import request from '@/utils/request'

// 获取图标数据接口
export function requestMetaData(body) {
    return request({
      url: '/api/dashboard/metadata',
      method: 'post',
      data: body
    })
  }