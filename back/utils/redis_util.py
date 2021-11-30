# create by cfc 2021/11/30 9:01 上午

from flask_redis import FlaskRedis
from redis import StrictRedis

# 这里需要将redis的配置信息加载到config
# https://pypi.org/project/flask-redis/0.1.0/

redis_store = FlaskRedis.from_custom_provider(StrictRedis)