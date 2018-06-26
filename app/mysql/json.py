#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= flask-baidumap
@file= json
@author= wubingyu
@create_time= 2018/6/26 上午11:26
"""
import pymysql.cursors


def save(name, json, children_json):
	connection = pymysql.connect(
		host='192.168.10.200',
		port=3306,
		user='root',
		password='',
		database='demo'
	)
	cursor = connection.cursor()
	sql = "insert into lianjia_json (name,json,children_json) VALUES (%s,%s,%s)" % (name, json, children_json)
	cursor.execute(sql)
	connection.commit()
	cursor.close()
	connection.close()


if __name__ == '__main__':
	save()
