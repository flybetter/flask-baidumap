#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= flask-baidumap
@file= crawl_test
@author= wubingyu
@create_time= 2018/6/26 下午1:27
"""

import requests
from app.controller.crawl import xiaoqu_detect
from app.mysql.json_data import save
from app.controller.crawl import XIAOQU_NAME
import json
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def test_xiaoqu():
	name, paren_json, children_json = xiaoqu_detect("名都花园")
	print name, paren_json, children_json
	save(name, paren_json, children_json)


if __name__ == '__main__':
	list = "['aa','bb']"
	print type(list)
	list = eval(list)
	print type(list)

	with open(XIAOQU_NAME, 'r+') as f:
		f.seek(0)
		f.truncate()
		f.write(json.dumps(list))
