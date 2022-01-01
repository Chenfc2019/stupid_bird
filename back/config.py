#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：config.py
# @Author ：orange
# @Date ：2021/12/12 下午3:05

# 把配置文件放在back目录下

import os


class Config(object):
    """
    配置信息
    """
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY') or '0V_pAv1dOZqN_Y_Zf3eJ'
    '''
    生成随机字符串
    import secrets
    secrets.token_urlsafe(nbytes=15)
    '''
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    # 分页
    FLASKY_POSTS_PER_PAGE = 10
    # 上传图片
    UPLOADED_IMAGES_DEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/images')
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    # 邮件服务器设置
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.qq.com')
    # 163不支持STARTTLS
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '731319247@qq.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'clxlxcgsvbctbaij')
    MAIL_DEFAULT_SENDER = ('stupid_bird', os.getenv('MAIL_USERNAME', '731319247@qq.com'))
    # redis 配置
    REDIS_URL = "redis://:123@localhost:6379/0"
    # REDIS_URL = "redis://localhost:6379/0"

    def __init__(self):
        pass

    @staticmethod
    def init_app(app):
        pass

class MySQLConfig:
    MYSQL_USERNAME = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '123456')
    MYSQL_DB = os.getenv('MYSQL_DB')
    MYSQL_HOST = 'localhost:3306'
    MYSQL_CHARSET = 'utf8mb4'  # 为了支持 emoji 显示，需要设置为 utf8mb4 编码


class DevelopmentConfig(Config):
    DEBUG = True
    database = MySQLConfig.MYSQL_DB or 'myblog_dev'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MySQLConfig.MYSQL_USERNAME}:{MySQLConfig.MYSQL_PASSWORD}' \
                              f'@{MySQLConfig.MYSQL_HOST}/{database}?charset={MySQLConfig.MYSQL_CHARSET}'


class ProductionConfig(Config):
    database = MySQLConfig.MYSQL_DB or 'myblog_product'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MySQLConfig.MYSQL_USERNAME}:{MySQLConfig.MYSQL_PASSWORD}' \
                              f'@{MySQLConfig.MYSQL_HOST}/{database}?charset={MySQLConfig.MYSQL_CHARSET}'


env_config = {
    'dev': DevelopmentConfig,
    'product': ProductionConfig
}

