#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：db_util.py
# @Author ：orange
# @Date ：2021/12/11 上午10:54

# 执行原生SQL的工具
# https://stackoverflow.com/questions/34322471/sqlalchemy-engine-connection-and-session-difference
# http://sunnyingit.github.io/book/section_python/SQLalchemy-session.html

import os
from sqlalchemy.sql import text
from sqlalchemy import create_engine
from back.api_v1_0.config import *

# 有三种方法可以使用原生SQL
# 1. engine.execute(select([table]))
# 2. connection.execute(select([table]))
# 3. sion.execute(select([table]))
# 直接执行——使用Engine.execute()或Connection.execute()
# 使用会话——高效地将事务作为单个工作单元处理


if os.getenv('stupid_bird', 'dev'):
    __setting = env_config.get('dev')
else:
    __setting = env_config.get('product')

# 执行原生SQL的数据库引擎
engine = create_engine(
    __setting.SQLALCHEMY_DATABASE_URI,
    pool_size=5,  # 连接池的大小，0表示连接数无限制
    pool_recycle=30,  # 连接池回收连接的时间，如果设置为-1，表示没有no timeout, 注意，mysql会自动断开超过8小时的连接，所以sqlalchemy沿用被mysql断开的连接会抛出MySQL has gone away
    max_overflow=5,  # 连接池中允许‘溢出’的连接个数，如果设置为-1，表示连接池中可以创建任意数量的连接
    pool_timeout=30,  # 在连接池获取一个空闲连接等待的时间
    echo=True  # 如果设置True, Engine将会记录所有的日志，日志默认会输出到sys.stdout
)


def sql_get_data(sql_text: str = '', args: dict = {}) -> list:
    if not sql_text:
        return []
    sql_text = text(sql_text)
    # get connection
    connection = engine.connect()
    result = connection.execute(sql_text, args)
    res_data = result.fetchall()
    return_list = []
    for info in res_data:
        # info是一个RowProxy对象，从中可以提取到字段和数值信息
        temp = dict(zip(info._keymap.keys(), info._row))
        return_list.append(temp)
    # 下一步，加参数和返回一个列表嵌套字典的数据结构
    connection.close()
    return return_list




