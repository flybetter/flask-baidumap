#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= flask-baidumap
@file= process_demo4
@author= wubingyu
@create_time= 2018/6/30 上午10:54
"""
from multiprocessing import Process, Pipe
from itertools import izip


# def fib(num):
# 	if num <= 2:
# 		return 1
# 	else:
# 		return fib(num - 1) + fib(num - 2)
#
#
# def spawn(f):
# 	def func(pipe, item):
# 		pipe.send(f(item))
# 		pipe.close()
#
# 	return func
#
#
# def parmap(f, items):
# 	pipe = [Pipe() for _ in items]
# 	process = [Process(target=spawn(f), args=(child, item)) for item, (parent, child) in izip(items, pipe)]
# 	[p.start() for p in process]
# 	[p.join() for p in process]
# 	return [parent.recv() for (parent, child) in pipe]
#
#
# class CalculateFib(object):
# 	@classmethod
# 	def fib(num):
# 		if num <= 2:
# 			return 1
# 		else:
# 			return fib(num - 1) + fib(num - 2)
#
# 	def parmap_run(self):
# 		print parmap(self.fib, [35] * 2)
#
#
# cl = CalculateFib()
# cl.parmap_run()


def spawn(f):
	def func(pipe, item):
		pipe.send(f(item))
		pipe.close()

	return func


def parmap(f, items):
	pipe = [Pipe() for _ in items]
	process = [Process(target=spawn(f), args=(child, item)) for (item, (parent, child)) in izip(items, pipe)]
	[p.start() for p in process]
	[p.join() for p in process]

	return [parent.recv() for (parent, child) in pipe]


class CaluableFib(object):

	def fib(self, num):
		if num <= 2:
			return 1
		else:
			return self.fib(num - 1) + self.fib(num - 2)

	def parmap_run(self):
		print parmap(self.fib, [35] * 2)


c = CaluableFib()
c.parmap_run()
