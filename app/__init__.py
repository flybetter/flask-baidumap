#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= flask-baidumap
@file= __init__.py
@author= wubingyu
@create_time= 2018/6/22 上午10:27
"""
from flask import Flask

app = Flask(__name__)

from app.controller import baidu
