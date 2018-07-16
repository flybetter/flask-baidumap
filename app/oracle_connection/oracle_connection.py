#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= flask-baidumap
@file= oracle_connection
@author= wubingyu
@create_time= 2018/7/12 下午5:17
"""
import cx_Oracle
import os

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

HOST = 'app/app@202.102.83.165/app'


def oracle_connection(host=HOST):
	connection = cx_Oracle.connect(host)
	cursor = connection.cursor()
	return connection, cursor


def get_data(blockname):
	sql = "select s.id,s.PRICE,s.BUILDAREA,s.FLOOR,s.TOTALFLOOR,s.FITMENT,s.BUILDYEAR,s.BLOCKSHOWNAME,s.DISTRICT from dwb_ras_block_nj b,dwb_ras_sell_nj_all s  where b.BLOCKNAME='%s' and b.id=s.BLOCKID and ROWNUM=1" % blockname
	connection, cursor = oracle_connection()
	cursor.execute(sql)
	data = cursor.fetchone()
	oracle_close(connection, cursor)
	return data


def oracle_close(connection, cursor):
	cursor.close()
	connection.close()


if __name__ == '__main__':
	print get_data('苏宁名都汇')
