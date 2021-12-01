# create by cfc 2021/12/1 9:49 下午

# -*- coding: utf-8 -*-

from flask import jsonify


# 定义几种常见的异常情况
def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


def unauthorized_error(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


def method_not_allowed(message):
    response = jsonify({'error': 'method not allowed', 'message': message})
    response.status_code = 405
    return response

