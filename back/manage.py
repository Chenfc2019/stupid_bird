#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：manage.py
# @Author ：orange
# @Date ：2021/12/5 上午10:33


import os
from back import create_app

env = os.getenv('stupid_env')
print(f'running env: {env}')
app = create_app(env)

@app.route('/index')
def index():
    return 'hello'


if __name__ == '__main__':
    app.run()