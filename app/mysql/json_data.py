#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= flask-baidumap
@author= wubingyu
@create_time= 2018/6/26 上午11:26
"""
import pymysql.cursors
import logging

logging.basicConfig(level=logging.DEBUG)


def save(name, parent_json, children_json):
	connection = pymysql.connect(
		host='192.168.10.200',
		port=3306,
		user='root',
		password='',
		database='demo',
		use_unicode=True,
		charset="utf8"
	)
	cursor = connection.cursor()
	sql = "insert into lianjia_json (name,parent_json,children_json) VALUES ('%s','%s','%s')" % (
		name, parent_json, children_json)
	cursor.execute(sql)
	connection.commit()
	cursor.close()
	connection.close()


def select_one(id):
	cursor, connection = mysql_connect()
	sql = "select * from lianjia_json where id=" + id
	cursor.execute(sql)
	data = cursor.fetchall()
	logging.info(data)
	mysql_close(cursor, connection)
	return data


def select_all():
	cursor, connection = mysql_connect()
	sql = "select * from lianjia_json"
	cursor.execute(sql)
	datas = cursor.fetchall()
	mysql_close(cursor, connection)
	return datas


def mysql_connect():
	connection = pymysql.connect(host='192.168.10.200', port=3306, user='root', password='', database='demo',
								 use_unicode=True, charset='utf8')
	cursor = connection.cursor()
	return cursor, connection


def mysql_close(cursor, connection):
	connection.commit()
	cursor.close()
	connection.close()


if __name__ == '__main__':
	select_one('1')
