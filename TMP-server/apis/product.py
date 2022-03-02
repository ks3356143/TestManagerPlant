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
        sql = "SELECT * FROM `products` WHERE `status`=0 ORDER BY `Update` DESC"
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

    # 获取请求传递json body
    body = request.get_data()
    body = json.loads(body)

    #先做个判断看keyCode是否重复
    with connection:
        with connection.cursor() as cursor:
            select = "SELECT * FROM `products` WHERE `keyCode` = %s AND `status`=0"
            cursor.execute(select,(body['keyCode']),)
            result = cursor.fetchall()

        if len(result) > 0:
            resp_data['code'] = 200001
            resp_data['message'] = f"唯一项目代号{body['keyCode']}已经存在"
            return resp_data

        with connection.cursor() as cursor:
            sql = "INSERT INTO `products` (`type`,`keyCode`,`title`,`tester`,`step`,`customer`,`seller`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(body['type'],body['keyCode'],body['title'],body['tester'],body['step'],body['customer'],body['seller']))
            connection.commit()
        return resp_data


@app_product.route("/api/product/update",methods=['POST'])
def product_update():
    connection = connectDB()
    #定义默认返回体
    resp_data = {
        "code":20000,
        "message":"success",
        "data":[]
    }

    # 获取请求传递json body
    body = request.get_data()
    body = json.loads(body)

    #先做个判断看keyCode是否重复
    with connection:
        with connection.cursor() as cursor:
            select = "SELECT * FROM `products` WHERE `keyCode` = %s AND `status`=0"
            cursor.execute(select,(body['keyCode']),)
            result = cursor.fetchall()

        if len(result) > 0 and body['id'] != result[0]['id']:
            resp_data['code'] = 200001
            resp_data['message'] = f"唯一项目代号{body['keyCode']}已经存在"
            return resp_data

        with connection.cursor() as cursor:
            sql = "UPDATE `products` SET `type`=%s,`keyCode`=%s,`title`=%s,`tester`=%s,`step`=%s,`customer`=%s,`seller`=%s,`update`=NOW()  WHERE `id`= %s"
            cursor.execute(sql,(body['type'],body['keyCode'],body['title'],body['tester'],body['step'],body['customer'],body['seller'],body['id']))
            connection.commit()
        return resp_data

@app_product.route("/api/product/delete",methods=['DELETE'])
def product_delete():
    #定义默认返回体
    resp_data = {
        "code":20000,
        "message":"success",
        "data":[]
    }

    # 获取请求传递json body
    ID = request.args.get('id')
    print(ID)
    if ID is None:
        resp_data['code'] = 200002
        resp_data['message'] = "请求参数id不存在"
        return resp_data

    connection = connectDB()
    with connection.cursor() as cursor:
        sql = "DELETE from `products` WHERE `id`=%s"
        cursor.execute(sql,ID)
        connection.commit()
    return resp_data

# [POST方法]根据id更新状态项目状态，做软删除
@app_product.route("/api/product/remove", methods=['POST'])
def product_remove():
    # 返回的reponse
    resp_data = {
        "code": 20000,
        "message": "success",
        "data": []
    }
    ID = request.args.get('id')
    # 做个参数必填校验
    if ID is None:
        resp_data["code"] = 20002
        resp_data["message"] = "请求id参数为空"
        return resp_data
    # 重新链接数据库
    print(ID)
    connection = connectDB()
    with connection.cursor() as cursor:
        # 状态默认正常状态为0，删除状态为1
        # alter table products add status int default 0 not null comment '状态有效0，无效0' after `desc`;
        sql = "UPDATE `products` SET `status`=1 WHERE id=%s"
        cursor.execute(sql, ID)
        connection.commit()

    return resp_data


@app_product.route("/api/product/search",methods=['GET'])
def product_search():
    #搜索接口-先获取title和keyCode字段
    title = request.args.get('title')
    keyCode = request.args.get('keyCode')

    #基础sql语句
    sql = "SELECT * FROM `products` WHERE `status`=0"
    #如果title不为空，拼接title语句，注意LIKE关键词
    if title is not None:
        sql = sql + " AND `title` LIKE '%{}%'".format(title)
    if keyCode is not None:
        sql = sql + " AND `keyCode` LIKE '%{}%'".format(keyCode)
    #按时间排序
    sql = sql + " ORDER BY `update` DESC"
    #连接数据库操作
    connection = connectDB()
    with connection.cursor() as cursor:
        print("输出的sql为{}".format(sql))
        cursor.execute(sql)
        data = cursor.fetchall()
    #返回数据
    resp_data = {
        "code":20000,
        "data":data
    }
    return resp_data
