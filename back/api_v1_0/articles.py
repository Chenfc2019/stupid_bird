#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：articles.py
# @Author ：orange
# @Date ：2021/12/6 下午7:43

# 文章相关的接口
from flask import request, current_app, jsonify, g
from . import api
from .errors import forbidden
from back.service.auth_ctrl import token_auth
from back.service import MakeupPost
from .base import BaseResource
from back.service.article_ctrl import article_get_ctrl, article_post_ctrl, article_put_ctrl, article_patch_ctrl, article_del_ctrl
from back.models import Article


post_maker = MakeupPost()


def abort_if_not_exist(post_id):
    """
    操作之前需要保证操作的文章存在，否则返回 404
    :param post_id:
    :return:
    """
    desc = 'The post {} not exist.'.format(post_id)
    post = Article.query.get_or_404(post_id, description=desc)
    return post


class ArticleApi(BaseResource):
    def __init__(self):
        self.response_obj = {'success': True, 'code': 0, 'data': None, 'msg': 'Get data ok.'}

    def get(self):
        """
        获取文章列表（分页展示及条件查询）
        多级资源使用查询字符串，语义更清晰
        获取某个作者的某一类文章：
        GET /authors/12/categories/2
        GET /authors/12?categories=2
        :return:
        """
        # get请求获取参数
        args = request.args
        if args:
            # ?new=true
            new = args.get('new', False, type=bool)
            # ?hot=true
            hot = args.get('hot', False, type=bool)
            # ?order = asc
            order = args.get('order')  # 默认降序
            order_by_desc = order and order == 'desc' if order else True  # 暂时默认是降序
            # ?limit=5
            limit_count = int(args.get('limit')) if args.get('limit') else None
            # 最新最热走limit逻辑，截取而不是分页
            page, per_page = (None,) * 2
            order_by = ''
            # 如果是最新或者最热，表示order_by已经传值，不能重新赋值！
            if not (new or hot):
                # ?page=1&per_page=10
                page = args.get('page', 1, type=int)
                per_page = args.get('per_page', type=int) or current_app.config['FLASKY_POSTS_PER_PAGE']
                # ?order_by=create_date
                order_by = args.get('order_by', 'create_date', type=str)
            query_by = args.get('query_by', type=str) or None
            category_id = args.get('categories', type=int) or None
            tag_id = args.get('tags', type=int) or None
            year = args.get('year', type=int) or None
            month = args.get('month', type=int) or None
            # 关键字查询
            query_data = article_get_ctrl.get_post_detail_by_args(query_by, order_by, category_id, tag_id, year, month, new, hot,
                                                             order_by_desc=order_by_desc)

            # result_data, count = article_get_ctrl.get_article_detail_by_args(args)

            if query_data:
                # 因为分页要调api，为防止循环引用，所以此处放在内部
                # ?page=1&per_page=10?order_by=name&order=asc
                if all([page, per_page]):
                    pagination = article_get_ctrl.make_paginate(query_data, page=page, per_page=per_page)
                    prev_page, next_page, data = self.parse_pagination(pagination, page=page, per_page=per_page,
                                                                       order_by=order_by, order=order_by_desc,
                                                                       query_by=query_by, categories=category_id,
                                                                       tags=tag_id, limit=limit_count)
                    self.response_obj['data'] = data
                    self.response_obj['prev'] = prev_page
                    self.response_obj['next'] = next_page
                    self.response_obj['total'] = pagination.total
                else:
                    data = article_get_ctrl.make_limit(query_data, limit_count)
                    self.response_obj['data'] = data
                return jsonify(self.response_obj)
        else:
            return self.return_json_data(status=400, msg='缺少参数')

    def post(self):
        """
        创建文章
        """
        '''
        {'id': '', 'title': '多喝热水', 'summary': '爱是什么？', 'category': '生活', 'dynamicTags': ['恋爱', '生活'],
         'tags': ['test', '原创', 'Python', '影评', '阅读', 'MySQL', '推荐'],
         'body': {'content': '除了清明都是情人节', 'contentHtml': '<p>除了清明都是情人节</p>\n'}}
        '''
        json_data = request.json
        # 用户最终提交的
        post_tags = json_data.get('dynamicTags', [])
        category_name = json_data.get('category')
        # TODO: 默认取前200个字符?
        post_summary = json_data.get('summary')
        author_id = json_data.get('authorId')
        post_title = json_data.get('title')
        raw_slug = json_data.get('slug')
        post_weight = int(json_data.get('weight')) or 0
        # visable_tags = json_data.get('tags')
        post_body = json_data.get('body')
        content, content_html = (None,) * 2
        if post_body:
            content = post_body.get('content')
            content_html = post_body.get('contentHtml')
        if not all([post_title, post_summary, category_name, content, content_html]):
            self.response_obj['code'] = 1
            self.response_obj['success'] = False
            self.response_obj['msg'] = 'Not enough args.'
            return self.jsonify_with_args(self.response_obj, 400)
        else:
            new_post = article_post_ctrl.new_post(author_id, category_name, post_summary, content_html, content,
                                               post_title, raw_slug, weight=post_weight, post_tags=post_tags)
            post_id = new_post.post_id
            identifier = new_post.identifier
            slug = new_post.slug
            data = {'articleId': post_id, 'identifier': identifier, 'slug': slug}
            self.response_obj['data'] = data
            # 服务器为新资源指派URL，并在响应的Location首部中返回
            return self.jsonify_with_args(self.response_obj, 201, {
                'Location': api.url_for(ArticleDetail, post_id=post_id, _external=True)})

    @staticmethod
    def parse_pagination(pagination, page=None, per_page=None, order_by=None, order='desc', query_by=None,
                         categories=None, tags=None, limit=None):
        _posts_list = pagination.items
        prev_page = None
        # https://stackoverflow.com/questions/24223628/how-do-i-use-flask-url-for-with-flask-restful
        # TODO: category tag 测试
        if pagination.has_prev:
            prev_page = api.url_for(ArticleApi, page=page - 1, per_page=per_page, order_by=order_by, sort=order,
                                    query_by=query_by, categories=categories, tags=tags, limit=limit, _external=True)
        next_page = None
        if pagination.has_next:
            next_page = api.url_for(ArticleApi, page=page + 1, per_page=per_page, order_by=order_by, sort=order,
                                    query_by=query_by, categories=categories, tags=tags, limit=limit, _external=True)
        data = post_maker.makeup_post_item_for_index(_posts_list)
        return prev_page, next_page, data

    @staticmethod
    def parse_pagination_new(result_data, count, page=None, per_page=None, order_by=None, order='desc', query_by=None,
                         categories=None, tags=None, limit=None):
        prev_page = None
        # https://stackoverflow.com/questions/24223628/how-do-i-use-flask-url-for-with-flask-restful
        # TODO: category tag 测试
        if page > 1:
            prev_page = api.url_for(ArticleApi, page=page - 1, per_page=per_page, order_by=order_by, sort=order,
                                    query_by=query_by, categories=categories, tags=tags, limit=limit, _external=True)
        next_page = None
        if page * per_page < count:
            next_page = api.url_for(ArticleApi, page=page + 1, per_page=per_page, order_by=order_by, sort=order,
                                    query_by=query_by, categories=categories, tags=tags, limit=limit, _external=True)
        data = post_maker.makeup_post_item_for_index(result_data)
        return prev_page, next_page, data


class IdentifyPostDetail(BaseResource):
    """
    单个文章处理的 API
    """

    def __init__(self):
        self.response_obj = {'success': True, 'code': 0, 'data': None, 'msg': ''}

    def get(self):
        """
        获得指定 identifier 对应的文章
        :return: json,
        """
        identifier = request.args.get('identifier')
        post_id = article_post_ctrl.get_post_id_by_identifier(identifier)
        post = abort_if_not_exist(post_id)
        post_info = article_get_ctrl.post_detail(post)
        self.response_obj['data'] = post_info
        return jsonify(self.response_obj)

    def patch(self, identifier):
        """
        更新文章阅读数操作
        :param identifier:
        :return:
        """
        data = None
        post_id = article_post_ctrl.get_post_id_by_identifier(identifier)
        post = abort_if_not_exist(post_id)
        args = request.args
        patch_count = args.get('field')
        if patch_count == 'count':
            new_count = article_patch_ctrl.add_view_count(post_id)
            if new_count:
                data = {'count': new_count}

        self.response_obj['data'] = data
        return jsonify(self.response_obj)


class ArticleDetail(BaseResource):
    """
    单个文章处理的 API
    """

    def __init__(self):
        self.response_obj = {'success': True, 'code': 0, 'data': None, 'msg': ''}

    def get(self, post_id):
        """
        获得指定ID对应的文章
        :param post_id: int,
        :param identifier: int,
        :return: json,
        """
        post = abort_if_not_exist(post_id)
        post_info = article_get_ctrl.post_detail(post)
        self.response_obj['data'] = post_info
        return jsonify(self.response_obj)

    @token_auth.login_required
    def put(self, post_id):
        """
        更新指定文章
        注意：必须是原作者，TODO:管理员可以折叠或隐藏？后期开发
        :param post_id:
        :return:
        """
        abort_if_not_exist(post_id)
        json_data = request.json
        current_user_id = json_data.get('authorId')
        if g.user.id != current_user_id:  # or  g.current_user.can(Permission.ADMINISTER):
            return forbidden('Insufficient permissions')
        post_tags = json_data.get('dynamicTags', [])
        category_name = json_data.get('category')
        post_summary = json_data.get('summary')
        post_title = json_data.get('title')
        post_weight = int(json_data.get('weight')) or 0
        # visable_tags = json_data.get('tags')
        post_body = json_data.get('body')
        content, content_html = (None,) * 2
        if post_body:
            content = post_body.get('content')
            content_html = post_body.get('contentHtml')
        if not all([post_title, post_summary, category_name, content, content_html]):
            self.response_obj['code'] = 1
            self.response_obj['success'] = False
            self.response_obj['msg'] = 'Not enough args.'
            return self.return_json_data(status=400, msg='failed', data='缺少参数')
            # return jsonify_with_args(self.response_obj, 400)
        else:
            post_obj = article_put_ctrl.update_post(post_id, current_user_id, category_name, post_summary, content_html,
                                                content,
                                                post_title,
                                                weight=post_weight, post_tags=post_tags)
            post_id = post_obj.post_id
            identifier = post_obj.identifier
            slug = post_obj.slug
            data = {'articleId': post_id, 'identifier': identifier, 'slug': slug}
            self.response_obj['data'] = data
            return self.return_json_data(data=self.response_obj, code=200, Location=api.url_for(ArticleDetail, post_id=post_id, _external=True))
            # return jsonify_with_args(self.response_obj, 200, {
            #     'Location': api.url_for(ArticleDetail, post_id=post_id, _external=True)})

    def patch(self, post_id):
        """
        更新文章部分信息操作
        :param post_id:
        :return:
        """
        data = None
        post = abort_if_not_exist(post_id)
        args = request.args
        patch_count = args.get('field')
        if patch_count == 'count':
            new_count = article_patch_ctrl.add_view_count(post_id)
            if new_count:
                data = {'count': new_count}

        self.response_obj['data'] = data
        return jsonify(self.response_obj)

    @token_auth.login_required
    def delete(self, post_id):
        """
        删除指定文章
        :param post_id: int
        :return:json
        """
        abort_if_not_exist(post_id)
        json_data = request.json
        author_id = json_data.get('authorId')
        # if g.current_user != post.author and not g.current_user.can(Permission.ADMINISTER):
        if g.user.id != author_id:  # TODO:对于普通用户来说，删除应该是数据库deleted字段置1，除了用户本人，管理员应该也可以删除
            return forbidden('Insufficient permissions')
        else:
            post_id = article_del_ctrl.delete_post(post_id)
            self.response_obj['msg'] = f'Delete post {post_id} success.'
        return self.return_json_data(data=self.response_obj, code=204)
        # return jsonify_with_args(self.response_obj, 204)




