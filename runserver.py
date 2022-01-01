#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：runserver.py
# @Author ：orange
# @Date ：2021/12/4 下午1:07

import os

from back import create_app, setting

app = create_app(os.getenv('FLASK_CONFIG', 'dev'))

if __name__ == '__main__':
    host_ip = setting.HOST_IP
    app.run(host=host_ip)  # TODO:此处需要写进环境变量