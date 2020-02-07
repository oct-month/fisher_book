"""
蓝图
"""
from flask import  Blueprint
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = "web.login"
login_manager.login_message = "用户没有登录，请先登录"

web = Blueprint("web", __name__, template_folder="templates")        # 新建蓝图（蓝图名，蓝图所在包）

from . import auth, book, drift, gift, main, wish
