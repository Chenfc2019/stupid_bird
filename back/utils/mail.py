# create by cfc 2021/11/30 9:02 上午

from flask_mail import Mail, Message

mail = Mail()


class SendMail(object):
    """发送邮件"""
    @staticmethod
    def send_mail(subject, to, body):
        message = Message(subject, recipients=[to], body=body)
        mail.send(message)
