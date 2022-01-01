#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：base.py
# @Author ：orange
# @Date ：2021/12/6 上午9:06


# 定义继承自Resource的类，添加通用方法

from flask_restful import Resource
from flask import make_response, jsonify



class BaseResource(Resource):
    """
    定义一些通用的方法，让API中的类集成这个类
    """
    def return_json_data(self, status=200, msg='success', data='', **kwargs):
        """
        通用的返回统一数据格式的方法
        :param status:
        :param msg:
        :param data:
        :param kwargs:
        :return:
        """
        ret_obj = {
            'status': status,
            'msg': msg,
            'data': data
        }
        ret_obj.update(kwargs)
        return jsonify(ret_obj)

    def jsonify_with_args(self, data, code=200, *args):
        """
        返回json数据，同时修改返回状态码
        :param data:
        :param code:
        :param args:
        :return:
        """
        assert isinstance(data, dict)
        return make_response(jsonify(data), code, *args)


