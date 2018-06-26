#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= flask-baidumap
@file= House
@author= wubingyu
@create_time= 2018/6/22 下午4:29
"""


class House:
	def __init__(self, lng, lat, name):
		self.lng = float(lng)
		self.lat = float(lat)
		self.name = name
		self.count = 50

	@property
	def count(self):
		return self.count

	@count.setter
	def count(self, count):
		self.count = count

	@property
	def name(self):
		return self.name

	@name.setter
	def name(self, name):
		self.name = name

	def __eq__(self, other):
		if isinstance(other, House):
			return self.lat == other.lat and self.lng == other.lng
		else:
			return False

	def __ne__(self, other):
		return not self.__eq__(other)

	def __hash__(self):
		return hash(self.count) + hash(self.lat) + hash(self.lng) + hash(self.name)
