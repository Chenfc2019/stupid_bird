#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：__init__.py
# @Author ：orange
# @Date ：2021/11/28 下午8:35

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_uploads import configure_uploads, patch_request_class
from back.api_v1_0 import uploads, api_bp, api, auth
from back.api_v1_0.config import *
from back.utils.logger import register_logger
from back.utils.mail import mail
from back.utils.redis_util import redis_store
from back.models import *

# 设置跨域
cors = CORS(resources={r'/api/*': {'origin': '*'}})


def add_api():
    """
    添加api接口
    :return:
    """
    api.add_resource(auth.Auth, '/api/signin', '/api/token')
    pass


def add_blueprints(app):
    """
    注册蓝图
    :return:
    """
    app.register_blueprint(api_bp)


def create_app(config_name):
    app = Flask(__name__, static_folder='../dist/static', template_folder='../dist')
    # 加载配置信息
    app.config.from_object(env_config[config_name])
    env_config[config_name].init_app(app)
    # 注册日志
    register_logger(__name__)
    cors.init_app(app)
    db.init_app(app)
    # 数据库迁移工具，需要在db对象创建之后调用
    migrate = Migrate(app, db)
    configure_uploads(app, uploads.image_upload)
    mail.init_app(app)
    redis_store.init_app(app)
    # 防止上传文件过大
    patch_request_class(app, size=None)
    add_api()
    # 需要add_api()完成后init
    api.init_app(app)
    add_blueprints(app)
    return app
