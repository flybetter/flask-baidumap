#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= flask-baidumap
@file= redis_connection
@author= wubingyu
@create_time= 2018/7/12 下午4:54
"""

import redis
import json
import app.mysql

HOST = '192.168.10.221'
PORT = '6379'


def redis_connect(host=HOST, port=PORT):
	redis_connect = redis.Redis(host, port)
	return redis_connect


def get_data(list):
	connection = redis_connect()
	result = connection.mget(list)
	return result


def reset_redis():
	app.mysql

if __name__ == '__main__':
	list = list()
	list.append("峨嵋岭19号")
	list.append("沙塘园")
	print json.dumps(get_data(list), ensure_ascii=False)
