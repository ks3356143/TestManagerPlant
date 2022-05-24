# -*- coding:utf-8 -*-
from flask import Blueprint
import pymysql
from flask import request
import json
from dbutils.pooled_db import PooledDB
from config import config,format

pool = PooledDB(pymysql, mincached=2, maxcached=5,host=config.MYSQL_HOST, port=config.MYSQL_PORT,
                user=config.MYSQL_USER, passwd= config.MYSQL_PASSWORD, database=config.MYSQL_DATABASES,
                cursorclass=pymysql.cursors.DictCursor)
dashboard_test = Blueprint("dashboard_test", __name__)

@dashboard_test.route("/api/dashboard/metadata",methods=['POST'])
def get_request_stacked_metadata():
    body = json.loads(request.get_data())
    connection = pool.connection()
    with connection.cursor() as cursor:
        if 'date' in body and body['date'] is not None and len(body['date']) > 0:
            start_date = body['date'][0]
            end_date = body['date'][1]
            sql_select = "SELECT DATE_FORMAT(testitem.createDate,'%Y%u') weeks,apps.note,COUNT(apps.id) counts FROM testitem LEFT JOIN apps\
                          ON testitem.appId=apps.id WHERE testitem.createDate BETWEEN '{}' AND '{}' GROUP BY weeks,apps.note".format(str(start_date),str(end_date))
        else:
            sql_select = "SELECT DATE_FORMAT(testitem.createDate,'%Y%u') weeks,apps.note,COUNT(apps.id) counts FROM testitem LEFT JOIN apps ON testitem.appId\
                          =apps.id GROUP BY weeks,apps.note"

        cursor.execute(sql_select)
        table_data = cursor.fetchall()

    resp = format.resp_format_success
    resp['data'] = table_data
    print(resp)
    return resp