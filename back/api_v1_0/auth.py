# create by cfc 2021/11/30 9:04 上午

from flask import jsonify, g, request
from flask_restful import Resource
from back.api_v1_0.errors import unauthorized_error, forbidden

from back.service.auth_ctrl import *
from . import api_bp, api
from .base import BaseResource


@api_bp.before_request
@multi_auth.login_required
def before_request():
    """
    想要在API访问前加login_required监护。
    为了让api蓝本中的所有API都一次性加上监护，可以用before_request修饰器应用到整个蓝本
    :return:
    """
    if not g.current_user.is_anonymous and not g.current_user.confirmed:
        return forbidden('Unconfirmed account')


class Auth(BaseResource):
    """
    https://www.cnblogs.com/vovlie/p/4182814.html
    """
    decorators = [basic_auth.login_required]
    def get(self):
        """
        /api/token
        """
        args = request.json
        username = args.get('username')
        token = generate_auth_token(user_id=username)
        return self.return_json_data(data={'token': token.decode('utf-8')})

    def post(self):
        """
        /api/sigin 接口
        先走基础认证回调函数，验证用户名和密码，验证成功把用户信息存到g对象中
        """
        # user_id = g.user.id
        username = g.user.username
        token = generate_auth_token(username, expiration=60*60)
        if not token:
            return self.return_json_data(status=401, msg='authorized failed')
        data = {
            'username': g.user.username,
            'token': token
        }
        return self.return_json_data(msg='authorized success', data=data)



