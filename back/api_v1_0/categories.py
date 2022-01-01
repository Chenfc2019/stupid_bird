#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：categories.py
# @Author ：orange
# @Date ：2021/12/13 下午10:08

# 分类相关的接口

from flask import request
from flask_restful import Resource
from back.api_v1_0.base import BaseResource
from back.service.categorie_ctrl import GetCategoryCtrl

category_getter = GetCategoryCtrl()


class CategoryApi(BaseResource):
    """
    避免重名，起名*Api
    """

    def __init__(self):
        self.response_obj = {'success': True, 'code': 0, 'data': None, 'msg': ''}

    def get(self, category_id=None):
        # 请求数据
        args = request.args
        if category_id:
            data = category_getter.posts_for_category(category_id)
            # self.response_obj['data'] = data
            return self.return_json_data(data=data)

        if args:
            return self.return_json_data(status=400, msg='获取数据失败')
        else:
            data = category_getter.show_categories()
            return self.return_json_data(data=data)
