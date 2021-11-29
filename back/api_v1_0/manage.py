#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：manage.py
# @Author ：orange
# @Date ：2021/11/29 下午11:48


from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
import redis
import os

from config import *


# class Config(object):
#     """
#     配置信息
#     """
#     DEBUG = True
#     SECRET_KEY = os.getenv('SECRET_KEY') or '0V_pAv1dOZqN_Y_Zf3eJ'
#     '''
#     生成随机字符串
#     import secrets
#     secrets.token_urlsafe(nbytes=15)
#     '''
#     SQLALCHEMY_COMMIT_ON_TEARDOWN = True
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SQLALCHEMY_RECORD_QUERIES = True
#     # 分页
#     FLASKY_POSTS_PER_PAGE = 10
#     # 上传图片
#     UPLOADED_IMAGES_DEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/images')
#     MAX_CONTENT_LENGTH = 10 * 1024 * 1024
#     # 邮件服务器设置
#     MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.qq.com')
#     # 163不支持STARTTLS
#     MAIL_PORT = 465
#     MAIL_USE_SSL = True
#     MAIL_USERNAME = os.getenv('MAIL_USERNAME', '731319247@qq.com')
#     MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'clxlxcgsvbctbaij')
#     MAIL_DEFAULT_SENDER = ('stupid_bird', os.getenv('MAIL_USERNAME', '731319247@qq.com'))
#     # redis 配置
#     # REDIS_URL = "redis://:123@localhost:6379/0"
#     REDIS_URL = "redis://localhost:6379/0"

app = Flask(__name__)

app.config.from_object(Config)

# 创建数据库
db = SQLAlchemy(app)

# 创建Redis链接对象
redis_store = redis.StrictRedis(host=Config.REDIS_URL, port=6379)

api = Api(app)

class User(Resource):
    def get(self, id):
        print('user_id: ', id)
        return jsonify({'user': 'hello'})


api.add_resource(User, '/users/<int:id>', endpoint='user')

@app.route('/index')
def index():
    return 'hello'

if __name__ == '__main__':
    app.run()