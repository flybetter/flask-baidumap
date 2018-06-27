#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= flask-baidumap
@file= baidu
@author= wubingyu
@create_time= 2018/6/22 上午10:30
"""
from app import app
from flask import render_template
from app.controller.crawl import FILE_NAME
from app.mysql.json_data import *
import json


@app.route("/")
def show():
	datas = select_all()
	with open(FILE_NAME, "r+") as f:
		points = f.read()
	return render_template("map.html", points=points, datas=datas)


@app.route("/xiaoqu/<id>")
def show_id(id):
	points_list = []
	datas = select_all()
	xiaoqu = select_one(id)
	xiaoqu_name_list = ''
	one = json.loads(xiaoqu[0][2])
	del one['name']
	points_list.append(one)

	xiaoqu_list = json.loads(xiaoqu[0][3])
	for object in xiaoqu_list:
		xiaoqu_name_list += object['name'] + ','
		del object['name']
		points_list.append(object)

	points = json.dumps(points_list, ensure_ascii=False, default=house2dict)

	return render_template("map.html", points=points, datas=datas, xiaoqu=xiaoqu, xiaoqu_name_list=xiaoqu_name_list)


def house2dict(house):
	return {
		'lng': house.lng,
		'lat': house.lat,
		'count': house.count
	}
