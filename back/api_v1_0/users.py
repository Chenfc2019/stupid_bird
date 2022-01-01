#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：users.py
# @Author ：orange
# @Date ：2021/12/6 上午9:00

from .base import BaseResource
from flask import g, request
from back.service.auth_ctrl import *
from back.models import User


def abort_if_not_exist(user_id):
    """
    操作之前需要user存在，否则返回 404
    :param user_id:
    :return:
    """
    desc = 'The user {} not exist.'.format(user_id)
    user = User.query.get_or_404(user_id, description=desc)
    return user


class UserApi(BaseResource):
    @token_auth.login_required
    def get(self, user_id=None):
        """
        获取用户，需要token验证
        :return:
        """
        if user_id:
            user = abort_if_not_exist(user_id)
        else:
            user = g.user
        if not user:
            return self.return_json_data(status=400, msg='user not found', data='')
        ret_data = dict()
        ret_data['account'] = user.name
        ret_data['nickname'] = user.username
        # TODO:just for test
        ret_data['avatar'] = '/static/user/admin.png'
        ret_data['id'] = user.id
        ret_data['confirmed'] = user.confirmed
        return self.return_json_data(data=ret_data)

    def post(self):
        """
        注册用户
        :return:
        """
        param = request.json
        username = param.get('account')
        password = param.get('password')
        re_password = param.get('rePassword')
        email = param.get('email')
        # 参数验证
        if not all([username, password, re_password, email]):
            return self.return_json_data(status=400, msg='Missing arguments.')
        if password != re_password:
            return self.return_json_data(status=400, msg='Please confirm password has been set correctly.')
        if user_ctrl.username_exists(username):
            return self.return_json_data(status=400, msg='User name already exists,Please rename it.')
        if user_ctrl.email_exists(email):
            return self.return_json_data(status=400, msg='Email address already exists.')

        user = user_ctrl.new_user(username, password, email)
        # user_id = user.id
        # 用username来生成token
        username = user.username
        token = generate_auth_token(username, expiration=60 * 120)
        ret_data = dict()
        ret_data['token'] = token
        ret_data['username'] = username
        return self.return_json_data(data=ret_data)
