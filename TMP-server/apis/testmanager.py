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
    print(body)

    # 基础语句定义
    sql = ""

    # 获取pageSize和currentPage
    pageSize = 10 if 'pageSize' not in body or body['pageSize'] is None else body['pageSize']
    currentPage = 1 if 'currentPage' not in body or body['currentPage'] is None else body['currentPage']

    # 拼接查询条件
    if 'productId' in body and body['productId']!='':
        sql = sql + " AND A.productId LIKE '%{}%'".format(body['productId'])
    if 'appId' in body and body['appId'] != '':
        sql = sql + " AND A.appId LIKE '%{}%'".format(body['appId'])
    if 'tester' in body and body['tester'] != '':
        sql = sql + " AND T.tester LIKE '%{}%'".format(body['tester'])
    if 'type' in body and body['type'] != '':
        sql = sql + " AND T.type LIKE '%{}%'".format(body['type'])
    if 'ident' in body and body['ident'] != '':
        sql = sql + " AND T.ident = '%{}%'".format(body['ident'])
    if 'pickTime' in body and body['pickTime'] != '':
        sql = sql + " AND T.createDate >= '{}' and T.createDate <= '{}' ".format(body['pickTime'][0],
                                                                                 body['pickTime'][1])

    #拼接末尾
    sql = sql + " ORDER BY T.createDate DESC LIMIT {},{}".format((currentPage - 1) * pageSize, pageSize)
    # 使用连接池链接数据库
    connection = pool.connection()
    with connection:
        #先查询总数
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM testitem as T , apps as A where T.appId = A.id AND T.isDel=0' + sql)
            total = cursor.fetchall()
            num = len(total)
            print('查询总数为',num)

        #执行查询
        with connection.cursor() as cursor:
            cursor.execute("SELECT A.Id , T.* FROM testitem as T , apps as A WHERE T.appId=A.id AND T.isDel=0" + sql)
            data = cursor.fetchall()

        #按照模板返回数据
        response = format.resp_format_success
        response['data'] = data
        response['total'] = num
        return response

#测试项添加接口
@test_manager.route("/api/test/create",methods=['POST'])
def createRequest():
    body = request.get_data()
    body = json.loads(body)
    resp_success = format.resp_format_success
    resp_failed = format.resp_format_failed

    print(body)

    #判断必填参数
    if 'appId' not in body:
        resp_failed['message'] = 'appId不能为空'
    if 'tester' not in body:
        resp_failed['message'] = 'tester不能为空'
    if 'type' not in body:
        resp_failed['message'] = '类型type不能为空'
    if 'name' not in body:
        resp_failed['message'] = 'name不能为空'
    if 'ident' not in body:
        resp_failed['message'] = '标识不能为空'
    if 'refe' not in body:
        resp_failed['message'] = '追踪的需求文档名称不能为空'
    if 'refhao' not in body:
        resp_failed['message'] = '追踪的需求文档章节号不能为空'
    if 'refename' not in body:
        resp_failed['message'] = '追踪的需求文档章节名称不能为空'
    if 'shun' not in body:
        resp_failed['message'] = '测试项的执行优先级不能为空'
    if 'createUser' not in body:
        resp_failed['message'] = '测试项的创建人不能为空'
    if 'version' not in body:
        resp_failed['message'] = '版本不能为空'

    connection = pool.connection()
    #判断增加或修改逻辑
    with connection:
        with connection.cursor() as cursor:
            try:
                #其中id为自增不处理，创建时间自动获取不处理
                sqlInsert = "INSERT INTO testitem (title,appId,tester,version,`type`,`name`,ident,comm,`method`,refe,refhao,\
                            refname,shun,caseitem,passitem,createUser) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,\
                            %s,%s,%s,%s,%s,%s,%s)"
                #执行保存新增数据

                cursor.execute(sqlInsert,(body['title'],body['appId'],body['tester'],body['version'],body['type'],body['name'],\
                                            body['ident'],body['comm'],body['method'],body['refe'],body['refhao'],\
                                            body['refname'],body['shun'],\
                                            body['caseitem'],body['passitem'],body['createUser']))
                connection.commit()
                return resp_success
            except Exception as err:
                resp_failed['message'] = "添加测试项失败" + err
                return resp_failed

#获取回填数据信息
@test_manager.route("/api/test/info",methods=['GET'])
def getTestInfo():
    test_id =request.args.get('id') #获取前端传入的id
    resp_success = format.resp_format_success
    resp_failed = format.resp_format_failed

    if not test_id:
        resp_failed['message'] = '测试项ID未找到'
        return resp_failed
    connection = pool.connection()
    with connection:
        with connection.cursor() as cursor:
            #查询测试项列表-按创建时间查询
            sql="SELECT A.id as appId,A.name as appName,T.id,T.title,T.tester,T.version,T.type,T.name,T.ident,T.comm,T.refe,T.refhao,T.refname,T.method, \
                T.bind,T.stop,T.shun,T.caseitem,T.passitem,T.status,T.createUser FROM testitem as T,apps as A WHERE T.appId=A.id AND T.isDel=0\
                 AND T.id={}".format(test_id)
            cursor.execute(sql)
            data=cursor.fetchall()
            if len(data)==1:
                resp_success['data'] = data[0]
    return resp_success

@test_manager.route("/api/test/update",methods=['POST'])
def updateTestitem():
    body = request.get_data()
    body = json.loads(body)
    connection = pool.connection()
    resp_success = format.resp_format_success
    #先将历史数据查询出来，用于回填？
    with connection.cursor() as cursor:
        sql = "SELECT A.id as appId,A.name as appName,T.id,T.title,T.tester,T.version,T.type,T.name,T.ident,T.comm,T.refe,T.refhao,T.refname,T.method, \
            T.bind,T.stop,T.shun,T.caseitem,T.passitem,T.status,T.createUser FROM testitem as T,apps as A WHERE T.appId=A.id AND T.isDel=0\
             AND T.id={}".format(body['id'])
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data) == 1:
            old_test_info = data[0]
        else:
            print('原有数据查询异常')

        #如果传入有ID值，那么进行修改操作
        with connection.cursor() as cursor:
            #拼接修改语句
            sqlUpdate = "UPDATE testitem SET title=%s,appId=%s,tester=%s,version=%s,`type`=%s,`name`=%s,ident=%s,comm=%s,refe=%s,refhao=%s,refname=%s, \
                         `method`=%s,shun=%s,caseitem=%s,passitem=%s,createUser=%s,createDate=NOW() WHERE id=%s"
            cursor.execute(sqlUpdate,(body['title'],body['appId'],body['tester'],body['version'],body['type'],body['name'],body['ident'],\
                                      body['comm'],body['refe'],body['refhao'],body['refname'],body['method'],body['shun'],\
                                      body['caseitem'],body['passitem'],body['createUser'],body['id']))
            #提交执行
            connection.commit()
    return resp_success