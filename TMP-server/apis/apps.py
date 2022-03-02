# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request
from dbutils.pooled_db import PooledDB
from config import config
from config.format import resp_format_success
import json
import pymysql.cursors

#使用数据库连接池，初始化链接数据库，提高数据库连接效率
pool = PooledDB(pymysql,mincached=1,maxcached=5,host=config.MYSQL_HOST,port=config.MYSQL_PORT,\
                user=config.MYSQL_USER,passwd=config.MYSQL_PASSWORD,database=config.MYSQL_DATABASES,\
                cursorclass=pymysql.cursors.DictCursor)

app_application = Blueprint("app_application",__name__)

@app_application.route("/api/application/product",methods=['GET'])
def getProduct():
    connection = pool.connection()
    with connection.cursor() as cursor:
        sql = "SELECT id,keyCode,title FROM `products` WHERE `status`=0 ORDER BY `update` DESC"
        cursor.execute(sql)
        data = cursor.fetchall()

    response = resp_format_success
    response['data'] = data
    return response

#分页查询apps接口
@app_application.route("/api/application/search",methods=['POST'])
def searchBykey():
    #先获取body
    body = request.get_data()
    body = json.loads(body)
    #基础定义sql语句
    sql = ''
    #获取前端pageSize和currentPage
    pageSize = 10 if body['pageSize'] is None else body['pageSize']
    currentPage = 1 if body['currentPage'] is None else body['currentPage']

    #拼接查询条件,注意使用通配符需要加上LIKE不要用=
    if 'productId' in body and body['productId'] != '':
        sql = sql + " AND `productId` = '{}'".format(body['productId'])
    if 'name' in body and body['name'] != '':
        sql = sql + " AND `name` LIKE '%{}%'".format(body['name'])
    if 'note' in body and body['note'] != '':
        sql = sql + " AND `note` LIKE '%{}%'".format(body['note'])
    if 'level' in body and body['level'] != '':
        sql = sql + " AND `level` LIKE '%{}%'".format(body['level'])
    if 'junstatus' in body and body['junstatus'] != '':
        sql = sql + " AND `junstatus` LIKE '%{}%'".format(body['junstatus'])
    # 排序和页数拼接
    sql = sql +' ORDER BY `updateDate` DESC LIMIT {},{}'.format((currentPage-1)*pageSize, pageSize)
    print(sql)

    # 使用连接池链接数据库
    connection = pool.connection()

    with connection:
        # 先查询总数
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM `apps` WHERE `status`=0')
            total = cursor.fetchall()
            num = len(total)
            print(num)
        # 执行查询
        with connection.cursor() as cursor:
            # 按照条件进行查询
            cursor.execute('SELECT P.title, A.* FROM apps AS A,products AS P WHERE A.productId = P.id and A.`status`=0' + sql)
            data = cursor.fetchall()

    # 按分页模版返回查询数据
    response = resp_format_success
    response['data'] = data
    response['total'] = num
    return response
