# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request
from dbutils.pooled_db import PooledDB
from config import config
from config.format import resp_format_success,resp_format_failed
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

@app_application.route("/api/application/update",methods=['POST'])
def product_update():
    body = request.get_data()
    body = json.loads(body)
    resp_success = resp_format_success
    resp_failed = resp_format_failed
    #由于是选填ID不用判断必填id，下面是判断必填参数
    if 'name' not in body:
        resp_format_failed.message = "名称不能为空"
        return resp_format_failed
    elif 'productId' not in body:
        resp_format_failed.message = "所属项目不能为空"
        return resp_format_failed
    elif 'level' not in body:
        resp_format_failed.message = "项目等级不能为空"
        return resp_format_failed
    elif 'junstatus' not in body:
        resp_format_failed.message = "软件改造/重用情况为空"
        return resp_format_failed
    elif 'producer' not in body:
        resp_format_failed.message = "产品负责人不能为空"
        return resp_format_failed

    connection = pool.connection()
    with connection:
        #如果传的值有ID，那么进行修改操作，否则新增
        if 'id' in body and body['id']!='':
            with connection.cursor() as cursor:
                #拼接修改语句，由于应用名name不能修改，不需要做重复校验
                sql = "UPDATE `apps` SET `name`=%s,`productId`=%s,`note`=%s,`level`=%s,`junstatus`=%s,`producer`=%s, \
                        `creteUser`=%s,`updateUser`=%s,`updateDate`=NOW() WHERE id=%s"
                cursor.execute(sql,(body['name'],body['productId'],body['note'],body['level'],body['junstatus'],\
                                    body['producer'],body['creteUser'],body['updateUser'],body['id']))
                connection.commit()
        else:
            #没有传id就走新增流程,先判断是否重复
            with connection.cursor() as cursor:
                select = "SELECT * FROM `apps` WHERE `name`=%s"
                cursor.execute(select,(body['name'],))
                result = cursor.fetchall()
            if len(result) > 0:
                resp_format_failed["code"] = 200001
                resp_format_failed["message"] = "该配置项名称已存在，请检查"
                return resp_format_failed
            with connection.cursor() as cursor:
                sql = "INSERT INTO `apps` (`name`,`productId`,`note`,`level`,`junstatus`,`producer`,`creteUser`,\
                      `updateUser`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql,(body["name"],body["productId"],body["note"],body["level"],body["junstatus"],\
                                    body["producer"],body["creteUser"],body["updateUser"]))
                connection.commit()
        return resp_format_success

#测试项-远程搜索接口-通知支持name和appId的搜索
@app_application.route("/api/application/options",methods=['GET'])
def getOptionsForSelected():
    value = request.args.get('value','')
    print("搜索的内容为：",value)
    response = resp_format_success
    connection = pool.connection()
    with connection.cursor() as cursor:
        #先按照appId模糊搜索，没有数据按name搜索
        sqlByAppId = "SELECT * FROM apps WHERE `id` LIKE '%{}%'".format(value)
        cursor.execute(sqlByAppId)
        dataByAppId = cursor.fetchall()
        if len(dataByAppId) > 0:
            response['data'] = dataByAppId
            print('进入了搜索appId分支',dataByAppId)
        else:
            sqlByName = "SELECT * FROM apps WHERE `name` LIKE '%{}%'".format(value)
            cursor.execute(sqlByName)
            dataByName = cursor.fetchall()
            response['data'] = dataByName
            print('进入了搜索app-name分支',dataByName)
        print('最后返回内容', response['data'])
        return response

