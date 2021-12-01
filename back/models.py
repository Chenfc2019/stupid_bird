# create by cfc 2021/11/30 8:59 上午

from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from passlib.apps import custom_app_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """
    用户表结构
    """
    __tablename__ = 'mb_user'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, comment='主键')
    # 因为有用户名登录选项，所以此处必须唯一
    username = db.Column(db.String(64), index=True, unique=True, comment='用户名')
    name = db.Column(db.String(32), comment='真实姓名')
    password = db.Column(db.String(128), comment='密码，加密保存')
    email = db.Column(db.String(120), index=True, unique=True, comment='注册邮箱')
    location = db.Column(db.String(64), comment='居住地')
    slogan = db.Column(db.String(64), server_default='就命运而言，休论公道。', comment='Slogan')
    create_date = db.Column(db.DateTime(), default=datetime.utcnow, comment='用户创建时间')
    last_login = db.Column(db.DateTime(), default=datetime.utcnow, comment='最近登录时间')
    confirmed = db.Column(db.Boolean, default=False, comment='注册确认')
    avatar_hash = db.Column(db.String(32), comment='头像')
    articles = db.relationship('Article')

    def __repr__(self):
        return '<User %r>' % self.username

    def hash_password(self, password):
        """
        明文密码哈希加密
        :param password:
        :return:
        """
        self.password = custom_app_context.encrypt(password)
        return self.password

    def verify_password(self, password):
        """
        验证密码
        :param password:
        :return:
        """
        return custom_app_context.verify(password, self.password)

    def generate_token(self, expires_time=60*60):
        """
        生成授权token
        :param expires_time:token过期时间
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'], expires_time)
        return s.dumps({'id': self.id})

    def verify_auth_token(self, token):
        """
        token验证
        :return:
        """
        # 解析token，返回用户信息
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception as e:
            return None
        user_id = data.get('id')
        user = User.query().get(user_id)
        return user
