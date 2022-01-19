# -*- coding:utf-8 -*-
 
from flask import Blueprint

app_product = Blueprint("app_product", __name__)

@app_product.route("/api/product/list",methods=['GET'])
def product_list():
    # 硬编码返回list
    data = [
        {"id":1, "keyCode":"R2021", "title":"源代码安全漏洞挖掘与分析系统软件", "type":"军方项目", "tester":"陈俊亦","seller":"高才栋","step":"等待报告评审","customer":"电信十所","begintime":"2020年5月8日","update":"2020-04-06"},
        {"id":2, "keyCode":"R2113", "title":"WXT星敏触发处理主控软件", "type":"航天项目", "tester":"陈俊亦","seller":"高才栋","step":"静态审查结束","customer":"空间中心","begintime":"2021年7月19日","update":"2021-01-06"},
    ]
    # 按返回模版格式进行json结果返回
    resp_data = {
        "code": 20000,
        "data": data
    }
    return resp_data