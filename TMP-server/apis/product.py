# -*- coding:utf-8 -*-
 
from flask import Blueprint
import pymysql
from flask import request
import json

app_product = Blueprint("app_product", __name__)

# 使用用户名密码创建数据库链接
# PyMySQL使用文档  https://pymysql.readthedocs.io
def connectDB():
    connection = pymysql.connect(host='localhost',   # 数据库IP地址或链接域名
                                 user='root',     # 设置的具有增改查权限的用户
                                 password='root', # 用户对应的密码
                                 database='TPMStore',# 数据表
                                 charset='utf8mb4',  # 字符编码
                                 cursorclass=pymysql.cursors.DictCursor) # 结果作为字典返回游标
    return connection


@app_product.route("/api/product/list",methods=['GET'])
def product_list():
    # 使用python的with..as控制流语句（相当于简化的try except finally）
    # 初始化数据库链接
    connection = connectDB()
    with connection.cursor() as cursor:
        #查询产品信息表-按更新时间新旧排序
        sql = "SELECT * FROM `products` ORDER BY `Update` DESC"
        cursor.execute(sql)
        data = cursor.fetchall()

    #按返回模式格式进行json结果返回
    resp_data = {
        "code":20000,
        "data":data
    }
    return resp_data

@app_product.route("/api/product/create",methods=['POST'])
def product_create():
    connection = connectDB()
    #定义默认返回体
    resp_data = {
        "code":20000,
        "message":"success",
        "data":[]
    }

    #获取请求传递的json
    body = request.get_data()
    body = json.loads(body)

    #先做个判断看keyCode是否重复
    with connection.cursor() as cursor:
        select = "SELECT * FROM `products` WHERE `keyCode` = %s"
        cursor.execute(select,(body['keyCode']),)