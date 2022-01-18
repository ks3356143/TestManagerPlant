# -*- coding:utf-8 -*-

from flask import request
from flask import Blueprint
import json

app_user = Blueprint("app_user",__name__)

@app_user.route("/api/user/login",methods=['POST'])
def login():
    data = request.get_data()
    js_data = json.loads(data)
    
    if 'username' in js_data and js_data['username']=='admin':
        result_success = {"code":20000,"data":{"token":"admin-token"}}
        return result_success
    else:
        result_error = {"code":60204,"message":"账号密码错误！"}
        return result_error
        
@app_user.route("/api/user/info",methods=["GET"])
def info():
    #获取GET请求中的token参数
    token = request.args.get("token")
    if token == "admin-token":
        result_success = {
            "code":20000,
            "data":{
                "roles":["admin"],
                "introduction":"我是超级管理员！",
                "avatar":"https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
                "name":"超级用户"}
            }
        return result_success
    else:
        result_error = {"code": 60204, "message": "用户信息获取错误"}
        return result_error