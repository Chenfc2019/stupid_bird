#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：runserver.py
# @Author ：orange
# @Date ：2021/12/4 下午1:07

import os

from back import create_app, setting

env = os.getenv('stupid_env', 'dev')
print(f'running env: {env}')
app = create_app(env)


@app.route('/index')
def index():
    return 'hello'


if __name__ == '__main__':
    host_ip = setting.HOST_IP
    app.run(host=host_ip)  # TODO:此处需要写进环境变量