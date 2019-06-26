from flask import Flask, render_template
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
    result = sql_select_execute('select DATE_FORMAT(date(created_at), "%Y-%m-%d"), count(*) from events where name="home" and date(created_at) BETWEEN date(NOW())-6 and DATE(now()) group by date(created_at);')
    x_data = []
    y_data = []
    for row in result:
        if (type(row[0]) == datetime.date):
            x_data.append(row[0].strftime("%Y-%m-%d"))
            y_data.append(row[1])
        else:
            x_data.append(row[0])
            y_data.append(row[1])
    print(x_data)
    print(y_data)
    return render_template("home.html", x=x_data, y=y_data)

def sql_select_execute(sql):
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