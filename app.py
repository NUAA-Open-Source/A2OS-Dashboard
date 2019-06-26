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
def hello_world():
    dashboard_select_result = dashboard_sql_select_execute("select * from record")
    result = []
    for record in dashboard_select_result:
        behavior_select_result = behavior_sql_select_execute(record[1])
        x_data = []
        y_data = []
        for row in behavior_select_result:
            if (type(row[0]) == datetime.date):
                x_data.append(row[0].strftime("%Y-%m-%d"))
                y_data.append(row[1])
            else:
                x_data.append(row[0])
                y_data.append(row[1])
        result.append((record[0], record[2], record[3], record[4], x_data, y_data))
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
        x_data = []
        y_data = []
        behavior_select_result = behavior_sql_select_execute(sql)
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

def dashboard_sql_select_execute(sql):
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
    return cursor.fetchall()

def behavior_sql_select_execute(sql):
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
    return cursor.fetchall()