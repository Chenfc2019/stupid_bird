# create by cfc 2021/12/1 9:23 下午

import hashlib
from flask import current_app, g
from sqlalchemy import or_
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth

from back.models import db, User

# 基础认证
basic_auth = HTTPBasicAuth()
# token认证
token_auth = HTTPTokenAuth()
# 混合认证（一个满足即可）
multi_auth = MultiAuth(basic_auth, token_auth)


@basic_auth.verify_password
def verify_password(account, password):
    """
    基础认证回调函数，验证用户名和密码
    :param account:账号（用户名|邮箱）
    :param password:密码
    :return:
    """
    if not all((account, password)):
        return False
    else:
        user = User.query.filter(or_(User.username == account, User.email == account)).first()
        if (not user) or (not user.verify_password(password)):
            return False
        # user对像会被存储到Flask的g对象中
        g.user = user
        return True


def generate_auth_token(user_id, expiration=60*30):  # TODO:与models-User重复
    """
    生成含有user_id的token，有效时间30min  >> 30*60
    :param user_id:
    :param expiration:
    :return:
    """
    s = Serializer(current_app.config['SECRET_KEY'], expiration)
    token = s.dumps({'id': user_id}).decode('utf-8')
    return token


@token_auth.verify_token
def verify_token(token):
    """
    token认证
    :param token:
    :return:
    """
    g.user = None
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None  # valid token, but expired
    except BadSignature:
        return None  # invalid token
    username = data.get('id')
    if data and username:
        # token验证通过，则把user信息保存到g对象中，别的地方就可以直接用了
        user = User.query.filter(or_(User.username == username, User.email == username)).one_or_none()
        g.user = user
        return True
    return False


class UserCtrl():

    @staticmethod
    def email_exists(email):
        return User.query.filter_by(email=email).one_or_none()

    @staticmethod
    def username_exists(username):
        return User.query.filter_by(username=username).one_or_none()

    @staticmethod
    def new_user(username, password, email):
        """
        创建新用户
        :param username: str,用户名
        :param password: str,密码
        :param email: str,邮箱
        :return:
        """
        user = User(email=email, username=username)
        hash_pw = user.hash_password(password)
        user.password = hash_pw
        db.session.add(user)
        db.session.commit()
        return user

    # @staticmethod
    # def new_password(email, password):
    #     """
    #     修改密码
    #     :param password: str,密码
    #     :param email: str,邮箱
    #     :return:
    #     """
    #     user = User.query.filter_by(email=email).one_or_none()
    #     if user:
    #         new_pw = user.hash_password(password)
    #         user.password = new_pw
    #         db.session.add(user)
    #         db.session.commit()
    #     return user
    #
    # @staticmethod
    # def gen_captcha():
    #     return captcha_obj.shuffle()
    #
    # @staticmethod
    # def makeup_send_reset_pw_mail(req_ip, captcha):
    #     """
    #
    #     :param req_ip:
    #     :param captcha:
    #     :return:
    #     """
    #     email_data = dict()
    #     _subject = '重设别院牧志帐号密码'
    #     _body = f'''
    #         已收到你的密码重设要求，请输入验证码：{captcha}，该验证码 {setting.TEMPORARY_PW_EXPIRE_MINUTES} 分钟内有效。
    #         本次请求者IP为：{req_ip} ，若非您本人操作，请及时修改登录密码，以保证账户安全。
    #
    #         感谢对 别院牧志 的支持，再次希望你在 别院牧志 的体验有益和愉快。
    #
    #         -- 别院牧志
    #
    #         (这是一封自动产生的 email ，请勿回复。)
    #     '''
    #     email_data['subject'] = _subject
    #     email_data['body'] = _body
    #     return email_data
    #
    # def send_reset_pw_mail(self, req_ip, captcha, receiver):
    #     """
    #     同步发送邮件
    #     :param req_ip:
    #     :param captcha:
    #     :param receiver:
    #     :return:
    #     """
    #     _email_data = self.makeup_send_reset_pw_mail(req_ip, captcha)
    #     sender.send_mail(_email_data['subject'], receiver, _email_data['body'])
    #
    # @staticmethod
    # def set_temporary_pw(verify_email, hash_pw):
    #     """
    #     设置临时密码
    #     :param verify_email:str,
    #     :param hash_pw:str,
    #     :return:bool
    #     """
    #     set_success = redis_store.set(verify_email, hash_pw, ex=setting.TEMPORARY_PW_EXPIRE_SECONDS)
    #     return set_success
    #
    # # TODO: see TemporaryPassword
    # @staticmethod
    # def get_temporary_pw(verify_email):
    #     """
    #     获取临时密码
    #     :param verify_email:str,
    #     :return:bool
    #     """
    #     return redis_store.get(verify_email)
    #
    # @staticmethod
    # def expire_temporary_pw(verify_email):
    #     """
    #     密码过期
    #     :param verify_email:
    #     :return:
    #     """
    #     return redis_store.expire(verify_email, -1)
    #
    # def verify_temporary_pw(self, verify_email, temporary_pw):
    #     """
    #     通过email查询临时密码并校验，同时一次校验之后，将临时密码直接设置过期
    #     :param verify_email:
    #     :param temporary_pw:
    #     :return:
    #     """
    #     hash_pw = self.hash_temporary_pw(temporary_pw)
    #     rdb_get = self.get_temporary_pw(verify_email)
    #     self.expire_temporary_pw(verify_email)
    #     if rdb_get:
    #         str_rdb_get = rdb_get.decode('utf-8')  # byte >>> str
    #         return str_rdb_get == hash_pw
    #     else:
    #         return None  # 密码过期
    #
    # @staticmethod
    # def hash_temporary_pw(temporary_pw):
    #     """
    #     加密临时密码
    #     :param temporary_pw:
    #     :return:
    #     """
    #     temporary_pw = str(temporary_pw) if isinstance(temporary_pw, int) else temporary_pw
    #     assert isinstance(temporary_pw, str)
    #     hash_pw = md5_encrypt(temporary_pw)
    #     return hash_pw
    #
    # def reset_pw_action(self, req_ip, verify_email):
    #     """
    #     更新用户临时密码到 redis 数据库（可设置过期时间），发送认证码邮件
    #     :param req_ip:str, 本次操作ip
    #     :param verify_email:str, 用户验证邮箱
    #     :return:
    #     """
    #     captcha = self.gen_captcha()
    #     hash_pw = self.hash_temporary_pw(captcha)
    #     set_success = self.set_temporary_pw(verify_email, hash_pw)
    #     if set_success:
    #         return self.send_reset_pw_mail(req_ip, captcha, verify_email)
    #     else:
    #         return 1

user_ctrl = UserCtrl()


if __name__ == '__main__':
    user = User.query.filter_by(username='orange')