#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= flask-baidumap
@file= setup
@author= wubingyu
@create_time= 2018/6/29 上午9:34
"""
from setuptools import setup

setup(
	name='flask-baidumap',
	package='app',
	include_package_data=True,
	install_requires=[
		'beautifulsoup4',
		'certifi',
		'chardet',
		'click',
		'Flask',
		'idna',
		'itsdangerous',
		'Jinja2',
		'MarkupSafe',
		'PyMySQL',
		'requests',
		'urllib3',
		'Werkzeug'
	],
)
