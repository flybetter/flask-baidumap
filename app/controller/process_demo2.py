#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= flask-baidumap
@file= process_demo2
@author= wubingyu
@create_time= 2018/6/28 下午9:53
"""
from multiprocessing import Process
import time
import logging

logging.basicConfig(level=logging.DEBUG)


def profile(func):
	def wrapper(*args, **kwargs):
		start = time.time()
		func(*args, **kwargs)
		end = time.time()
		print 'COST: {}'.format(end - start)

	return wrapper


def fib(num):
	if num <= 2:
		return 1
	else:
		return fib(num - 1) + fib(num - 2)


@profile
def nomultiprocess():
	fib(35)
	fib(35)


@profile
def hasmultiprocess():
	jobs = []

	for _ in range(1):
		p = Process(target=fib, args=(25,))
		p.start()
		jobs.append(p)

	for p in jobs:
		p.join()


if __name__ == '__main__':
	hasmultiprocess()
	nomultiprocess()
