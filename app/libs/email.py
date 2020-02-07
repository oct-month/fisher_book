from flask import current_app, render_template
from flask_mail import Message
from threading import Thread

from app.web import mail

def send_async_email(app, msg):
    """异步发送邮件"""
    with app.app_context():
        try:
            mail.send(msg)
        except Exception:
            pass

def send_email(to, title, template, **kwargs):
    """发送邮件"""
    #              标题        发送方                      正文          接收者们
    #msg = Message("测试邮件", sender="1944275918@qq.com", body="test", recipients=["41812200@snnu.edu.cn"])
    msg = Message("[鱼书] "+title, sender=current_app.config["MAIL_USERNAME"], recipients=[to])
    msg.html = render_template(template, **kwargs)
    app = current_app._get_current_object()     # 取到真实的app对象
    thr = Thread(target=send_async_email, args=(app, msg))
    thr.start()
