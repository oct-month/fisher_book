"""
应用
"""
from flask import Flask
from app.models import db
from app.web import login_manager

def create_app():
    """新建Flask 对象"""
    app = Flask(__name__)
    app.config.from_object("app.secure")    # 导入配置文件
    app.config.from_object("app.setting")
    register_blueprint(app)

    db.init_app(app)                        # 把数据库模型与app关联（实际上是在设置config）
    login_manager.init_app(app)
    # 1、传参
    if app.config["NEW_TABLE"]:
        db.drop_all(app=app)
    db.create_all(app=app)                  # 建表
    # 2、上下文环境
    #with app.app_context():
    #    db.create_all()
    # 3、强行赋值（不建议），可以在建立db 对象时传入app 参数
    #db.app = app
    return app

def register_blueprint(app):
    """通过蓝图完善Flask 对象"""
    from app.web import web
    app.register_blueprint(web)
