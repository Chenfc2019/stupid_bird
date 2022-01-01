#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：setting.py
# @Author ：orange
# @Date ：2021/12/4 下午1:09


import os

# log
APP_LOG_FP = 'logs/app.log'

LIMIT_NEW_POST_COUNT = 5
LIMIT_HOT_POST_COUNT = 5
LIMIT_HOT_TAG_COUNT = 10
INITIAL_VIEW_COUNTS = 0
INITIAL_POST_IDENTIFIER = 20211227

# flask
FLASK_HOST = '0.0.0.0'
FLASK_PORT = '5000'
HOST_IP = os.getenv('FLASK_HOST', FLASK_HOST)

# re
RE_SYMBOL = r'[\,\，\.\。\?\？\:\：\'\‘\’\"\“\”\、\/\*\&\$\#\@\!\(\（\)\）\[\【\]\】\{\}\|\-"]'
RE_EXCLUDE_CHINESE = r'[A-Za-z0-9\!\%\[\]\,\。]'