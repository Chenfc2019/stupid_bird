#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：archives.py
# @Author ：orange
# @Date ：2021/12/9 下午11:11

from flask import jsonify, request
from .base import BaseResource

from back.service.archive_ctrl import GetArchiveCtrl
from back.utils.db_util import sql_get_data

Archives_getter = GetArchiveCtrl()


class Archives(BaseResource):
    """
    文章归档
    """
    def get(self):
        # 请求数据
        order_desc = True
        args = request.args
        if args:
            order = args.get('order')
            # 默认降序，如果传值，则判断传值是否为desc,否? >> False
            order_desc = order and order == 'desc'
        sql_get_data(sql_text='select * from mb_user where username=:username;', args={'username': 'orange'})
        data = Archives_getter.extract_post_with_year_and_month(order_desc)

        return self.return_json_data(data=data)
