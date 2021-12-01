# create by cfc 2021/11/30 9:04 上午

from flask import jsonify
from flask_restful import Resource
from back.api_v1_0.errors import unauthorized_error, forbidden

from back.service.auth_ctrl import *
from . import api_bp, api


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


class Auth(Resource):
    """"""
    decorators = [basic_auth.login_required]
    def get(self):
        """
        /api/token
        """
        return jsonify({'hello': 'get token'})

    def post(self):
        """
        /api/sigin 接口
        """
        return jsonify({'hello': 'sigin'})


