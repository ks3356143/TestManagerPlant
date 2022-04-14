from flask import Blueprint
from dbutils.pooled_db import PooledDB
from config import config,format
from flask import request
import pymysql.cursors
import json

pool = PooledDB(pymysql, mincached=2, maxcached=5,host=config.MYSQL_HOST, port=config.MYSQL_PORT,
                user=config.MYSQL_USER, passwd= config.MYSQL_PASSWORD, database=config.MYSQL_DATABASES,
                cursorclass=pymysql.cursors.DictCursor)
test_manager = Blueprint("test_manager",__name__)

@test_manager.route("/api/test/search",methods=['POST'])
def searchBykey():
    body = request.get_data()
    body = json.loads(body)

    # 基础语句定义
    sql = ""

    # 获取pageSize和currentPage
    pageSize = 10 if 'pageSize' not in body or body['pageSize'] is None else body['pageSize']
    currentPage = 1 if 'currentPage' not in body or body['currentPage'] is None else body['currentPage']

    # 拼接查询条件
    if 'appId' in body and body['appId'] != '':
        sql = sql + " AND A.appId LIKE '%{}%'".format(body['appId'])
    if 'tester' in body and body['tester'] != '':
        sql = sql + " AND R.tester LIKE '%{}%'".format(body['tester'])
    if 'type' in body and body['developer'] != '':
        sql = sql + " AND R.developer LIKE '%{}%'".format(body['developer'])
    if 'status' in body and body['status'] != '':
        sql = sql + " AND R.status = '{}'".format(body['status'])
    if 'pickTime' in body and body['pickTime'] != '':
        sql = sql + " AND R.createDate >= '{}' and R.createDate <= '{}' ".format(body['pickTime'][0],
                                                                                 body['pickTime'][1])

    #拼接末尾
    sql = sql + " ORDER BY T.createDate DESC LIMIT {},{}".format((currentPage - 1) * pageSize, pageSize)
    print(sql)
    # 使用连接池链接数据库
    connection = pool.connection()
    with connection:
        #先查询总数
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM testitem as T , apps as A where T.appId = A.id AND R.isDel=0' + sql)
            total = cursor.fetchall()
            num = len(total)
            print('查询总数为',num)

        #执行查询
        with connection.cursor() as cursor:
            cursor.execute("SELECT A.appId , T.* FROM testitem as T , apps as A WHERE T.appId=A.id AND T.isDel=0" + sql)
            data = cursor.fetchall()

        #按照模板返回数据
        response = format.resp_format_success
        response['data'] = data
        response['total'] = num
        return response


