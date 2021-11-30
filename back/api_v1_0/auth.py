# create by cfc 2021/11/30 9:04 上午

from flask import jsonify
from flask_restful import Resource

class Auth(Resource):
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


