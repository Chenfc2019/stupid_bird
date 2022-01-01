#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：tags.py
# @Author ：orange
# @Date ：2021/12/9 上午8:18

# 标签相关的接口

from .base import BaseResource
from flask import jsonify, request, current_app
from flask_restful import Resource

from back import setting
from back.service.tag_ctrl import GetTagCtrl
from back.models import Tag

tag_getter = GetTagCtrl()


class TagApi(BaseResource):
    def get(self, tag_id=None):
        args = request.args
        query_by = args.get('query', None, type=str)
        order_by = args.get('order_by', 'id', type=str)
        order = args.get('order')  # 默认降序
        order_by_desc = order and order == 'desc' if order else True
        query_key, limit_count = (None,) * 2
        # 最新最热走limit逻辑，截取而不是分页 TODO: 标签暂时应该没有这个必要
        page, per_page = (None,) * 2
        if args.get('limit') and args['limit']:
            limit_count = int(args.get('limit'))
        hot = args.get('hot', False, type=bool)
        if tag_id:  # 查单个
            # /api/tags/id
            query_key = tag_id
            query_by = 'tag_id'     # 只传id时给默认值

        elif not hot:
            # TODO:默认按照id排，后续可以添加按照名字排（index >> name）
            order_by = args.get('order_by', 'id', type=str)
            # **注意**:args这里获取参数最好用dict.get() 而不是dict['key'],否则可能导致出错而程序不报错！！！
            query_key = args.get('name') and args['name'] or args.get('id') and args['id']

        else:
            # 总数少于设定值则全返回，否则返回设定值
            limit_count = Tag.query.count() if Tag.query.count() < setting.LIMIT_HOT_TAG_COUNT else \
                setting.LIMIT_HOT_TAG_COUNT
        if not args:
            # 没有请求参数，则返回全部
            limit_count = None
        data = tag_getter.get_tag_detail_by_args(query_key, query_by=query_by, order_by=order_by, hot=hot,
                                                 order_by_desc=order_by_desc,
                                                 limit_count=limit_count)
        # response_obj = dict()
        if data:
            # response_obj['data'] = data
            # response_obj['total'] = len(data)
            return self.return_json_data(data=data, total=len(data))
        else:
            # 数据为空，还没来得及初始化！
            return self.return_json_data(status=400, msg='未查询到数据')