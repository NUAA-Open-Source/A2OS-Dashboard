# Copyright 2019 SafeU Dev Team
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License. 

# coding=utf-8
from flask import Flask, render_template, request
import pymysql
import datetime
import functools
import configparser
import json

app = Flask(__name__)
cf = configparser.ConfigParser()
cf.read('db.conf')

@app.route('/')
def home():
    dashboard_select_result = dashboard_sql_execute("select * from record")
    result = []
    for record in dashboard_select_result:
        behavior_select_result = behavior_sql_execute(record[1])
        x_data = []
        y_data = []
        for row in behavior_select_result:
            if (type(row[0]) == datetime.date):
                x_data.append(row[0].strftime("%Y-%m-%d"))
                y_data.append(row[1])
            else:
                x_data.append(row[0])
                y_data.append(row[1])
        result.append((record[0], record[2], record[3], record[4], record[5], x_data, y_data))
    return render_template("home.html", result=result)

@app.route('/new', methods=["POST", "GET"])
def new():
    if request.method == "GET":
        return render_template("new.html")
    elif request.method == "POST":
        title = request.form['title']
        x_title = request.form['x_title']
        y_title = request.form['y_title']
        sql = request.form['sql']
        chart_type = request.form['chart_type']
        # print("insert into record (title, xtitle, ytitle, query, chart_type) values ('%s', '%s', '%s', '%s', '%s')" % (title, x_title, y_title, pymysql.escape_string(sql), type_chart))
        dashboard_sql_execute("insert into record (title, xtitle, ytitle, query, chart_type) values ('%s', '%s', '%s', '%s', '%s')" % (title, x_title, y_title, pymysql.escape_string(sql), chart_type)) 
        
        result = {"status": "success"}
        return json.dumps(result)

@app.route('/quicklook', methods=["POST"])
def quicklook():
    title = request.form['title']
    x_title = request.form['x_title']
    y_title = request.form['y_title']
    sql = request.form['sql']
    x_data = []
    y_data = []
    behavior_select_result = behavior_sql_execute(sql)
    for row in behavior_select_result:
        if (type(row[0]) == datetime.date):
            x_data.append(row[0].strftime("%Y-%m-%d"))
            y_data.append(row[1])
        else:
            x_data.append(row[0])
            y_data.append(row[1]) 
    result = {
        "title": title,
        "x_title": x_title,
        "y_title": y_title,
        "x_data": x_data,
        "y_data": y_data
    }
    return json.dumps(result) 

def dashboard_sql_execute(sql):
    connection = pymysql.connect(
        host = cf.get('a2os_dashboard_db', 'a2os_dashboard_db_host'),
        port = cf.getint('a2os_dashboard_db', 'a2os_dashboard_db_port'),
        user = cf.get('a2os_dashboard_db', 'a2os_dashboard_db_user'),
        password = cf.get('a2os_dashboard_db', 'a2os_dashboard_db_password'),
        db = cf.get('a2os_dashboard_db', 'a2os_dashboard_db'),
        charset = cf.get('a2os_dashboard_db', 'a2os_dashboard_db_charset')
    )
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    select_result = cursor.fetchall()
    cursor.close()
    connection.close()
    return select_result

def behavior_sql_execute(sql):
    connection = pymysql.connect(
        host=cf.get('behavior_db', 'behavior_db_host'),
        port=cf.getint('behavior_db', 'behavior_db_port'),
        user=cf.get('behavior_db', 'behavior_db_user'),
        password=cf.get('behavior_db', 'behavior_db_password'),
        db=cf.get('behavior_db', 'behavior_db'),
        charset=cf.get('behavior_db', 'behavior_db_charset')
    )
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    select_result = cursor.fetchall()
    cursor.close()
    connection.close()
    return select_result