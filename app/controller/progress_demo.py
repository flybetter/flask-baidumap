#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= flask-baidumap
@file= progress_demo
@author= wubingyu
@create_time= 2018/6/28 下午3:54
"""
from multiprocessing import Process, Queue, Pool
import os
import time, random
import itertools
from app.controller.util import get_xiaoqu_name


def producer(q, list):
	for object in list:
		print object
		q.put(object)
		time.sleep(random.random() * 10)


def consumer(q):
	while True:
		object = q.get(True)
		print object


def long_time_task(name):
	print('Run task %s (%s)...' % (name, os.getpid()))
	q.put(name)
	start = time.time()
	time.sleep(random.random() * 3)
	end = time.time()
	print('Task %s runs %0.2f seconds.' % (name, (end - start)))


if __name__ == '__main__':
	q=Queue()
	print('Parent process %s.' % os.getpid())
	list = get_xiaoqu_name()
	p = Pool(4)
	for name in list:
		print name
		p.apply_async(long_time_task, args=(name,q))
	print('Waiting for all subprocesses done...')
	p.close()
	p.join()
	print('All subprocesses done.')

# if __name__ == '__main__':
# 	print('Parent process %s.' % os.getpid())
# 	p = Pool(4)
# 	for i in range(5):
# 		p.apply_async(producer, args=(i, itertools.islice(list, i * 100, (i + 1) * 100)))
# 	print('Waiting for all subprocesses done...')
# 	p.close()
# 	p.join()
# 	print('All subprocesses done.')
#
# 	q = Queue()
#
# 	p = Pool(4)
# 	list = get_xiaoqu_name()
# 	for i in range(2):
# 		print itertools.islice(list, i * 100, (i + 1) * 100)
# 		p.apply_async(producer, args=(q, itertools.islice(list, i * 100, (i + 1) * 100)))
#
# 	p.close()
# 	pr = Process(target=consumer, args=(q,))
# 	pr.start()
# 	p.join()
# 	pr.terminate()
