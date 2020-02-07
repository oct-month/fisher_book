"""
蓝图
"""
from flask import  Blueprint, render_template
from flask_login import LoginManager
from flask_mail import Mail

login_manager = LoginManager()
login_manager.login_view = "web.login"
login_manager.login_message = "用户没有登录，请先登录"

mail = Mail()

web = Blueprint("web", __name__, template_folder="templates")        # 新建蓝图（蓝图名，蓝图所在包）

@web.app_errorhandler(404)      # 定义404视图函数
def not_found(e):
    return render_template("404.html"), 404


from . import auth, book, drift, gift, main, wish
