#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= flask-baidumap
@file= process_demo3
@author= wubingyu
@create_time= 2018/6/29 上午11:25
"""
from multiprocessing import Process, Pipe


def f(conn):
	conn.send(['hello'])
	conn.close()


def test():
	parent_conn, children_conn = Pipe()
	p = Process(target=f, args=(children_conn,))

	p.start()
	print parent_conn.recv()
	p.join()


if __name__ == '__main__':
	test()
