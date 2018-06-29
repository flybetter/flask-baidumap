#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= flask-baidumap
@file= util
@author= wubingyu
@create_time= 2018/6/28 下午4:56
"""
import os
import json


def get_xiaoqu_name():
	with open(os.getcwd() + os.sep + "xiaoqu.json", "r+") as f:
		list = eval(f.read())
		return list


if __name__ == '__main__':
	get_xiaoqu_name()
