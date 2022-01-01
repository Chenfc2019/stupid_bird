#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：comments.py
# @Author ：orange
# @Date ：2021/12/29 下午10:13


"""
定义所有跟评论相关的api接口
"""

from flask import jsonify, request
from .base import BaseResource


class Comments(BaseResource):
    """
    获取文章评论，具体功能还没实现
    """

    def __init__(self):
        self.response_obj = {'success': True, 'code': 0, 'data': None, 'msg': ''}

    def get(self, comment_id=None):
        # 请求数据
        if comment_id:
            pass
        else:
            args = request.args
            if args:
                post_id = args.get('post_id')
                if post_id:
                    data = None
                    self.response_obj['data'] = data
            else:
                self.response_obj['code'] = 1
                self.response_obj['success'] = False
                self.response_obj['msg'] = 'Args required.'
        return jsonify(self.response_obj)