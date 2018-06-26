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

RANK = {"TOP": 1, "Second": 2}

result = []

HOUSECOUNT = {"First": 90, "Second": 10}


# https://nj.lianjia.com/ershoufang/rs万达紫金明珠/


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
	# logging.debug(content)
	soup = BeautifulSoup(content, "html.parser")
	list = soup.find_all("a", attrs={"class": "img", "data-log_index": "1", "data-el": "ershoufang", "data-bl": "list"})
	return list[0]["href"]


def get_house_graphx(content):
	coordinate = re.search("resblockPosition:'(.*)'", content).group(1)
	houseId = re.search(" houseId:'(.*)'", content).group(1)
	logging.debug("coordinate:" + coordinate + " houseId:" + houseId)
	house = House(coordinate.split(',')[0], coordinate.split(',')[1], HOUSECOUNT['First'])
	result.append(house)
	json_response = request_url(RECOM_URL.replace("*", houseId))
	for object in json.loads(json_response)["data"]["recommend"]:
		second_content = request_url(object["viewUrl"])
		coordinate = re.search("resblockPosition:'(.*)'", second_content).group(1)
		house = House(coordinate.split(',')[0], coordinate.split(',')[1], HOUSECOUNT['Second'])
		result.append(house)


# final_result = list(set(result))
# return json.dumps(final_result, default=lambda object: object.__dict__)


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


# resblockName:'万达紫金明珠',
# isRemove:'0',
# defaultImg:'https://s1.ljcdn.com/feroot/pc/asset/img/blank.gif?_v=20180621185149',
# defaultBrokerIcon:'https://s1.ljcdn.com/feroot/pc/asset/img/blank.gif?_v=20180621185149',
# resblockPosition:'118.86612779808,32.021330008158',
# cityId:'320100',
# changedate:[1, 3, 4, 5, 3]


if __name__ == '__main__':
	# 获取小区名称
	response = request_url(XIAOQU_URL)
	while True:
		next_page = get_xiaoquname(response)
		logging.debug(next_page)
		if not next_page:
			break
		response = request_url(next_page)

	# 获得房子名 by小区名称
	for name in xiaoqu_name:
		xiaoqu_url = XIAOQU_HOUSE_URL.replace("*", name)
		response = request_url(xiaoqu_url)
		house_url = get_house_by_xiaoqu(response)
		response = request_url(house_url)
		get_house_graphx(response)

	write()

# response = request_url("https://nj.lianjia.com/ershoufang/rs万达紫金明珠/")
# get_house_by_xiaoqu(response)
#
# response = request_url("https://nj.lianjia.com/ershoufang/103102480999.html")
# result_json = get_house_graphx(response)
# write(result_json)
