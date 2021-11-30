#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：__init__.py.py
# @Author ：orange
# @Date ：2021/11/28 下午8:32

from flask import Blueprint
from flask_restful import Api


api_bp = Blueprint('api', __name__)
api = Api()