#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= flask-baidumap
@file= crawl
@author= wubingyu
@create_time= 2018/6/22 上午11:20
"""
import os
import datetime
import stat
import requests
import json
import logging
from bs4 import BeautifulSoup
import re
from app.model.House import House
from itertools import groupby
from app.mysql.json_data import save

import sys

reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(level=logging.DEBUG)
# https://nj.lianjia.com/ershoufang/esfrecommend?id=103102480999
# https://nj.lianjia.com/ershoufang/esfrecommend?id=103102455850

RECOM_URL = "https://nj.lianjia.com/ershoufang/esfrecommend?id=*"

FILE_NAME = "/Users/wubingyu/PycharmProjects/Projects/2.7.11/flask-baidumap/app/controller/temp.json"

XIAOQU_URL = "https://nj.lianjia.com/xiaoqu/rs"

XIAOQU_PAGE_URL = "https://nj.lianjia.com/xiaoqu/pg*/"

HOUSE_URL = "https://nj.lianjia.com/ershoufang/*.html"

XIAOQU_HOUSE_URL = "https://nj.lianjia.com/ershoufang/rs*/"

xiaoqu_name = []

xiaoqu_dict = dict()

result = []

HOUSECOUNT = {"Top": 100, "First": 90, "Second": 70, "Third": 60, "Default": 50}


# https://nj.lianjia.com/ershoufang/rs名都花园/


def get_houseid(xiaoqu_id):
	pass


def no_rel(tag):
	return tag.has_attr("target") and tag.has_attr("href") and re.match("https://nj.lianjia.com/xiaoqu/*",
																		tag["href"]) and not tag.has_attr("rel")


# 获得所有小区名称
def get_xiaoquname(content):
	soup = BeautifulSoup(content, "html.parser")
	# logging.debug(content)
	list = soup.find_all(no_rel, limit=30)
	for entry in list:
		logging.debug(re.search(">(.*)<", str(entry)).group(1))
		xiaoqu_name.append(re.search(">(.*)<", str(entry)).group(1))

	page = re.search(r"{\"totalPage\":(\d+),\"curPage\":(\d+)}", content)
	totalpage = int(page.group(1))
	curpage = int(page.group(2))
	logging.debug("totalPage:%d curPage:%d" % (totalpage, curpage))
	if curpage <= totalpage:
		return XIAOQU_PAGE_URL.replace("*", str(curpage + 1))
	else:
		return None


def get_house_by_xiaoqu(content):
	soup = BeautifulSoup(content, "html.parser")
	list = soup.find_all("a", attrs={"class": "img", "data-log_index": "1", "data-el": "ershoufang", "data-bl": "list"})
	return list[0]["href"]


def get_house_graphx(content):
	coordinate = re.search("resblockPosition:'(.*)'", content).group(1)
	houseId = re.search(" houseId:'(.*)'", content).group(1)
	houseName = re.search("resblockName:'(.*)'", content).group(1)
	logging.debug("coordinate:" + coordinate + " houseId:" + houseId + " houseName:" + houseName)
	house = House(coordinate.split(',')[0], coordinate.split(',')[1], houseName, HOUSECOUNT['Top'])
	result.append(house)
	json_response = request_url(RECOM_URL.replace("*", houseId))
	for object in json.loads(json_response)["data"]["recommend"]:
		second_content = request_url(object["viewUrl"])
		coordinate = re.search("resblockPosition:'(.*)'", second_content).group(1)
		house = House(coordinate.split(',')[0], coordinate.split(',')[1], HOUSECOUNT['Second'])
		result.append(house)


def write():
	final_result = list(set(result))
	data = json.dumps(final_result, default=lambda object: object.__dict__)
	with open(FILE_NAME, "r+") as f:
		f.read()
		f.seek(0)
		f.truncate()
		f.writelines(data)


def request_url(url):
	response = requests.get(url)
	return response.text


def xiaoqu_filter(tag):
	return tag.has_attr


def xiaoqu_detect(name):
	final_result = []
	xiaoqu_result = []
	xiaoqu_url = XIAOQU_HOUSE_URL.replace("*", name)
	# 获得小区
	response = request_url(xiaoqu_url)
	logging.debug(xiaoqu_url)
	soup = BeautifulSoup(response, "html.parser")
	list = soup.find_all("a", attrs={"class": "img", "data-el": "ershoufang", "data-bl": "list"})
	house_top = None
	for object in list:
		# 获得小区里面房子
		house_top, house_id = get_House(object['href'])
		house_top.count = HOUSECOUNT['Top']
		xiaoqu_result.extend(xiaoqu_children_detect(house_id))

	# print json.dumps(xiaoqu_result, default=lambda object: object.__dict__, ensure_ascii=False)
	# print json.dumps(house_top, default=lambda object: object.__dict__, ensure_ascii=False)

	xiaoqu_result.sort(key=lambda object: object.name)
	# print json.dumps(xiaoqu_result, default=lambda object: object.__dict__, ensure_ascii=False)

	key_group = groupby(xiaoqu_result, key=lambda object: object.name)

	for i, key in enumerate(key_group):
		if key[0] == name:
			continue
		if i == 0:
			house = xiaoqu_dict[key[0]]
			house.count = HOUSECOUNT['First']
			final_result.append(house)
		elif i == 1:
			house = xiaoqu_dict[key[0]]
			house.count = HOUSECOUNT['Second']
			final_result.append(house)
		elif i == 2:
			house = xiaoqu_dict[key[0]]
			house.count = HOUSECOUNT['Third']
			final_result.append(house)
		else:
			house = xiaoqu_dict[key[0]]
			final_result.append(house)

	return name, json.dumps(house_top, default=lambda x: x.__dict__, ensure_ascii=False), json.dumps(final_result,
																									 default=lambda
																										 x: x.__dict__,
																									 ensure_ascii=False)


def xiaoqu_children_detect(houseId):
	children_house = []
	json_response = request_url(RECOM_URL.replace("*", houseId))
	for object in json.loads(json_response)["data"]["recommend"]:
		content = request_url(object["viewUrl"])
		coordinate = re.search("resblockPosition:'(.*)'", content).group(1)
		houseName = re.search("resblockName:'(.*)'", content).group(1)
		house = House(coordinate.split(',')[0], coordinate.split(',')[1], houseName)
		xiaoqu_dict[houseName] = house
		children_house.append(house)
	return children_house


def get_House(url):
	content = request_url(url);
	coordinate = re.search("resblockPosition:'(.*)'", content).group(1)
	houseId = re.search(" houseId:'(.*)'", content).group(1)
	houseName = re.search("resblockName:'(.*)'", content).group(1)
	house = House(coordinate.split(',')[0], coordinate.split(',')[1], houseName)
	return house, houseId


if __name__ == '__main__':
	# 获取小区名称
	response = request_url(XIAOQU_URL)
	# while True:
	# 	next_page = get_xiaoquname(response)
	# 	logging.debug(next_page)
	# 	if not next_page:
	# 		break
	# 	response = request_url(next_page)

	next_page = get_xiaoquname(response)



	for name in xiaoqu_name:
		try:
			name, parent_json, children_json = xiaoqu_detect(name)
			save(name, parent_json, children_json)
		except Exception, e:
			logging.info(str(e))
			continue

# 获得房子名 by小区名称
# for name in xiaoqu_name:
# 	xiaoqu_url = XIAOQU_HOUSE_URL.replace("*", name)
# 	response = request_url(xiaoqu_url)
# 	house_url = get_house_by_xiaoqu(response)
# 	response = request_url(house_url)
# 	get_house_graphx(response)

# response = request_url("https://nj.lianjia.com/ershoufang/rs万达紫金明珠/")
# get_house_by_xiaoqu(response)
#
# response = request_url("https://nj.lianjia.com/ershoufang/103102480999.html")
# result_json = get_house_graphx(response)
# write(result_json)
