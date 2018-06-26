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


@app.route("/")
def show():
	with open(FILE_NAME, "r+") as f:
		points = f.read()
	return render_template("map.html", points=points)
